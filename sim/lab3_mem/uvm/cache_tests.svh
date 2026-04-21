`ifndef CACHE_TESTS_SVH
`define CACHE_TESTS_SVH

class cache_base_test extends uvm_test;
  `uvm_component_utils(cache_base_test)
  cache_env env;

  function new(string name, uvm_component parent);
    super.new(name, parent);
  endfunction

  function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    env = cache_env::type_id::create("env", this);
  endfunction

  function void end_of_elaboration_phase(uvm_phase phase);
    super.end_of_elaboration_phase(phase);
    uvm_top.print_topology();
  endfunction
endclass

class test_cache_sanity extends cache_base_test;
  `uvm_component_utils(test_cache_sanity)

  function new(string name, uvm_component parent);
    super.new(name, parent);
  endfunction

  task run_phase(uvm_phase phase);
    cache_sanity_seq seq;
    phase.raise_objection(this);
    seq = cache_sanity_seq::type_id::create("seq");
    seq.start(env.proc_agent.sqr);
    phase.drop_objection(this);
  endtask
endclass

class test_cache_random extends cache_base_test;
  `uvm_component_utils(test_cache_random)

  function new(string name, uvm_component parent);
    super.new(name, parent);
  endfunction

  task run_phase(uvm_phase phase);
    cache_random_seq seq;
    phase.raise_objection(this);
    seq = cache_random_seq::type_id::create("seq");
    seq.start(env.proc_agent.sqr);
    phase.drop_objection(this);
  endtask
endclass

`endif
