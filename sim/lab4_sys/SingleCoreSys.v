//========================================================================
// Single-Core System
//========================================================================

`ifndef LAB4_SYS_SINGLE_CORE_SYS_V
`define LAB4_SYS_SINGLE_CORE_SYS_V

`include "vc/mem-msgs.v"
`include "vc/trace.v"

`include "lab2_proc/ProcAlt.v"
`include "lab3_mem/CacheAlt.v"

module lab4_sys_SingleCoreSys
(
  input  logic          clk,
  input  logic          reset,

  // From mngr streaming port

  input  logic [31:0]   mngr2proc_msg,
  input  logic          mngr2proc_val,
  output logic          mngr2proc_rdy,

  // To mngr streaming port

  output logic [31:0]   proc2mngr_msg,
  output logic          proc2mngr_val,
  input  logic          proc2mngr_rdy,

  // Instruction Memory Request Port

  output mem_req_16B_t  imem_reqstream_msg,
  output logic          imem_reqstream_val,
  input  logic          imem_reqstream_rdy,

  // Instruction Memory Response Port

  input  mem_resp_16B_t imem_respstream_msg,
  input  logic          imem_respstream_val,
  output logic          imem_respstream_rdy,

  // Data Memory Request Port

  output mem_req_16B_t  dmem_reqstream_msg,
  output logic          dmem_reqstream_val,
  input  logic          dmem_reqstream_rdy,

  // Data Memory Response Port

  input  mem_resp_16B_t dmem_respstream_msg,
  input  logic          dmem_respstream_val,
  output logic          dmem_respstream_rdy,

  // stats output

  output logic          stats_en,
  output logic          commit_inst,
  output logic          icache_access,
  output logic          icache_miss,
  output logic          dcache_access,
  output logic          dcache_miss
);

  //''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // Instantiate and connect processor and caches
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  // Use some extra ports to report on the number of cache accesses and
  // misses to be able to calculate the miss rate in the evaluation
  // simulator. If you use different names for your wires, you may need
  // to update this logic.

  assign icache_access = icache_reqstream_val  & icache_reqstream_rdy;
  assign icache_miss   = icache_respstream_val & icache_respstream_rdy & ~icache_respstream_msg.test[0];
  assign dcache_access = dcache_reqstream_val  & dcache_reqstream_rdy;
  assign dcache_miss   = dcache_respstream_val & dcache_respstream_rdy & ~dcache_respstream_msg.test[0];

  //----------------------------------------------------------------------
  // Line Traceing
  //----------------------------------------------------------------------
  // If you use different instance names for your processor and caches,
  // you may need to update the line tracing logic.

  `ifndef SYNTHESIS

  `VC_TRACE_BEGIN
  begin
    proc.line_trace( trace_str );
    vc_trace.append_str( trace_str, "|" );
    icache.line_trace( trace_str );
    dcache.line_trace( trace_str );
  end
  `VC_TRACE_END

   `endif /* SYNTHESIS */

endmodule

`endif /* LAB4_SYS_SINGLE_CORE_SYS_V */
