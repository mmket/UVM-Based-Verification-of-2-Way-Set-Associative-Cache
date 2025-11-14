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

genvar k;
parameter p_type = `VC_QUEUE_NORMAL;
parameter p_num_msgs = 4;

logic [p_msg_nbits-1:0] out_queue_msg [0:2];
logic                   out_queue_val [0:2];
logic                   out_queue_rdy [0:2];

logic [$clog2(p_num_msgs):0] inq_num_free_entries [0:2];

logic [p_msg_nbits-1:0] Route_Unit_out_msg [0:2][0:2];      // [Route Unit] [Output Port]
logic                   Route_Unit_out_val [0:2][0:2];
logic                   Route_Unit_out_rdy [0:2][0:2];

logic [p_msg_nbits-1:0] Switch_Unit_in_msg [0:2][0:2];      // [Switch Unit] [Input Port]
logic                   Switch_Unit_in_val [0:2][0:2];
logic                   Switch_Unit_in_rdy [0:2][0:2];


assign Switch_Unit_in_msg[0][0] = Route_Unit_out_msg[0][0];
assign Switch_Unit_in_val[0][0] = Route_Unit_out_val[0][0];
assign Route_Unit_out_rdy[0][0] = Switch_Unit_in_rdy[0][0];

assign Switch_Unit_in_msg[0][1] = Route_Unit_out_msg[1][0];
assign Switch_Unit_in_val[0][1] = Route_Unit_out_val[1][0];
assign Route_Unit_out_rdy[1][0] = Switch_Unit_in_rdy[0][1];

assign Switch_Unit_in_msg[0][2] = Route_Unit_out_msg[2][0];
assign Switch_Unit_in_val[0][2] = Route_Unit_out_val[2][0];
assign Route_Unit_out_rdy[2][0] = Switch_Unit_in_rdy[0][2];


assign Switch_Unit_in_msg[1][0] = Route_Unit_out_msg[0][1];
assign Switch_Unit_in_val[1][0] = Route_Unit_out_val[0][1];
assign Route_Unit_out_rdy[0][1] = Switch_Unit_in_rdy[1][0];

assign Switch_Unit_in_msg[1][1] = Route_Unit_out_msg[1][1];
assign Switch_Unit_in_val[1][1] = Route_Unit_out_val[1][1];
assign Route_Unit_out_rdy[1][1] = Switch_Unit_in_rdy[1][1];

assign Switch_Unit_in_msg[1][2] = Route_Unit_out_msg[2][1];
assign Switch_Unit_in_val[1][2] = Route_Unit_out_val[2][1];
assign Route_Unit_out_rdy[2][1] = Switch_Unit_in_rdy[1][2];


assign Switch_Unit_in_msg[2][0] = Route_Unit_out_msg[0][2];
assign Switch_Unit_in_val[2][0] = Route_Unit_out_val[0][2];
assign Route_Unit_out_rdy[0][2] = Switch_Unit_in_rdy[2][0];

assign Switch_Unit_in_msg[2][1] = Route_Unit_out_msg[1][2];
assign Switch_Unit_in_val[2][1] = Route_Unit_out_val[1][2];
assign Route_Unit_out_rdy[1][2] = Switch_Unit_in_rdy[2][1];

assign Switch_Unit_in_msg[2][2] = Route_Unit_out_msg[2][2];
assign Switch_Unit_in_val[2][2] = Route_Unit_out_val[2][2];
assign Route_Unit_out_rdy[2][2] = Switch_Unit_in_rdy[2][2];


generate
  for(k=0; k<3; k=k+1) begin

      vc_Queue
    #(
      .p_type(p_type),
      .p_msg_nbits(p_msg_nbits),
      .p_num_msgs(p_num_msgs)
    )
      Queue0
    (
      .clk(clk),
      .reset(reset),

      .enq_val(istream_val[k]),
      .enq_rdy(istream_rdy[k]),
      .enq_msg(istream_msg[k]),

      .deq_val(out_queue_val[k]),
      .deq_rdy(out_queue_rdy[k]),
      .deq_msg(out_queue_msg[k]),

      .num_free_entries(inq_num_free_entries[k])
    );


      lab4_sys_NetRouterRouteUnit
    #(
      .p_msg_nbits(p_msg_nbits)
    )
      Route_Unit
    (
      .clk(clk),
      .reset(reset),

      // Router id (which router is this in the network?)

      .router_id(router_id),

      // Input stream

      .istream_msg(out_queue_msg[k]),
      .istream_val(out_queue_val[k]),
      .istream_rdy(out_queue_rdy[k]),

      // Output streams

      .ostream_msg(Route_Unit_out_msg[k]),
      .ostream_val(Route_Unit_out_val[k]),
      .ostream_rdy(Route_Unit_out_rdy[k])
    );

      lab4_sys_NetRouterSwitchUnit
    #(
      .p_msg_nbits(p_msg_nbits)
    )
      Switch_Unit
    (
      .clk(clk),
      .reset(reset),

      // Input streams

      .istream_msg(Switch_Unit_in_msg[k]),
      .istream_val(Switch_Unit_in_val[k]),
      .istream_rdy(Switch_Unit_in_rdy[k]),

      // Output stream

      .ostream_msg(ostream_msg[k]),
      .ostream_val(ostream_val[k]),
      .ostream_rdy(ostream_rdy[k])
    );
  end
endgenerate

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

    case ( inq_num_free_entries[0] )
      4: vc_trace.append_str( trace_str, " " );
      3: vc_trace.append_str( trace_str, "." );
      2: vc_trace.append_str( trace_str, ":" );
      1: vc_trace.append_str( trace_str, "*" );
      0: vc_trace.append_str( trace_str, "#" );
    endcase

    case ( inq_num_free_entries[1] )
      4: vc_trace.append_str( trace_str, " " );
      3: vc_trace.append_str( trace_str, "." );
      2: vc_trace.append_str( trace_str, ":" );
      1: vc_trace.append_str( trace_str, "*" );
      0: vc_trace.append_str( trace_str, "#" );
    endcase

    case ( inq_num_free_entries[2] )
      4: vc_trace.append_str( trace_str, " " );
      3: vc_trace.append_str( trace_str, "." );
      2: vc_trace.append_str( trace_str, ":" );
      1: vc_trace.append_str( trace_str, "*" );
      0: vc_trace.append_str( trace_str, "#" );
    endcase

    vc_trace.append_str( trace_str, "|" );

    // Line tracing for switch units

    // sunit0.line_trace( trace_str );
    // sunit1.line_trace( trace_str );
    // sunit2.line_trace( trace_str );

  end
  `VC_TRACE_END

  `endif /* SYNTHESIS */

endmodule

`endif /* NET_ROUTER_V */
