//========================================================================
// Network Router
//========================================================================

`ifndef LAB4_SYS_NET_ROUTER_V
`define LAB4_SYS_NET_ROUTER_V

`include "vc/net-msgs.v"
`include "vc/trace.v"
`include "vc/queues.v"

`include "lab4_sys/NetRouterRouteUnit.v"
`include "lab4_sys/NetRouterSwitchUnit.v"

module lab4_sys_NetRouter
#(
  parameter p_msg_nbits = 44
)
(
  input  logic                   clk,
  input  logic                   reset,

  // Router id (which router is this in the network?)

  input  logic     [1:0]         router_id,

  // Input streams

  input  logic [p_msg_nbits-1:0] istream_msg [3],
  input  logic                   istream_val [3],
  output logic                   istream_rdy [3],

  // Output streams

  output logic [p_msg_nbits-1:0] ostream_msg [3],
  output logic                   ostream_val [3],
  input  logic                   ostream_rdy [3]
);

  //''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // Implement router with input queues, route units, and switch units
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  //----------------------------------------------------------------------
  // Line Tracing
  //----------------------------------------------------------------------

  `ifndef SYNTHESIS

  vc_NetMsgTrace#(p_msg_nbits) ostream0_trace
  (
    .clk   (clk),
    .reset (reset),
    .msg   (ostream_msg[0]),
    .val   (ostream_val[0]),
    .rdy   (ostream_rdy[0])
  );

  vc_NetMsgTrace#(p_msg_nbits) ostream1_trace
  (
    .clk   (clk),
    .reset (reset),
    .msg   (ostream_msg[1]),
    .val   (ostream_val[1]),
    .rdy   (ostream_rdy[1])
  );

  vc_NetMsgTrace#(p_msg_nbits) ostream2_trace
  (
    .clk   (clk),
    .reset (reset),
    .msg   (ostream_msg[2]),
    .val   (ostream_val[2]),
    .rdy   (ostream_rdy[2])
  );

  logic [`VC_TRACE_NBITS-1:0] str;
  `VC_TRACE_BEGIN
  begin

    // Line tracing for input queues

    case ( inq0_num_free_entries )
      4: vc_trace.append_str( trace_str, " " );
      3: vc_trace.append_str( trace_str, "." );
      2: vc_trace.append_str( trace_str, ":" );
      1: vc_trace.append_str( trace_str, "*" );
      0: vc_trace.append_str( trace_str, "#" );
    endcase

    case ( inq1_num_free_entries )
      4: vc_trace.append_str( trace_str, " " );
      3: vc_trace.append_str( trace_str, "." );
      2: vc_trace.append_str( trace_str, ":" );
      1: vc_trace.append_str( trace_str, "*" );
      0: vc_trace.append_str( trace_str, "#" );
    endcase

    case ( inq2_num_free_entries )
      4: vc_trace.append_str( trace_str, " " );
      3: vc_trace.append_str( trace_str, "." );
      2: vc_trace.append_str( trace_str, ":" );
      1: vc_trace.append_str( trace_str, "*" );
      0: vc_trace.append_str( trace_str, "#" );
    endcase

    vc_trace.append_str( trace_str, "|" );

    // Line tracing for switch units

    sunit0.line_trace( trace_str );
    sunit1.line_trace( trace_str );
    sunit2.line_trace( trace_str );

  end
  `VC_TRACE_END

  `endif /* SYNTHESIS */

endmodule

`endif /* NET_ROUTER_V */
