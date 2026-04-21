//=========================================================================
// UVM package: lab3 CacheAlt verification environment
//=========================================================================

`ifndef CACHE_UVM_PKG_SV
`define CACHE_UVM_PKG_SV

package cache_uvm_pkg;
  import uvm_pkg::*;

  `include "cache_bit_pack.svh"
  `include "cache_constants.svh"
  `include "cache_evt.svh"
  `include "cache_proc_seq_item.svh"
  `include "cache_proc_driver.svh"
  `include "cache_proc_monitor.svh"
  `include "cache_proc_sequencer.svh"
  `include "cache_proc_agent.svh"
  `include "cache_mem_slave.svh"
  `include "cache_mem_monitor.svh"
  `include "cache_mem_agent.svh"
  `include "cache_scoreboard.svh"
  `include "cache_env.svh"
  `include "cache_sequences.svh"
  `include "cache_tests.svh"
endpackage

`endif
