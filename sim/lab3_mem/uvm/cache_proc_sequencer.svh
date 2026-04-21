`ifndef CACHE_PROC_SEQUENCER_SVH
`define CACHE_PROC_SEQUENCER_SVH

class cache_proc_sequencer extends uvm_sequencer #(cache_proc_req_item);
  `uvm_component_utils(cache_proc_sequencer)
  function new(string name, uvm_component parent);
    super.new(name, parent);
  endfunction
endclass

`endif
