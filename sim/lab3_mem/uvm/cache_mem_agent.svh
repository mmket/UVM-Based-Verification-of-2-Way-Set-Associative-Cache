`ifndef CACHE_MEM_AGENT_SVH
`define CACHE_MEM_AGENT_SVH

class cache_mem_agent extends uvm_component;
  `uvm_component_utils(cache_mem_agent)

  cache_mem_slave   slv;
  cache_mem_monitor mon;

  uvm_analysis_port #(cache_evt_mem_req) ap_req;
  uvm_analysis_port #(cache_evt_mem_rsp) ap_rsp;

  function new(string name, uvm_component parent);
    super.new(name, parent);
  endfunction

  function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    slv = cache_mem_slave::type_id::create("slv", this);
    mon = cache_mem_monitor::type_id::create("mon", this);
    ap_req = new("ap_req", this);
    ap_rsp = new("ap_rsp", this);
  endfunction

  function void connect_phase(uvm_phase phase);
    super.connect_phase(phase);
    mon.ap_req.connect(ap_req);
    mon.ap_rsp.connect(ap_rsp);
  endfunction
endclass

`endif
