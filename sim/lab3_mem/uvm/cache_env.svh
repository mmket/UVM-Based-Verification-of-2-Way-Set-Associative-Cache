`ifndef CACHE_ENV_SVH
`define CACHE_ENV_SVH

class cache_env extends uvm_component;
  `uvm_component_utils(cache_env)

  cache_proc_agent   proc_agent;
  cache_mem_agent    mem_agent;
  cache_scoreboard   sb;

  function new(string name, uvm_component parent);
    super.new(name, parent);
  endfunction

  function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    proc_agent = cache_proc_agent::type_id::create("proc_agent", this);
    mem_agent  = cache_mem_agent::type_id::create("mem_agent", this);
    sb         = cache_scoreboard::type_id::create("sb", this);
  endfunction
endclass

`endif
