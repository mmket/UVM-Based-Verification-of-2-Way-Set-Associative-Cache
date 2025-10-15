//=========================================================================
// Base Blocking Cache Datapath
//=========================================================================

`ifndef LAB3_MEM_CACHE_BASE_DPATH_V
`define LAB3_MEM_CACHE_BASE_DPATH_V

`include "vc/mem-msgs.v"
`include "vc/srams.v"
`include "vc/regs.v"

module lab3_mem_CacheBaseDpath
#(
  parameter p_num_banks = 1
)
(
  input  logic          clk,
  input  logic          reset,

  // Processor <-> Cache Interface

  input  mem_req_4B_t   proc2cache_reqstream_msg,
  output mem_resp_4B_t  proc2cache_respstream_msg,

  // Cache <-> Memory Interface

  output mem_req_16B_t  cache2mem_reqstream_msg,
  input  mem_resp_16B_t cache2mem_respstream_msg,

  input  logic          cache2mem_respstream_val,
  input  logic          cache2mem_respstream_rdy,

  // control signals (ctrl->dpath)

  input  logic          cachereq_reg_en,
  input  logic          tag_array_wen,
  input  logic          tag_array_ren,
  input  logic          data_array_wen,
  input  logic          data_array_ren,

  input  logic        hit_TC,

  input  logic [2:0]    memreq_type,
  input logic write_data_from_mem,
  input logic write_addr_evict,

  // status signals (dpath->ctrl)

  output logic  [2:0]   cachereq_type,
  output logic [31:0]   cachereq_addr,

  output logic [23:0] tag_array_read_out
);

    // Register the unpacked proc2cache_reqstream_msg

  logic [31:0] cachereq_addr_reg_out;
  logic [31:0] cachereq_data_reg_out;
  logic  [2:0] cachereq_type_reg_out;
  logic  [7:0] cachereq_opaque_reg_out;

  vc_EnResetReg #(3,0) cachereq_type_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (cachereq_reg_en),
    .d      (proc2cache_reqstream_msg.type_),
    .q      (cachereq_type_reg_out)
  );

  vc_EnResetReg #(32,0) cachereq_addr_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (cachereq_reg_en),
    .d      (proc2cache_reqstream_msg.addr),
    .q      (cachereq_addr_reg_out)
  );

  vc_EnResetReg #(8,0) cachereq_opaque_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (cachereq_reg_en),
    .d      (proc2cache_reqstream_msg.opaque),
    .q      (cachereq_opaque_reg_out)
  );

  vc_EnResetReg #(32,0) cachereq_data_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (cachereq_reg_en),
    .d      (proc2cache_reqstream_msg.data),
    .q      (cachereq_data_reg_out)
  );

  assign cachereq_type = cachereq_type_reg_out;
  assign cachereq_addr = cachereq_addr_reg_out;

  // Address Mapping

  logic  [1:0] cachereq_addr_byte_offset;
  logic  [1:0] cachereq_addr_word_offset;
  logic  [3:0] cachereq_addr_index;
  logic [23:0] cachereq_addr_tag;
  logic  [1:0] cachereq_addr_bank;

  logic [31:0] mk_addr_refill;
  logic [31:0] mk_addr_evict;
  logic [31:0] mk_addr_evict_reg_out;

  generate
    if ( p_num_banks == 1 ) begin
      assign cachereq_addr_byte_offset = cachereq_addr[1:0];
      assign cachereq_addr_word_offset = cachereq_addr[3:2];
      assign cachereq_addr_index       = cachereq_addr[7:4];
      assign cachereq_addr_tag         = cachereq_addr[31:8];

      assign cachereq_addr_bank = 2'b0;

      assign mk_addr_refill = {cachereq_addr_reg_out[31:4], 4'b0};
      assign mk_addr_evict = {tag_array_read_out, cachereq_addr_reg_out[7:4], 4'b0};
    end
    else if ( p_num_banks == 4 ) begin
      // handle address mapping for four banks
      assign cachereq_addr_byte_offset = cachereq_addr[1:0];
      assign cachereq_addr_word_offset = cachereq_addr[3:2];
      assign cachereq_addr_index       = cachereq_addr[9:6];
      assign cachereq_addr_tag         = cachereq_addr[31:10];

      assign cachereq_addr_bank = cachereq_addr[5:4];

      assign mk_addr_refill = {cachereq_addr_reg_out[31:4], 4'b0};
      assign mk_addr_evict = {tag_array_read_out[21:0], cachereq_addr_reg_out[9:6], cachereq_addr_reg_out[5:4], 4'b0};
    end
  endgenerate

  vc_EnResetReg #(32,0) evict_addr_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (tag_array_ren),
    .d      (mk_addr_evict),
    .q      (mk_addr_evict_reg_out)
  );

  // Replicate cachereq_data

  logic [127:0] cachereq_data_replicated;

  assign cachereq_data_replicated = {4{cachereq_data_reg_out}};

  // Write byte enable decoder

  logic [15:0] wben_decoder_out;

  always_comb begin
    if(write_data_from_mem) wben_decoder_out = 16'hffff;
    else begin
      case ( cachereq_addr_word_offset )
        2'd0: wben_decoder_out = 16'h000f;
        2'd1: wben_decoder_out = 16'h00f0;
        2'd2: wben_decoder_out = 16'h0f00;
        2'd3: wben_decoder_out = 16'hf000;
        default: wben_decoder_out = 16'h000f;
      endcase
    end
  end

  logic [127:0] data_array_read_out;
  logic [127:0] data_array_write_in;
  logic [127:0] memresp_data;

  genvar i;

  assign data_array_write_in = write_data_from_mem ? memresp_data : cachereq_data_replicated;

  // Tag array (16 tags, 24 bits/tag)
  vc_CombinationalBitSRAM_1rw
  #(
    .p_data_nbits  (24),
    .p_num_entries (16)
  )
  tag_array
  (
    .clk           (clk),
    .reset         (reset),
    .read_addr     (cachereq_addr_index),
    .read_data     (tag_array_read_out),
    .write_en      (tag_array_wen),
    .read_en       (tag_array_ren),
    .write_addr    (cachereq_addr_index),
    .write_data    (cachereq_addr_tag)
  );

  // Data array (16 cacheslines, 128 bits/cacheline)
  vc_CombinationalSRAM_1rw #(128,16) data_array
  (
    .clk           (clk),
    .reset         (reset),
    .read_addr     (cachereq_addr_index),
    .read_data     (data_array_read_out),
    .write_en      (data_array_wen),
    .read_en       (data_array_ren),
    .write_byte_en (wben_decoder_out),
    .write_addr    (cachereq_addr_index),
    .write_data    (data_array_write_in)
  );


  // proc2cache_respstream_msg
  logic test;
  logic [127:0] read_data_reg;

  assign proc2cache_respstream_msg.type_  = cachereq_type;
  assign proc2cache_respstream_msg.opaque = cachereq_opaque_reg_out;
  assign proc2cache_respstream_msg.test   = test;
  assign proc2cache_respstream_msg.len    = 2'b0;

  always_comb begin
    case(cachereq_addr_word_offset)
      2'd0: proc2cache_respstream_msg.data = read_data_reg[31:0];
      2'd1: proc2cache_respstream_msg.data = read_data_reg[63:32];
      2'd2: proc2cache_respstream_msg.data = read_data_reg[95:64];
      2'd3: proc2cache_respstream_msg.data = read_data_reg[127:96];
      default: proc2cache_respstream_msg.data = read_data_reg[31:0];
    endcase
  end

  always_ff @(posedge clk) begin
    if(reset) test   <= 0;
    else if(tag_array_ren) test   <= hit_TC;
    else test <= test;
  end

  always_ff @(posedge clk) begin
    if(reset) read_data_reg   <= 0;
    else if(data_array_ren) read_data_reg <= data_array_read_out;
    else if(data_array_wen) read_data_reg <= 0;
    else read_data_reg <= read_data_reg;
  end

  // cache2mem_reqstream_msg

  assign cache2mem_reqstream_msg.type_ = memreq_type;
  assign cache2mem_reqstream_msg.len = 4'b0;
  assign cache2mem_reqstream_msg.addr = write_addr_evict ? mk_addr_evict_reg_out : mk_addr_refill;
  assign cache2mem_reqstream_msg.data = read_data_reg;
  assign cache2mem_reqstream_msg.opaque = 8'b0;

  vc_EnResetReg #(128,0) memresp_data_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (cache2mem_respstream_val && cache2mem_respstream_rdy),
    .d      (cache2mem_respstream_msg.data),
    .q      (memresp_data)
  );

endmodule

`endif
