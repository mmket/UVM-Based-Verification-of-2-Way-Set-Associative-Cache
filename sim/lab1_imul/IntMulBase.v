//========================================================================
// Integer Multiplier Fixed-Latency Implementation
//========================================================================

`ifndef LAB1_IMUL_INT_MUL_BASE_V
`define LAB1_IMUL_INT_MUL_BASE_V

`include "vc/trace.v"

//========================================================================
// Integer Multiplier Fixed-Latency Implementation
//========================================================================

module lab1_imul_IntMulBase
(
  input  logic        clk,
  input  logic        reset,

  input  logic        istream_val,
  output logic        istream_rdy,
  input  logic [63:0] istream_msg,

  output logic        ostream_val,
  input  logic        ostream_rdy,
  output logic [31:0] ostream_msg
);

// FSM Control
parameter IDLE = 2'd0, CALC = 2'd1, DONE = 2'd2;
logic [1:0] state, next_state;
logic [5:0] counter;

always_comb begin
  case(state)
    IDLE: next_state = (istream_val && istream_rdy) ? CALC : IDLE;
    CALC: next_state = (counter == 6'd32) ? DONE : CALC;
    DONE: next_state = ostream_rdy ? IDLE : DONE;
    default: next_state = IDLE;
  endcase
end

always_ff @(posedge clk) begin
  if(reset) state <= IDLE;
  else state <= next_state;
end

always_ff @(posedge clk) begin
  if(reset) counter <= 6'b0;
  else if(state == CALC) counter <= counter + 1;
  else counter <= 6'b0;
end

// Shake Hand
assign istream_rdy = (state == IDLE);

always_comb begin
  if(state == DONE) begin
    ostream_msg = result_reg[31:0];
    ostream_val = 1'b1;
  end
  else begin
    ostream_msg = 32'b0;
    ostream_val = 1'b0;
  end
end

// Multiplier
logic [31:0] a_reg, b_reg;
logic [31:0] result_reg;

always_ff @(posedge clk) begin
  if(reset) b_reg <= 32'b0;
  else if(istream_val && istream_rdy) b_reg <= istream_msg[31:0];
  else if(state == CALC) b_reg <= $signed(b_reg >>> 1);
  else b_reg <= b_reg;
end

always_ff @(posedge clk) begin
  if(reset) a_reg <= 32'b0;
  else if(istream_val && istream_rdy) a_reg <= istream_msg[63:32];
  else if(state == CALC) a_reg <= $signed(a_reg <<< 1);
  else a_reg <= a_reg;
end

always_ff @(posedge clk) begin
  if(reset) result_reg <= 31'b0;
  else if(state == IDLE) result_reg <= 31'b0;
  else if(state == CALC) result_reg <= b_reg[0] ? $signed(result_reg + a_reg) : result_reg;
  else result_reg <= result_reg;
end

  //----------------------------------------------------------------------
  // Line Tracing
  //----------------------------------------------------------------------

  `ifndef SYNTHESIS

  logic [`VC_TRACE_NBITS-1:0] str;
  `VC_TRACE_BEGIN
  begin

    $sformat( str, "%x", istream_msg );
    vc_trace.append_val_rdy_str( trace_str, istream_val, istream_rdy, str );

    vc_trace.append_str( trace_str, "(" );

    vc_trace.append_str( trace_str, ")" );

    $sformat( str, "%x", ostream_msg );
    vc_trace.append_val_rdy_str( trace_str, ostream_val, ostream_rdy, str );

  end
  `VC_TRACE_END

  `endif /* SYNTHESIS */

endmodule

`endif /* LAB1_IMUL_INT_MUL_BASE_V */

