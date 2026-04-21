`ifndef CACHE_MEM_MONITOR_SVH
`define CACHE_MEM_MONITOR_SVH

// Optional: transaction logging / coverage hook (not required for scoreboard)
class cache_mem_monitor extends uvm_component;
  `uvm_component_utils(cache_mem_monitor)
  virtual cache_mem_if vif;
  uvm_analysis_port #(cache_evt_mem_req) ap_req;
  uvm_analysis_port #(cache_evt_mem_rsp) ap_rsp;

  function new(string name, uvm_component parent);
    super.new(name, parent);
    ap_req = new("ap_req", this);
    ap_rsp = new("ap_rsp", this);
  endfunction

  function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    if (!uvm_config_db#(virtual cache_mem_if)::get(this, "", "vif", vif))
      `uvm_fatal("NOVIF", "cache_mem_if not set for mem monitor")
  endfunction

  task run_phase(uvm_phase phase);
    forever @(posedge vif.clk) begin
      if (vif.reset) continue;
      if (vif.req_val && vif.req_rdy) begin
        cache_evt_mem_req e;
        e = cache_evt_mem_req::type_id::create("e");
        unpack_mem_req_16B(vif.req_msg, e.type_, e.opaque, e.addr, e.len, e.data);
        ap_req.write(e);
      end
      if (vif.resp_val && vif.resp_rdy) begin
        cache_evt_mem_rsp r;
        r = cache_evt_mem_rsp::type_id::create("r");
        unpack_mem_resp_16B(vif.resp_msg, r.type_, r.opaque, r.test, r.len, r.data);
        ap_rsp.write(r);
      end
    end
  endtask
endclass

`endif
