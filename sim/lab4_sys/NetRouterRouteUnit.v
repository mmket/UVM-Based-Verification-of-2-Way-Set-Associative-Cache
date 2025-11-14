//========================================================================
// Network Router Route Unit
//========================================================================

`ifndef LAB4_SYS_NET_ROUTER_ROUTE_UNIT_V
`define LAB4_SYS_NET_ROUTER_ROUTE_UNIT_V

`include "vc/net-msgs.v"
`include "vc/trace.v"


module lab4_sys_NetRouterRouteUnit
#(
  parameter p_msg_nbits = 44
)
(
  input  logic                   clk,
  input  logic                   reset,

  // Router id (which router is this in the network?)

  input  logic [1:0]             router_id,

  // Input stream

  input  logic [p_msg_nbits-1:0] istream_msg,
  input  logic                   istream_val,
  output logic                   istream_rdy,

  // Output streams

  output logic [p_msg_nbits-1:0] ostream_msg [3],
  output logic                   ostream_val [3],
  input  logic                   ostream_rdy [3]
);

  net_msg_hdr_t istream_msg_hdr;
  assign istream_msg_hdr = istream_msg[`VC_NET_MSGS_HDR(p_msg_nbits)];

  parameter IDLE = 1'b0, ROUTE = 1'b1;
  integer i;

  logic state;
  logic next_state;
  
  logic [1:0] destination;
  logic [p_msg_nbits-1:0] msg_reg;

  // FSM Control
  always_comb begin
    case(state)
      IDLE: next_state = (istream_rdy && istream_val) ? ROUTE : IDLE;
      ROUTE: next_state = ((ostream_rdy[0] && ostream_val[0]) 
                        || (ostream_rdy[1] && ostream_val[1]) 
                        || (ostream_rdy[2] && ostream_val[2])) ? IDLE : ROUTE;
      default: next_state = IDLE;
    endcase
  end

  always_ff @(posedge clk) begin
    if(reset) state <= IDLE;
    else state <= next_state;
  end

  // Datapath
  assign istream_rdy = (state == IDLE);

  always_ff @(posedge clk) begin
    if(reset) begin
      msg_reg <= 0;
      destination <= 2'b0;
    end
    else if(istream_rdy && istream_val) begin
      msg_reg <= istream_msg;
      destination <= istream_msg_hdr.dest;
    end
  end

  always_comb begin
    if(state == ROUTE) begin
      if(destination == router_id) begin    // I am the dest
        ostream_msg[1] = msg_reg;
        ostream_val[1] = 1'b1;

        ostream_msg[0] = 0;
        ostream_val[0] = 1'b0;
        ostream_msg[2] = 0;
        ostream_val[2] = 1'b0;
      end
      else if(destination == router_id - 2'd1) begin   // going left
        ostream_msg[0] = msg_reg;
        ostream_val[0] = 1'b1;

        ostream_msg[1] = 0;
        ostream_val[1] = 1'b0;
        ostream_msg[2] = 0;
        ostream_val[2] = 1'b0;
      end
      else begin                    // going right
        ostream_msg[2] = msg_reg;
        ostream_val[2] = 1'b1;

        ostream_msg[0] = 0;
        ostream_val[0] = 1'b0;
        ostream_msg[1] = 0;
        ostream_val[1] = 1'b0;
      end
    end
    else begin
      for(i=0; i<3; i=i+1) begin
        ostream_msg[i] = 0;
        ostream_val[i] = 1'b0;
      end
    end
  end

  //----------------------------------------------------------------------
  // Line Tracing
  //----------------------------------------------------------------------

  `ifndef SYNTHESIS

  logic [`VC_TRACE_NBITS-1:0] str;
  `VC_TRACE_BEGIN
  begin

    if ( istream_val && istream_rdy ) begin
      $sformat( str, "%d", istream_msg_hdr.dest );
      vc_trace.append_str( trace_str, str );
    end
    else
      vc_trace.append_str( trace_str, " " );

  end
  `VC_TRACE_END

  `endif /* SYNTHESIS */

endmodule

`endif /* NET_ROUTER_ROUTE_UNIT_V */
