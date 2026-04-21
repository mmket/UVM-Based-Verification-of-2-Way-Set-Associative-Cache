//=========================================================================
// Testbench top: lab3_mem CacheAlt + UVM
//=========================================================================
`timescale 1ns/1ps

// mem-msgs must be compiled before this module (see compile_uvm.f).

module tb_top;
  import uvm_pkg::*;
  import cache_uvm_pkg::*;

  logic clk;
  logic reset;

  initial begin
    clk = 0;
    forever #5 clk = ~clk;
  end

  initial begin
    reset = 1;
    repeat (4) @(posedge clk);
    reset = 0;
  end

  cache_proc_if proc_if (.clk(clk), .reset(reset));
  cache_mem_if  mem_if  (.clk(clk), .reset(reset));

  mem_req_4B_t   dut_proc_req;
  mem_resp_4B_t  dut_proc_resp;
  mem_req_16B_t  dut_mem_req;
  mem_resp_16B_t dut_mem_resp;

  assign dut_proc_req = mem_req_4B_t'(proc_if.req_msg);
  assign proc_if.resp_msg = $bits(proc_if.resp_msg)'(dut_proc_resp);

  assign mem_if.req_msg = $bits(mem_if.req_msg)'(dut_mem_req);
  assign dut_mem_resp = mem_resp_16B_t'(mem_if.resp_msg);

  lab3_mem_CacheAlt dut (
    .clk                        (clk),
    .reset                      (reset),
    .proc2cache_reqstream_msg   (dut_proc_req),
    .proc2cache_reqstream_val   (proc_if.req_val),
    .proc2cache_reqstream_rdy   (proc_if.req_rdy),
    .proc2cache_respstream_msg  (dut_proc_resp),
    .proc2cache_respstream_val  (proc_if.resp_val),
    .proc2cache_respstream_rdy  (proc_if.resp_rdy),
    .cache2mem_reqstream_msg    (dut_mem_req),
    .cache2mem_reqstream_val    (mem_if.req_val),
    .cache2mem_reqstream_rdy    (mem_if.req_rdy),
    .cache2mem_respstream_msg   (dut_mem_resp),
    .cache2mem_respstream_val   (mem_if.resp_val),
    .cache2mem_respstream_rdy   (mem_if.resp_rdy)
  );

  initial begin
    uvm_config_db#(virtual cache_proc_if)::set(null, "uvm_test_top.env.proc_agent.*", "vif", proc_if);
    uvm_config_db#(virtual cache_mem_if)::set(null, "uvm_test_top.env.mem_agent.*", "vif", mem_if);
    uvm_config_db#(virtual cache_proc_if)::set(null, "uvm_test_top.env.sb", "proc_vif", proc_if);
    uvm_config_db#(virtual cache_mem_if)::set(null, "uvm_test_top.env.sb", "mem_vif", mem_if);
    run_test();
  end
endmodule
