//=========================================================================
// Bind coverage + SVA to lab3_mem_CacheAlt -> ctrl.state_reg (FSM)
// Compile after lab3_mem/CacheAlt.v
//=========================================================================
`ifndef CACHE_ALT_CTRL_BIND_SV
`define CACHE_ALT_CTRL_BIND_SV

module cache_alt_ctrl_bind_props (
  input logic        clk,
  input logic        reset,
  input logic [4:0]  state
);

  localparam logic [4:0] ST_IDLE              = 5'd0;
  localparam logic [4:0] ST_TAG_CHECK         = 5'd1;
  localparam logic [4:0] ST_INIT_DATA_ACCESS  = 5'd2;
  localparam logic [4:0] ST_READ_DATA_ACCESS  = 5'd3;
  localparam logic [4:0] ST_WRITE_DATA_ACCESS = 5'd4;
  localparam logic [4:0] ST_REFILL_REQUEST    = 5'd5;
  localparam logic [4:0] ST_REFILL_WAIT       = 5'd6;
  localparam logic [4:0] ST_REFILL_UPDATE     = 5'd7;
  localparam logic [4:0] ST_EVICT_PREPARE     = 5'd8;
  localparam logic [4:0] ST_EVICT_REQUEST     = 5'd9;
  localparam logic [4:0] ST_EVICT_WAIT        = 5'd10;
  localparam logic [4:0] ST_WAIT              = 5'd11;

  //----------------------------------------------------------------------
  // Covergroup: per-state + key FSM arcs (matches CacheAltCtrl)
  //----------------------------------------------------------------------
  covergroup cg_cache_ctrl_fsm @(posedge clk iff !reset);
    option.per_instance = 1;
    option.name = "cg_cache_ctrl_fsm";

    cp_state: coverpoint state {
      bins s_idle  = {ST_IDLE};
      bins s_tag   = {ST_TAG_CHECK};
      bins s_init  = {ST_INIT_DATA_ACCESS};
      bins s_rdda  = {ST_READ_DATA_ACCESS};
      bins s_wrda  = {ST_WRITE_DATA_ACCESS};
      bins s_rrq   = {ST_REFILL_REQUEST};
      bins s_rrw   = {ST_REFILL_WAIT};
      bins s_rru   = {ST_REFILL_UPDATE};
      bins s_epr   = {ST_EVICT_PREPARE};
      bins s_erq   = {ST_EVICT_REQUEST};
      bins s_ewt   = {ST_EVICT_WAIT};
      bins s_wait  = {ST_WAIT};
      illegal_bins ill = {[12:31]};
    }

    cp_arc: coverpoint state {
      bins idle_to_tag            = (ST_IDLE              => ST_TAG_CHECK);
      bins tag_to_rd_hit          = (ST_TAG_CHECK         => ST_READ_DATA_ACCESS);
      bins tag_to_wr_hit          = (ST_TAG_CHECK         => ST_WRITE_DATA_ACCESS);
      bins tag_to_init            = (ST_TAG_CHECK         => ST_INIT_DATA_ACCESS);
      bins tag_to_evict_prep      = (ST_TAG_CHECK         => ST_EVICT_PREPARE);
      bins tag_to_refill_req      = (ST_TAG_CHECK         => ST_REFILL_REQUEST);
      bins evict_prep_to_req      = (ST_EVICT_PREPARE     => ST_EVICT_REQUEST);
      bins evict_req_to_wait      = (ST_EVICT_REQUEST     => ST_EVICT_WAIT);
      bins evict_wait_to_refill   = (ST_EVICT_WAIT        => ST_REFILL_REQUEST);
      bins refill_req_to_wait     = (ST_REFILL_REQUEST    => ST_REFILL_WAIT);
      bins refill_wait_to_update  = (ST_REFILL_WAIT       => ST_REFILL_UPDATE);
      bins refill_upd_to_rdda     = (ST_REFILL_UPDATE     => ST_READ_DATA_ACCESS);
      bins refill_upd_to_wrda     = (ST_REFILL_UPDATE     => ST_WRITE_DATA_ACCESS);
      bins init_to_wait           = (ST_INIT_DATA_ACCESS  => ST_WAIT);
      bins rdda_to_wait           = (ST_READ_DATA_ACCESS  => ST_WAIT);
      bins wrda_to_wait           = (ST_WRITE_DATA_ACCESS => ST_WAIT);
      bins wait_to_idle           = (ST_WAIT              => ST_IDLE);
    }
  endgroup

  cg_cache_ctrl_fsm cg_inst;

  initial begin
    cg_inst = new();
  end

  //----------------------------------------------------------------------
  // SVA: only legal FSM encodings (12 states); disabled during reset
  //----------------------------------------------------------------------
  property p_state_legal;
    @(posedge clk) disable iff (reset)
      (state <= ST_WAIT);
  endproperty

  a_state_legal: assert property (p_state_legal)
    else $error("[cache_alt_ctrl_bind] FSM state out of legal range: %0d", state);

  c_state_legal: cover property (p_state_legal);

endmodule

bind lab3_mem_CacheAlt cache_alt_ctrl_bind_props u_cache_alt_ctrl_bind (
  .clk   (clk),
  .reset (reset),
  .state (ctrl.state_reg)
);

`endif
