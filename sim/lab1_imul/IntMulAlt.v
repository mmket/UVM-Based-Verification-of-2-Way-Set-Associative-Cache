//=========================================================================
// Integer Multiplier Variable-Latency Implementation
//=========================================================================

`ifndef LAB1_IMUL_INT_MUL_ALT_V
`define LAB1_IMUL_INT_MUL_ALT_V

`include "vc/trace.v"

//=========================================================================
// Integer Multiplier Variable-Latency Implementation
//=========================================================================

module lab1_imul_IntMulAlt
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

  // ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // Instantiate datapath and control models here and then connect them
  // together.
  // '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

// FSM Control
parameter IDLE = 2'd0, CALC = 2'd1, DONE = 2'd2;
reg [1:0] state, next_state;
reg [5:0] counter;
wire stop;

always @(*) begin
  case(state)
    IDLE: next_state = (istream_val && istream_rdy) ? CALC : IDLE;
    CALC: next_state = stop ? DONE : CALC;
    DONE: next_state = ostream_rdy ? IDLE : DONE;
    default: next_state = IDLE;
  endcase
end

always @(posedge clk or posedge reset) begin
  if(reset) state <= IDLE;
  else state <= next_state;
end

always @(posedge clk or posedge reset) begin
  if(reset) counter <= 6'b0;
  else if(state == CALC) counter <= counter + index;
  else counter <= 6'b0;
end

// Shake Hand
assign istream_rdy = (state == IDLE);

always @(posedge clk or posedge reset) begin
  if(reset) begin
    ostream_msg <= 32'b0;
    ostream_val <= 1'b0;
  end
  else if(state == DONE) begin
    ostream_msg <= ostream_val ? ostream_msg :result_reg[31:0];
    ostream_val <= 1'b1;
  end
  else begin
    ostream_msg <= 32'b0;
    ostream_val <= 1'b0;
  end
end

// Multiplier
reg [5:0] index;
reg signed [31:0] a_reg, b_reg;
reg signed [63:0] result_reg;

always @(posedge clk or posedge reset) begin
  if(reset) b_reg <= 32'b0;
  else if(istream_val && istream_rdy) b_reg <= istream_msg[31:0];
  else if(state == CALC) b_reg <= (b_reg >>> index);
  else b_reg <= b_reg;
end

always @(posedge clk or posedge reset) begin
  if(reset) a_reg <= 32'b0;
  else if(istream_val && istream_rdy) a_reg <= istream_msg[63:32];
  else if(state == CALC) a_reg <= (a_reg <<< index);
  else a_reg <= a_reg;
end

always @(posedge clk or posedge reset) begin
  if(reset) result_reg <= 63'b0;
  else if(state == CALC) result_reg <= b_reg[0] ? (result_reg + a_reg) : result_reg;
  else result_reg <= 63'b0;
end


// Look Up Table
always @(*) begin
    casez(b_reg)
        32'b??????????????????????????????1?: index = 6'd1;
        32'b?????????????????????????????10?: index = 6'd2;
        32'b????????????????????????????100?: index = 6'd3;
        32'b???????????????????????????1000?: index = 6'd4;
        32'b??????????????????????????10000?: index = 6'd5;
        32'b?????????????????????????100000?: index = 6'd6;
        32'b????????????????????????1000000?: index = 6'd7;
        32'b???????????????????????10000000?: index = 6'd8;
        32'b??????????????????????100000000?: index = 6'd9;
        32'b?????????????????????1000000000?: index = 6'd10;
        32'b????????????????????10000000000?: index = 6'd11;
        32'b???????????????????100000000000?: index = 6'd12;
        32'b??????????????????1000000000000?: index = 6'd13;
        32'b?????????????????10000000000000?: index = 6'd14;
        32'b????????????????100000000000000?: index = 6'd15;
        32'b???????????????1000000000000000?: index = 6'd16;
        32'b??????????????10000000000000000?: index = 6'd17;
        32'b?????????????100000000000000000?: index = 6'd18;
        32'b????????????1000000000000000000?: index = 6'd19;
        32'b???????????10000000000000000000?: index = 6'd20;
        32'b??????????100000000000000000000?: index = 6'd21;
        32'b?????????1000000000000000000000?: index = 6'd22;
        32'b????????10000000000000000000000?: index = 6'd23;
        32'b???????100000000000000000000000?: index = 6'd24;
        32'b??????1000000000000000000000000?: index = 6'd25;
        32'b?????10000000000000000000000000?: index = 6'd26;
        32'b????100000000000000000000000000?: index = 6'd27;
        32'b???1000000000000000000000000000?: index = 6'd28;
        32'b??10000000000000000000000000000?: index = 6'd29;
        32'b?100000000000000000000000000000?: index = 6'd30;
        32'b1000000000000000000000000000000?: index = 6'd31;
        32'b0000000000000000000000000000000?: index = 6'd32;
        default: index = 6'd0;
    endcase
end

assign stop = ((index + counter) >= 6'd32);


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

`endif /* LAB1_IMUL_INT_MUL_ALT_V */

