#=========================================================================
# ProcFL_jump_test.py
#=========================================================================
# We group all our test cases into a class so that we can easily reuse
# these test cases in our RTL tests. We can simply inherit from this test
# class, overload the setup_class method, and set the ProcType
# appropriately.

import pytest

from pymtl3 import *
from lab2_proc.test.harness import asm_test, run_test
from lab2_proc.ProcFL import ProcFL

from lab2_proc.test import inst_jal
from lab2_proc.test import inst_jalr
from lab2_proc.test import inst_mix 

#-------------------------------------------------------------------------
# Tests
#-------------------------------------------------------------------------

@pytest.mark.usefixtures("cmdline_opts")
class Tests:

  @classmethod
  def setup_class( cls ):
    cls.ProcType = ProcFL

  #-----------------------------------------------------------------------
  # jal
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_jal.gen_basic_test        ) ,
    asm_test( inst_jal.gen_multijump_test       ) ,
    asm_test( inst_jal.gen_data_test       ) ,
    asm_test( inst_jal.gen_back_to_back_test      ) ,
    asm_test( inst_jal.gen_random_test      ) , 
  ])

  def test_jal( s, name, test ):
    run_test( s.ProcType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_jal_delays( s ):
    run_test( s.ProcType, inst_jal.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )
  #-----------------------------------------------------------------------
  # jalr
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_jalr.gen_basic_test    ),
    asm_test( inst_jalr.gen_data_test    ),
    asm_test( inst_jalr.gen_multijump_test    ),
    asm_test( inst_jalr.gen_back_to_back_test      ) ,
    asm_test( inst_jalr.gen_random_test      ) , 
  ])

  def test_jalr( s, name, test ):
    run_test( s.ProcType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_jalr_delays( s ):
    run_test( s.ProcType, inst_jalr.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )
    
    
  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_mix.gen_branch_1    ),
    asm_test( inst_mix.gen_branch_2    ),
    asm_test( inst_mix.gen_branch_3    ),
    asm_test( inst_mix.gen_branch_4    ),
    asm_test( inst_mix.gen_branch_5    ),
    asm_test( inst_mix.gen_branch_6    ),
    asm_test( inst_mix.gen_branch_7    ),
    asm_test( inst_mix.gen_jal_stall    ),
  ])

  def test_mix( s, name, test ):
    run_test( s.ProcType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_mix_delays( s ):
    run_test( s.ProcType, inst_jalr.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )