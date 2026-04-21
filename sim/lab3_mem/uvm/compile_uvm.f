// Compile from directory: lab-group36/sim/lab3_mem/uvm
// Simulator: Questa/ModelSim/VCS (adjust UVM invocation for your tool)
//
// +incdir+ must point at sim/ (parent of vc/ and lab3_mem/) so includes like
// "vc/mem-msgs.v" and "lab3_mem/CacheAltCtrl.v" resolve for CacheAlt.v
//
+incdir+../..
../../vc/mem-msgs.v
cache_proc_if.sv
cache_mem_if.sv
cache_uvm_pkg.sv
../CacheAlt.v
cache_alt_ctrl_bind.sv
cache_sva_assertion_writer.sv
tb_top.sv
