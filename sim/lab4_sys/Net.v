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

  genvar k;

  logic [p_msg_nbits-1:0] router_in_msg [0:3][0:2];   // [router] [port]
  logic                   router_in_val [0:3][0:2];
  logic                   router_in_rdy [0:3][0:2];

  logic [p_msg_nbits-1:0] router_out_msg [0:3][0:2];   // [router] [port]
  logic                   router_out_val [0:3][0:2];
  logic                   router_out_rdy [0:3][0:2];



  // Router 0
  assign router_in_msg[0][0] = router_out_msg[3][2];
  assign router_in_val[0][0] = router_out_val[3][2];
  assign router_out_rdy[3][2] = router_in_rdy[0][0];

  assign router_in_msg[0][1] = istream_msg[0];
  assign router_in_val[0][1] = istream_val[0];
  assign istream_rdy[0] = router_in_rdy[0][1];

  assign router_in_msg[0][2] = router_out_msg[1][0];
  assign router_in_val[0][2] = router_out_val[1][0];
  assign router_out_rdy[1][0] = router_in_rdy[0][2];


  // Router 1
  assign router_in_msg[1][0] = router_out_msg[0][2];
  assign router_in_val[1][0] = router_out_val[0][2];
  assign router_out_rdy[0][2] = router_in_rdy[1][0];

  assign router_in_msg[1][1] = istream_msg[1];
  assign router_in_val[1][1] = istream_val[1];
  assign istream_rdy[1] = router_in_rdy[1][1];

  assign router_in_msg[1][2] = router_out_msg[2][0];
  assign router_in_val[1][2] = router_out_val[2][0];
  assign router_out_rdy[2][0] = router_in_rdy[1][2];

  // Router 2
  assign router_in_msg[2][0] = router_out_msg[1][2];
  assign router_in_val[2][0] = router_out_val[1][2];
  assign router_out_rdy[1][2] = router_in_rdy[2][0];

  assign router_in_msg[2][1] = istream_msg[2];
  assign router_in_val[2][1] = istream_val[2];
  assign istream_rdy[2] = router_in_rdy[2][1];

  assign router_in_msg[2][2] = router_out_msg[3][0];
  assign router_in_val[2][2] = router_out_val[3][0];
  assign router_out_rdy[3][0] = router_in_rdy[2][2];
  

  // Router 3
  assign router_in_msg[3][0] = router_out_msg[2][2];
  assign router_in_val[3][0] = router_out_val[2][2];
  assign router_out_rdy[2][2] = router_in_rdy[3][0];

  assign router_in_msg[3][1] = istream_msg[3];
  assign router_in_val[3][1] = istream_val[3];
  assign istream_rdy[3] = router_in_rdy[3][1];

  assign router_in_msg[3][2] = router_out_msg[0][0];
  assign router_in_val[3][2] = router_out_val[0][0];
  assign router_out_rdy[0][0] = router_in_rdy[3][2];


  // Output 
  assign ostream_msg[0] = router_out_msg[0][1];
  assign ostream_val[0] = router_out_val[0][1];
  assign router_out_rdy[0][1] = ostream_rdy[0];

  assign ostream_msg[1] = router_out_msg[1][1];
  assign ostream_val[1] = router_out_val[1][1];
  assign router_out_rdy[1][1] = ostream_rdy[1];

  assign ostream_msg[2] = router_out_msg[2][1];
  assign ostream_val[2] = router_out_val[2][1];
  assign router_out_rdy[2][1] = ostream_rdy[2];

  assign ostream_msg[3] = router_out_msg[3][1];
  assign ostream_val[3] = router_out_val[3][1];
  assign router_out_rdy[3][1] = ostream_rdy[3];


generate
  for(k=0; k<4; k=k+1) begin
      lab4_sys_NetRouter
    #(
      .p_msg_nbits(p_msg_nbits)
    )
      Router
    (
      .clk(clk),
      .reset(reset),

      // Router id (which router is this in the network?)

      .router_id(k),

      // Input streams

      .istream_msg(router_in_msg[k]),
      .istream_val(router_in_val[k]),
      .istream_rdy(router_in_rdy[k]),

      // Output streams

      .ostream_msg(router_out_msg[k]),
      .ostream_val(router_out_val[k]),
      .ostream_rdy(router_out_rdy[k])
    );
  end
endgenerate

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
