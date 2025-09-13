#=========================================================================
# ProcFL_rimm_test.py
#=========================================================================
# We group all our test cases into a class so that we can easily reuse
# these test cases in our RTL tests. We can simply inherit from this test
# class, overload the setup_class method, and set the ProcType
# appropriately.

import pytest

from pymtl3 import *
from lab2_proc.test.harness import asm_test, run_test
from lab2_proc.ProcFL import ProcFL

from lab2_proc.test import inst_addi
from lab2_proc.test import inst_ori
from lab2_proc.test import inst_slti
from lab2_proc.test import inst_srai
from lab2_proc.test import inst_slli
from lab2_proc.test import inst_lui
from lab2_proc.test import inst_auipc

#-------------------------------------------------------------------------
# Tests
#-------------------------------------------------------------------------

@pytest.mark.usefixtures("cmdline_opts")
class Tests:

  @classmethod
  def setup_class( cls ):
    cls.ProcType = ProcFL

  #-----------------------------------------------------------------------
  # addi
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_addi.gen_basic_test     ) ,

    # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # Add more rows to the test case table to test more complicated
    # scenarios.
    # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  ])
  def test_addi( s, name, test ):
    run_test( s.ProcType, test, cmdline_opts=s.__class__.cmdline_opts )

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # random stall and delay
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  #-----------------------------------------------------------------------
  # ori
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_ori.gen_basic_test     ) ,
    asm_test( inst_ori.gen_dest_dep_test  ) ,
    asm_test( inst_ori.gen_src_dep_test   ) ,
    asm_test( inst_ori.gen_srcs_dest_test ) ,
    asm_test( inst_ori.gen_value_test     ) ,
    asm_test( inst_ori.gen_random_test    ) ,
  ])
  def test_ori( s, name, test ):
    run_test( s.ProcType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_ori_delays( s ):
    run_test( s.ProcType, inst_ori.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )

  #-----------------------------------------------------------------------
  # slti
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_slti.gen_basic_test     ) ,

    # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # Add more rows to the test case table to test more complicated
    # scenarios.
    # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  ])
  def test_slti( s, name, test ):
    run_test( s.ProcType, test, cmdline_opts=s.__class__.cmdline_opts )

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # random stall and delay
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


  #-----------------------------------------------------------------------
  # srai
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_srai.gen_basic_test     ) ,

    # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # Add more rows to the test case table to test more complicated
    # scenarios.
    # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  ])
  def test_srai( s, name, test ):
    run_test( s.ProcType, test, cmdline_opts=s.__class__.cmdline_opts )

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # random stall and delay
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  #-----------------------------------------------------------------------
  # slli
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_slli.gen_basic_test     ) ,

    # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # Add more rows to the test case table to test more complicated
    # scenarios.
    # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  ])
  def test_slli( s, name, test ):
    run_test( s.ProcType, test, cmdline_opts=s.__class__.cmdline_opts )

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # random stall and delay
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  #-----------------------------------------------------------------------
  # lui
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_lui.gen_basic_test    ) ,

    # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # Add more rows to the test case table to test more complicated
    # scenarios.
    # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  ])
  def test_lui( s, name, test ):
    run_test( s.ProcType, test, cmdline_opts=s.__class__.cmdline_opts )

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # random stall and delay
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  #-----------------------------------------------------------------------
  # auipc
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_auipc.gen_basic_test    ) ,

    # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # Add more rows to the test case table to test more complicated
    # scenarios.
    # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  ])
  def test_auipc( s, name, test ):
    run_test( s.ProcType, test, cmdline_opts=s.__class__.cmdline_opts )

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # random stall and delay
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

