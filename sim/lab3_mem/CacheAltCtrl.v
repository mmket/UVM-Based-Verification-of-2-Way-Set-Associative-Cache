//=========================================================================
// Alt Blocking Cache Control
//=========================================================================

`ifndef LAB3_MEM_CACHE_ALT_CTRL_V
`define LAB3_MEM_CACHE_ALT_CTRL_V

`include "vc/regfiles.v"
`include "vc/mem-msgs.v"

module lab3_mem_CacheAltCtrl
#(
  parameter p_num_banks = 1
)
(
  input  logic        clk,
  input  logic        reset,

  // Processor <-> Cache Interface

  input  logic        proc2cache_reqstream_val,
  output logic        proc2cache_reqstream_rdy,

  output logic        proc2cache_respstream_val,
  input  logic        proc2cache_respstream_rdy,

  // Cache <-> Memory Interface

  output logic        cache2mem_reqstream_val,
  input  logic        cache2mem_reqstream_rdy,

  input  logic        cache2mem_respstream_val,
  output logic        cache2mem_respstream_rdy,

  // status signals (dpath->ctrl)

  input  logic  [2:0] cachereq_type,
  input  logic [31:0] cachereq_addr,

  input  logic [24:0] tag_array_read_out_0, tag_array_read_out_1,

  // control signals (ctrl->dpath)
  output logic        hit_TC,

  output logic        cachereq_reg_en,
  output logic        tag_array_wen,
  output logic        tag_array_ren,
  output logic        data_array_wen,
  output logic        data_array_ren,

  output logic [2:0] memreq_type,
  output logic write_data_from_mem,
  output logic write_addr_evict,

  output logic way_sel

);

  //----------------------------------------------------------------------
  // State Definitions
  //----------------------------------------------------------------------

  localparam STATE_IDLE              = 5'd0;
  localparam STATE_TAG_CHECK         = 5'd1;
  localparam STATE_INIT_DATA_ACCESS  = 5'd2;
  localparam STATE_READ_DATA_ACCESS  = 5'd3;
  localparam STATE_WRITE_DATA_ACCESS = 5'd4;
  localparam STATE_REFILL_REQUEST    = 5'd5;
  localparam STATE_REFILL_WAIT       = 5'd6;
  localparam STATE_REFILL_UPDATE     = 5'd7;
  localparam STATE_EVICT_PREPARE     = 5'd8;
  localparam STATE_EVICT_REQUEST     = 5'd9;
  localparam STATE_EVICT_WAIT        = 5'd10;
  localparam STATE_WAIT              = 5'd11;


  //----------------------------------------------------------------------
  // Valid/Dirty bits record
  //----------------------------------------------------------------------

  logic [3:0] cachereq_addr_index;
  logic [23:0] cache_req_tag;

  logic [1:0] cache_req_bank;

  generate
    if ( p_num_banks == 1 ) begin
      assign cachereq_addr_index = cachereq_addr[6:4];
      
      assign cache_req_tag = cachereq_addr[31:7];

      assign cache_req_bank = 2'b0;
    end
    else if ( p_num_banks == 4 ) begin
      // handle address mapping for four banks
      assign cachereq_addr_index = cachereq_addr[8:6];
      
      assign cache_req_tag = cachereq_addr[31:9];

      assign cache_req_bank = cachereq_addr[5:4];
    end
  endgenerate

  logic valid_bit_in;
  logic valid_bits_write_en, valid_bits_write_en_0, valid_bits_write_en_1;
  logic is_valid, is_valid_0, is_valid_1;

  logic dirty_bit_in;
  logic dirty_bits_write_en, dirty_bits_write_en_0, dirty_bits_write_en_1;
  logic is_dirty, is_dirty_0, is_dirty_1;

  logic least_recent_used;
  logic least_recent_used_in;
  logic LRU_wen;

  logic [1:0] tag_match;
  logic hit_way;

  logic is_init;

  always_ff @(posedge clk) begin
    if(reset) way_sel <= 0;
    else if(is_init) way_sel <= 0;
    else if((state_reg == STATE_TAG_CHECK) && hit_TC) way_sel <= hit_way;
    else if(state_reg == STATE_TAG_CHECK) way_sel <= least_recent_used;
  end

  assign valid_bits_write_en_0 = valid_bits_write_en && (way_sel == 1'b0);
  assign valid_bits_write_en_1 = valid_bits_write_en && (way_sel == 1'b1);
  assign dirty_bits_write_en_0 = dirty_bits_write_en && (way_sel == 1'b0);
  assign dirty_bits_write_en_1 = dirty_bits_write_en && (way_sel == 1'b1);

  // LRU
  vc_ResetRegfile_1r1w#(1,8) LRU_bits
  (
    .clk        (clk),
    .reset      (reset),
    .read_addr  (cachereq_addr_index),
    .read_data  (least_recent_used),
    .write_en   (LRU_wen),
    .write_addr (cachereq_addr_index),
    .write_data (least_recent_used_in)
  );

  always_comb begin
    if((state_reg == STATE_TAG_CHECK) && hit_TC) begin
      least_recent_used_in = !hit_way;
      LRU_wen = 1'b1;
    end
    else if(state_reg == STATE_REFILL_UPDATE) begin
      least_recent_used_in = !way_sel;
      LRU_wen = 1'b1;
    end
    else begin
      least_recent_used_in = least_recent_used;
      LRU_wen = 1'b0;
    end
  end
    
  // Way 0
  vc_ResetRegfile_1r1w#(1,8) valid_bits_0
  (
    .clk        (clk),
    .reset      (reset),
    .read_addr  (cachereq_addr_index),
    .read_data  (is_valid_0),
    .write_en   (valid_bits_write_en_0),
    .write_addr (cachereq_addr_index),
    .write_data (valid_bit_in)
  );

  vc_ResetRegfile_1r1w#(1,8) dirty_bits_0
  (
    .clk        (clk),
    .reset      (reset),
    .read_addr  (cachereq_addr_index),
    .read_data  (is_dirty_0),
    .write_en   (dirty_bits_write_en_0),
    .write_addr (cachereq_addr_index),
    .write_data (dirty_bit_in)
  );

  // Way 1
  vc_ResetRegfile_1r1w#(1,8) valid_bits_1
  (
    .clk        (clk),
    .reset      (reset),
    .read_addr  (cachereq_addr_index),
    .read_data  (is_valid_1),
    .write_en   (valid_bits_write_en_1),
    .write_addr (cachereq_addr_index),
    .write_data (valid_bit_in)
  );

  vc_ResetRegfile_1r1w#(1,8) dirty_bits_1
  (
    .clk        (clk),
    .reset      (reset),
    .read_addr  (cachereq_addr_index),
    .read_data  (is_dirty_1),
    .write_en   (dirty_bits_write_en_1),
    .write_addr (cachereq_addr_index),
    .write_data (dirty_bit_in)
  );
  
    
  // FINITE STATE MACHINE

  logic [4:0] state_reg, next_state;


  assign hit_TC = ((is_valid_0 && tag_match[0]) || (is_valid_1 && tag_match[1])) && !(cachereq_type == `VC_MEM_REQ_MSG_TYPE_WRITE_INIT);
  assign tag_match[0] = (cache_req_tag == tag_array_read_out_0);
  assign tag_match[1] = (cache_req_tag == tag_array_read_out_1);
  assign hit_way = is_valid_1 && tag_match[1];

  assign is_valid = (is_valid_0 || is_valid_1);
  assign is_dirty = !hit_TC && (((least_recent_used == 1'b0) && is_dirty_0) || ((least_recent_used == 1'b1) && is_dirty_1));

  always_comb begin
    case(state_reg)
      STATE_IDLE: next_state = proc2cache_reqstream_val ? STATE_TAG_CHECK : STATE_IDLE;

      STATE_TAG_CHECK: begin
        if(hit_TC || (cachereq_type == `VC_MEM_REQ_MSG_TYPE_WRITE_INIT)) begin
          case(cachereq_type)
            `VC_MEM_REQ_MSG_TYPE_READ: next_state = STATE_READ_DATA_ACCESS;         // read hit
            `VC_MEM_REQ_MSG_TYPE_WRITE: next_state = STATE_WRITE_DATA_ACCESS;       // write hit
            `VC_MEM_REQ_MSG_TYPE_WRITE_INIT: next_state = STATE_INIT_DATA_ACCESS;   // init
            default: next_state = STATE_IDLE;
          endcase
        end
        else begin
          next_state = is_dirty ? STATE_EVICT_PREPARE : STATE_REFILL_REQUEST;       // miss
        end
      end

      STATE_INIT_DATA_ACCESS: next_state = STATE_WAIT;
      STATE_READ_DATA_ACCESS: next_state = STATE_WAIT;
      STATE_WRITE_DATA_ACCESS: next_state = STATE_WAIT;

      STATE_EVICT_PREPARE: next_state = STATE_EVICT_REQUEST;
      STATE_EVICT_REQUEST: next_state = cache2mem_reqstream_rdy ? STATE_EVICT_WAIT : STATE_EVICT_REQUEST;
      STATE_EVICT_WAIT: next_state = cache2mem_respstream_val ? STATE_REFILL_REQUEST : STATE_EVICT_WAIT;

      STATE_REFILL_REQUEST: next_state = cache2mem_reqstream_rdy ? STATE_REFILL_WAIT : STATE_REFILL_REQUEST;
      STATE_REFILL_WAIT: next_state = cache2mem_respstream_val ? STATE_REFILL_UPDATE : STATE_REFILL_WAIT;

      STATE_REFILL_UPDATE: begin
        case(cachereq_type)
          `VC_MEM_REQ_MSG_TYPE_READ: next_state = STATE_READ_DATA_ACCESS;         // read
          `VC_MEM_REQ_MSG_TYPE_WRITE: next_state = STATE_WRITE_DATA_ACCESS;       // write
          default: next_state = STATE_IDLE;
        endcase
      end


      STATE_WAIT: next_state = proc2cache_respstream_rdy ? STATE_IDLE : STATE_WAIT;
      default: next_state = STATE_IDLE;
    endcase
  end

  always_ff @(posedge clk) begin
    if(reset) state_reg <= STATE_IDLE;
    else state_reg <= next_state;
  end

  assign is_init = (cachereq_type == `VC_MEM_REQ_MSG_TYPE_WRITE_INIT);

  // Controls from FSM
  task cs
  (
    input logic cs_cachereq_rdy,
    input logic cs_cacheresp_val,
    input logic cs_cachereq_reg_en,
    input logic cs_tag_array_wen,
    input logic cs_tag_array_ren,
    input logic cs_data_array_wen,
    input logic cs_data_array_ren,
    input logic cs_valid_bit_in,
    input logic cs_valid_bits_write_en,
    input logic cs_dirty_bit_in,
    input logic cs_dirty_bits_write_en
  );
  begin
    proc2cache_reqstream_rdy  = cs_cachereq_rdy;
    proc2cache_respstream_val = cs_cacheresp_val;
    cachereq_reg_en           = cs_cachereq_reg_en;
    tag_array_wen             = cs_tag_array_wen;
    tag_array_ren             = cs_tag_array_ren;
    data_array_wen            = cs_data_array_wen;
    data_array_ren            = cs_data_array_ren;
    valid_bit_in              = cs_valid_bit_in;
    valid_bits_write_en       = cs_valid_bits_write_en;
    dirty_bit_in              = cs_dirty_bit_in;
    dirty_bits_write_en       = cs_dirty_bits_write_en;
  end
  endtask

  // Set outputs using a control signal "table"
  always @(*) begin
                              cs( 0,   0,    0,    0,    0,    0,    0,    0,    0,    0,    0     );
    case ( state_reg )
      //                         cache cache cache tag   tag   data  data  valid valid dirty dirty
      //                         req   resp  req   array array array array bit   write bit   write
      //                         rdy   val   en    wen   ren   wen   ren   in    en    in    en
      STATE_IDLE:             cs( 1,   0,    1,    0,    0,    0,    0,    0,    0,    0,    0     );
      STATE_TAG_CHECK:        cs( 0,   0,    0,    0,    1,    0,    0,    0,    0,    0,    0     );

      STATE_INIT_DATA_ACCESS: cs( 0,   0,    0,    1,    0,    1,    0,    1,    1,    0,    0     );
      STATE_READ_DATA_ACCESS: cs( 0,   0,    0,    0,    0,    0,    1,    0,    0,    0,    0     );
      STATE_WRITE_DATA_ACCESS:cs( 0,   0,    0,    0,    0,    1,    0,    0,    0,    1,    1     );

      STATE_REFILL_REQUEST:   cs( 0,   0,    0,    0,    0,    0,    0,    0,    0,    0,    0     );
      STATE_REFILL_WAIT:      cs( 0,   0,    0,    0,    0,    0,    0,    0,    0,    0,    0     );
      STATE_REFILL_UPDATE:    cs( 0,   0,    0,    1,    0,    1,    0,    1,    1,    0,    1     );

      STATE_EVICT_PREPARE:    cs( 0,   0,    0,    0,    1,    0,    1,    0,    0,    0,    0     );
      STATE_EVICT_REQUEST:    cs( 0,   0,    0,    0,    0,    0,    0,    0,    0,    0,    0     );
      STATE_EVICT_WAIT:       cs( 0,   0,    0,    0,    0,    0,    0,    0,    0,    0,    0     );


      STATE_WAIT:             cs( 0,   1,    0,    0,    0,    0,    0,    0,    0,    0,    0     );
      default:                cs( 0,   0,    0,    0,    0,    0,    0,    0,    0,    0,    0     );

    endcase
  end

  // cache <-> memory interface val/rdy signals

  assign cache2mem_reqstream_val  = (state_reg == STATE_REFILL_REQUEST) || (state_reg == STATE_EVICT_REQUEST);
  assign cache2mem_respstream_rdy = (state_reg == STATE_REFILL_WAIT) || (state_reg == STATE_EVICT_WAIT);
  assign write_data_from_mem = (state_reg == STATE_REFILL_UPDATE);
  assign write_addr_evict = (state_reg == STATE_EVICT_REQUEST);

  always_comb begin
    case(state_reg)
      STATE_REFILL_REQUEST: memreq_type = `VC_MEM_REQ_MSG_TYPE_READ;
      STATE_EVICT_REQUEST: memreq_type = `VC_MEM_REQ_MSG_TYPE_WRITE;
      default: memreq_type = `VC_MEM_REQ_MSG_TYPE_X;
    endcase
  end

endmodule

`endif
