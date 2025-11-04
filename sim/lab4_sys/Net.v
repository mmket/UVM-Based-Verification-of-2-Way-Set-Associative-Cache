//========================================================================
// Ring Network
//========================================================================

`ifndef LAB4_SYS_NET_V
`define LAB4_SYS_NET_V

`include "vc/net-msgs.v"
`include "vc/trace.v"
`include "vc/queues.v"

`include "lab4_sys/NetRouter.v"

module lab4_sys_Net
#(
  parameter p_msg_nbits = 44
)
(
  input  logic                   clk,
  input  logic                   reset,

  // Input streams

  input  logic [p_msg_nbits-1:0] istream_msg [4],
  input  logic                   istream_val [4],
  output logic                   istream_rdy [4],

  // Output streams

  output logic [p_msg_nbits-1:0] ostream_msg [4],
  output logic                   ostream_val [4],
  input  logic                   ostream_rdy [4]
);

  // Clockwise and couter-clockwise channels

  logic [p_msg_nbits-1:0] channels_cw_msg  [4];
  logic                   channels_cw_val  [4];
  logic                   channels_cw_rdy  [4];

  logic [p_msg_nbits-1:0] channels_ccw_msg [4];
  logic                   channels_ccw_val [4];
  logic                   channels_ccw_rdy [4];

  //''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // Implement ring network with four routers
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  //----------------------------------------------------------------------
  // Line Tracing
  //----------------------------------------------------------------------

  `ifndef SYNTHESIS

  // Generate for loop to instantiate trace modules

  genvar j;
  generate
  for ( j = 0; j < 4; j = j + 1 ) begin: CHANNEL_TRACE

    vc_NetMsgMiniTrace#(p_msg_nbits) cw_trace
    (
      .clk   (clk),
      .reset (reset),
      .msg   (channels_cw_msg[j]),
      .val   (channels_cw_val[j]),
      .rdy   (channels_cw_rdy[j])
    );

    vc_NetMsgMiniTrace#(p_msg_nbits) ccw_trace
    (
      .clk   (clk),
      .reset (reset),
      .msg   (channels_ccw_msg[j]),
      .val   (channels_ccw_val[j]),
      .rdy   (channels_ccw_rdy[j])
    );

  end
  endgenerate

  logic [`VC_TRACE_NBITS-1:0] str;
  `VC_TRACE_BEGIN
  begin

    // Line tracing for clockwise channels

    CHANNEL_TRACE[0].cw_trace.line_trace( trace_str );
    vc_trace.append_str( trace_str, "|" );
    CHANNEL_TRACE[1].cw_trace.line_trace( trace_str );
    vc_trace.append_str( trace_str, "|" );
    CHANNEL_TRACE[2].cw_trace.line_trace( trace_str );
    vc_trace.append_str( trace_str, "|" );
    CHANNEL_TRACE[3].cw_trace.line_trace( trace_str );

    vc_trace.append_str( trace_str, "I" );

    // Line tracing for counter clockwise channels

    CHANNEL_TRACE[0].ccw_trace.line_trace( trace_str );
    vc_trace.append_str( trace_str, "|" );
    CHANNEL_TRACE[1].ccw_trace.line_trace( trace_str );
    vc_trace.append_str( trace_str, "|" );
    CHANNEL_TRACE[2].ccw_trace.line_trace( trace_str );
    vc_trace.append_str( trace_str, "|" );
    CHANNEL_TRACE[3].ccw_trace.line_trace( trace_str );

  end
  `VC_TRACE_END

  `endif /* SYNTHESIS */

endmodule

`endif /* LAB4_SYS_NET_V */
