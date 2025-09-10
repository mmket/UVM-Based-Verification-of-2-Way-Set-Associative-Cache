#=========================================================================
# imul_sim_test
#=========================================================================
# Make sure that imul-sim works.

import pytest
import os

from subprocess import check_call, CalledProcessError
from itertools  import product

impls  = [ "fl", "base", "alt"]
inputs = [ "small", "small_pos_pos_msgs", "zero_one_neg_msgs", "small_neg_pos_msgs",
    "small_pos_neg_msgs", "small_neg_neg_msgs", "large_pos_pos_msgs", "large_pos_neg_msgs",
    "large_neg_pos_msgs", "large_neg_neg_msgs", "low_bit_masked_msgs", "middle_bit_masked_msgs",
    "sparse_number_msgs", "dense_number_msgs", "trigger_corner_cases_msgs"]

test_cases = []
for input_ in inputs:
  for impl in impls:
    test_cases.append([ impl, input_ ])

@pytest.mark.parametrize( "impl,input_", test_cases )
def test( impl, input_, cmdline_opts ):

  # Get path to simulator script

  test_dir = os.path.dirname( os.path.abspath( __file__ ) )
  sim_dir  = os.path.dirname( test_dir )
  sim      = sim_dir + os.path.sep + 'imul-sim'

  # Command

  cmd = [ sim, "--impl", impl, "--input", input_ ]

  # Handle test verilog

  if cmdline_opts['test_verilog']:
    if impl.startswith("rtl"):
      cmd.append( "--translate" )
    else:
      pytest.skip("ignoring non-Verilog tests")

    if cmdline_opts['dump_vcd']:
      cmd.append( "--dump-vcd" )

  # Display simulator command line

  print("")
  print("Simulator command line:", ' '.join(cmd))

  # Run the simulator

  try:
    check_call(cmd)
  except CalledProcessError as e:
    raise Exception( "Error running simulator!" )

