`ifndef CACHE_MEM_SLAVE_SVH
`define CACHE_MEM_SLAVE_SVH

// Behavioral memory backing store (16B lines). Drives cache_mem_if resp channel.
class cache_mem_slave extends uvm_component;
  `uvm_component_utils(cache_mem_slave)
  virtual cache_mem_if vif;

  logic [127:0] line_ram [bit [27:0]];
  bit           busy;

  function new(string name, uvm_component parent);
    super.new(name, parent);
  endfunction

  function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    if (!uvm_config_db#(virtual cache_mem_if)::get(this, "", "vif", vif))
      `uvm_fatal("NOVIF", "cache_mem_if not set for mem slave")
  endfunction

  function logic [127:0] get_line(logic [31:0] byte_addr);
    bit [27:0] lid;
    lid = byte_addr[31:4];
    if (!line_ram.exists(lid))
      return 128'h0;
    return line_ram[lid];
  endfunction

  function void set_line(logic [31:0] byte_addr, logic [127:0] d);
    bit [27:0] lid;
    lid = byte_addr[31:4];
    line_ram[lid] = d;
  endfunction

  task run_phase(uvm_phase phase);
    logic [175:0] req_bits;
    logic [145:0] rsp_bits;
    logic [3:0]   rq_ty, rs_ty;
    logic [7:0]   rq_op, rs_op;
    logic [31:0]  rq_ad;
    logic [3:0]   rq_len;
    logic [127:0] rq_dat, rs_dat;
    logic [1:0]   rs_test;
    logic [3:0]   rs_len;

    busy = 0;
    vif.resp_val <= 1'b0;
    forever @(posedge vif.clk) begin
      if (vif.reset) begin
        busy = 0;
        vif.resp_val <= 1'b0;
        continue;
      end
      if (busy && vif.resp_val && vif.resp_rdy) begin
        vif.resp_val <= 1'b0;
        busy = 0;
      end
      if (!busy && vif.req_val && vif.req_rdy) begin
        req_bits = vif.req_msg;
        unpack_mem_req_16B(req_bits, rq_ty, rq_op, rq_ad, rq_len, rq_dat);
        if (rq_ty == VC_MEM_REQ_MSG_TYPE_READ) begin
          rs_dat   = get_line(rq_ad);
          rs_ty    = VC_MEM_RESP_MSG_TYPE_READ;
          rs_op    = rq_op;
          rs_test  = 2'b0;
          rs_len   = 4'h0;
          rsp_bits = pack_mem_resp_16B(rs_ty, rs_op, rs_test, rs_len, rs_dat);
        end
        else begin
          set_line(rq_ad, rq_dat);
          rs_dat   = 128'h0;
          rs_ty    = VC_MEM_RESP_MSG_TYPE_WRITE;
          rs_op    = rq_op;
          rs_test  = 2'b0;
          rs_len   = 4'h0;
          rsp_bits = pack_mem_resp_16B(rs_ty, rs_op, rs_test, rs_len, rs_dat);
        end
        vif.resp_msg <= rsp_bits;
        vif.resp_val <= 1'b1;
        busy = 1;
      end
    end
  endtask
endclass

`endif
