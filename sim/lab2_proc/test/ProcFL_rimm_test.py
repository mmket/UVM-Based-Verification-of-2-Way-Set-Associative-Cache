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
from lab2_proc.test import inst_beq

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
    asm_test( inst_addi.gen_dest_dep_test    ) ,
    asm_test( inst_addi.gen_src_dep_test     ) ,
    asm_test( inst_addi.gen_src_eq_dest_test     ) ,
    asm_test( inst_addi.gen_value_test     ) ,
    asm_test( inst_addi.gen_random_test     ) ,
    asm_test( inst_addi.gen_src_dep_test     ) ,  
    asm_test( inst_addi.gen_src_imm_dep_test    ) ,
  ])
  def test_addi( s, name, test ):
    run_test( s.ProcType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_addi_delays( s ):
    run_test( s.ProcType, inst_addi.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )
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
    asm_test( inst_addi.gen_src_dep_test     ) ,
    asm_test( inst_addi.gen_src_eq_dest_test     ) ,
    asm_test( inst_addi.gen_value_test     ) ,
    asm_test( inst_addi.gen_random_test     ) ,
    asm_test( inst_addi.gen_dest_dep_test     ) ,  
  ])
  def test_slti( s, name, test ):
    run_test( s.ProcType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_slti_delays( s ):
    run_test( s.ProcType, inst_slti.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )

  #-----------------------------------------------------------------------
  # srai
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_srai.gen_basic_test     ) ,
    asm_test( inst_addi.gen_src_dep_test     ) ,
    asm_test( inst_addi.gen_src_eq_dest_test     ) ,
    asm_test( inst_addi.gen_value_test     ) ,
    asm_test( inst_addi.gen_random_test     ) ,
    asm_test( inst_addi.gen_src_dep_test     ) ,  
    asm_test( inst_addi.gen_src_imm_dep_test    ) ,
  ])
  def test_srai( s, name, test ):
    run_test( s.ProcType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_srai_delays( s ):
    run_test( s.ProcType, inst_srai.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )
  #-----------------------------------------------------------------------
  # slli
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_slli.gen_basic_test     ) ,
    asm_test( inst_slli.gen_dest_dep_test     ) ,
    asm_test( inst_slli.gen_src_dep_test     ) ,
    asm_test( inst_slli.gen_src_eq_dest_test     ) ,
    asm_test( inst_slli.gen_value_test     ) ,
    asm_test( inst_slli.gen_random_test     ) ,
    asm_test( inst_slli.gen_src_dep_test     ) ,  
    asm_test( inst_slli.gen_src_imm_dep_test    ) ,
  ])
  def test_slli( s, name, test ):
    run_test( s.ProcType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_slli_delays( s ):
    run_test( s.ProcType, inst_slli.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )
  #-----------------------------------------------------------------------
  # lui
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_lui.gen_basic_test    ) ,
    asm_test( inst_lui.gen_value_test   ) ,
    asm_test( inst_lui.gen_random_test   ) ,
    asm_test( inst_lui.gen_basic_a_test   ) ,
    asm_test( inst_lui.gen_basic_b_test  ) ,
    asm_test( inst_lui.gen_basic_c_test   ) ,
    asm_test( inst_lui.gen_src_dep_test  ) ,
  ])
  def test_lui( s, name, test ):
    run_test( s.ProcType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_lui_delays( s ):
    run_test( s.ProcType, inst_lui.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )
  #-----------------------------------------------------------------------
  # auipc
  #-----------------------------------------------------------------------

  @pytest.mark.parametrize( "name,test", [
    asm_test( inst_auipc.gen_basic_test    ) ,
    asm_test( inst_auipc.gen_dest_dep_a_test    ),
    asm_test( inst_auipc.gen_dest_dep_b_test    ),
    asm_test( inst_auipc.gen_dest_dep_c_test    ),
    asm_test( inst_auipc.gen_dest_dep_d_test    ),
    asm_test( inst_auipc.gen_dest_dep_e_test    ),
    asm_test( inst_auipc.gen_dest_dep_f_test    ),
    asm_test( inst_auipc.gen_src_dep_a_test    ),
    asm_test( inst_auipc.gen_src_dep_b_test    ),
    asm_test( inst_auipc.gen_src_dep_c_test    ),
    asm_test( inst_auipc.gen_src_dep_d_test    ),
    asm_test( inst_auipc.gen_src_dep_e_test    ),
    asm_test( inst_auipc.gen_src_dep_f_test    ),
    asm_test( inst_auipc.gen_value_test    ),
    asm_test( inst_auipc.gen_random_test    ),
  ])
  def test_auipc( s, name, test ):
    run_test( s.ProcType, test, cmdline_opts=s.__class__.cmdline_opts )

  def test_auipc_delays( s ):
    run_test( s.ProcType, inst_auipc.gen_random_test, delays=True,
              cmdline_opts=s.__class__.cmdline_opts )