# Questa/ModelSim example script (adjust UVM paths for your installation)
# Usage: vsim -do run_questa.do   (from this directory, or edit paths)
#
# set UVM_HOME to your UVM installation root (contains src/uvm_pkg.sv)

transcript on
if {[info exists env(UVM_HOME)]} {
  set UVM_HOME $env(UVM_HOME)
} else {
  echo "Set env UVM_HOME to your UVM tree (with src/uvm_pkg.sv)"
  exit -f
}

vlib work
vlog -sv +incdir+$UVM_HOME/src +define+UVM_NO_DEPRECATED $UVM_HOME/src/uvm_pkg.sv
# Optional: enable covergroup collection (Questa): -cover sbcef on vlog, -coverage on vsim
vlog -sv +incdir+../.. -f compile_uvm.f

# Pick test: test_cache_sanity | test_cache_random
vsim -c -sv_seed 1 +UVM_TESTNAME=test_cache_sanity work.tb_top
# Optional: vsim -c -coverage ... work.tb_top  ;  then: coverage save -onexit cov.ucdb
run -all
quit -f
