//========================================================================
// Network Router Switch Unit
//========================================================================

`ifndef LAB4_SYS_NET_ROUTER_SWITCH_UNIT_V
`define LAB4_SYS_NET_ROUTER_SWITCH_UNIT_V

`include "vc/net-msgs.v"
`include "vc/trace.v"

module lab4_sys_NetRouterSwitchUnit
#(
  parameter p_msg_nbits = 44
)
(
  input  logic                   clk,
  input  logic                   reset,

  // Input streams

  input  logic [p_msg_nbits-1:0] istream_msg [3],
  input  logic                   istream_val [3],
  output logic                   istream_rdy [3],

  // Output stream

  output logic [p_msg_nbits-1:0] ostream_msg,
  output logic                   ostream_val,
  input  logic                   ostream_rdy
);

  parameter IDLE = 1'b0, ROUTE = 1'b1;
  integer i;

  logic state;
  logic next_state;
  
  logic [p_msg_nbits-1:0] msg_reg;

  logic [1:0] src;

  // FSM Control
  always_comb begin
    case(state)
      IDLE: next_state = (istream_rdy[0] || istream_rdy[1] || istream_rdy[2]) ? ROUTE : IDLE;
      ROUTE: next_state = (ostream_rdy && ostream_val) ? IDLE : ROUTE;
      default: next_state = IDLE;
    endcase
  end

  always_ff @(posedge clk) begin
    if(reset) state <= IDLE;
    else state <= next_state;
  end

  // Datapath
  always_comb begin
    if(state == IDLE) begin
      if(istream_val[0]) begin
        istream_rdy[0] = 1'b1;

        istream_rdy[1] = 1'b0;
        istream_rdy[2] = 1'b0;
      end
      else if(istream_val[1]) begin
        istream_rdy[1] = 1'b1;

        istream_rdy[0] = 1'b0;
        istream_rdy[2] = 1'b0;
      end
      else if(istream_val[2]) begin
        istream_rdy[2] = 1'b1;

        istream_rdy[0] = 1'b0;
        istream_rdy[1] = 1'b0;
      end
      else begin
        istream_rdy[0] = 1'b0;
        istream_rdy[1] = 1'b0;
        istream_rdy[2] = 1'b0;
      end
    end
    else begin
      istream_rdy[0] = 1'b0;
      istream_rdy[1] = 1'b0;
      istream_rdy[2] = 1'b0;
    end
  end

  always_ff @(posedge clk) begin
    if(reset) msg_reg <= 0;
    else begin
      case({istream_rdy[2], istream_rdy[1], istream_rdy[0]})
        3'b001: msg_reg <= istream_msg[0];
        3'b010: msg_reg <= istream_msg[1];
        3'b100: msg_reg <= istream_msg[2];
        default: msg_reg <= msg_reg;
      endcase
    end
  end

  always_comb begin
    if(state == ROUTE) begin
      ostream_msg = msg_reg;
      ostream_val = 1'b1;
    end
    else begin
      ostream_msg = 0;
      ostream_val = 1'b0;
    end
  end

  //----------------------------------------------------------------------
  // Line Tracing
  //----------------------------------------------------------------------

  `ifndef SYNTHESIS

  integer num_reqs = 0;

  logic [`VC_TRACE_NBITS-1:0] str;
  `VC_TRACE_BEGIN
  begin

    num_reqs = istream_val[0] + istream_val[1] + istream_val[2];

    case ( num_reqs )
      0: vc_trace.append_str( trace_str, " " );
      1: vc_trace.append_str( trace_str, "." );
      2: vc_trace.append_str( trace_str, ":" );
      3: vc_trace.append_str( trace_str, "#" );
    endcase

  end
  `VC_TRACE_END

  `endif /* SYNTHESIS */

endmodule

`endif /* NET_ROUTER_SWITCH_UNIT_V */
