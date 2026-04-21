`ifndef CACHE_PROC_MONITOR_SVH
`define CACHE_PROC_MONITOR_SVH

class cache_proc_monitor extends uvm_component;
  `uvm_component_utils(cache_proc_monitor)
  virtual cache_proc_if vif;
  uvm_analysis_port #(cache_evt_cpu_req) ap_req;
  uvm_analysis_port #(cache_evt_cpu_rsp) ap_rsp;

  function new(string name, uvm_component parent);
    super.new(name, parent);
    ap_req = new("ap_req", this);
    ap_rsp = new("ap_rsp", this);
  endfunction

  function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    if (!uvm_config_db#(virtual cache_proc_if)::get(this, "", "vif", vif))
      `uvm_fatal("NOVIF", "cache_proc_if not set for proc monitor")
  endfunction

  task run_phase(uvm_phase phase);
    forever @(posedge vif.clk) begin
      if (vif.reset) continue;
      if (vif.req_val && vif.req_rdy) begin
        cache_evt_cpu_req e;
        e = cache_evt_cpu_req::type_id::create("e");
        unpack_mem_req_4B(vif.req_msg, e.type_, e.opaque, e.addr, e.len, e.data);
        ap_req.write(e);
      end
      if (vif.resp_val && vif.resp_rdy) begin
        cache_evt_cpu_rsp r;
        r = cache_evt_cpu_rsp::type_id::create("r");
        unpack_mem_resp_4B(vif.resp_msg, r.type_, r.opaque, r.test, r.len, r.data);
        ap_rsp.write(r);
      end
    end
  endtask
endclass

`endif
