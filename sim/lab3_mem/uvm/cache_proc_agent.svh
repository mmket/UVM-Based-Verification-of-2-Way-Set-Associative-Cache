`ifndef CACHE_PROC_AGENT_SVH
`define CACHE_PROC_AGENT_SVH

class cache_proc_agent extends uvm_component;
  `uvm_component_utils(cache_proc_agent)

  cache_proc_driver    drv;
  cache_proc_sequencer sqr;
  cache_proc_monitor   mon;

  uvm_analysis_port #(cache_evt_cpu_req) ap_req;
  uvm_analysis_port #(cache_evt_cpu_rsp) ap_rsp;

  function new(string name, uvm_component parent);
    super.new(name, parent);
  endfunction

  function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    drv = cache_proc_driver::type_id::create("drv", this);
    sqr = cache_proc_sequencer::type_id::create("sqr", this);
    mon = cache_proc_monitor::type_id::create("mon", this);
    ap_req = new("ap_req", this);
    ap_rsp = new("ap_rsp", this);
  endfunction

  function void connect_phase(uvm_phase phase);
    super.connect_phase(phase);
    drv.seq_item_port.connect(sqr.seq_export);
    mon.ap_req.connect(ap_req);
    mon.ap_rsp.connect(ap_rsp);
  endfunction
endclass

`endif
