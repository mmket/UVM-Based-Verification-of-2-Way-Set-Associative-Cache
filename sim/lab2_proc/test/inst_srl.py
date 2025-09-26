#=========================================================================
# srl
#=========================================================================

import random

# Fix the random seed so results are reproducible
random.seed(0xdeadbeef)

from pymtl3 import *
from lab2_proc.test.inst_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """
    csrr x1, mngr2proc < 0x00008000
    csrr x2, mngr2proc < 0x00000003
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    srl x3, x1, x2
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 0x00001000
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
  """

#-------------------------------------------------------------------------
# gen_dest_dep_test
#-------------------------------------------------------------------------

def gen_dest_dep_test():
  return [
    gen_rr_dest_dep_test( 5, "srl", 0x00000010, 1, 0x00000008 ), 
    gen_rr_dest_dep_test( 4, "srl", 0x00000010, 2, 0x00000004 ), 
    gen_rr_dest_dep_test( 3, "srl", 0x80000000, 1, 0x40000000 ), 
    gen_rr_dest_dep_test( 2, "srl", 0xffffffff, 1, 0x7fffffff ), 
    gen_rr_dest_dep_test( 1, "srl", 0x00000001, 1, 0x00000000 ), 
    gen_rr_dest_dep_test( 0, "srl", 0xffffffff, 31, 0x00000001 ),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src0_dep_test():
  return [
    gen_rr_src0_dep_test( 5, "srl", 0x00000020, 1, 0x00000010 ),
    gen_rr_src0_dep_test( 4, "srl", 0x00000020, 2, 0x00000008 ),
    gen_rr_src0_dep_test( 3, "srl", 0x80000000, 1, 0x40000000 ),
    gen_rr_src0_dep_test( 2, "srl", 0xffffffff, 1, 0x7fffffff ),
    gen_rr_src0_dep_test( 1, "srl", 0x00000001, 1, 0x00000000 ),
    gen_rr_src0_dep_test( 0, "srl", 0xffffffff, 31, 0x00000001 ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_test
#-------------------------------------------------------------------------

def gen_src1_dep_test():
  return [
    gen_rr_src1_dep_test( 5, "srl", 0x00000010, 1, 0x00000008 ),
    gen_rr_src1_dep_test( 4, "srl", 0x00000010, 2, 0x00000004 ),
    gen_rr_src1_dep_test( 3, "srl", 0x80000000, 1, 0x40000000 ),
    gen_rr_src1_dep_test( 2, "srl", 0xffffffff, 1, 0x7fffffff ),
    gen_rr_src1_dep_test( 1, "srl", 0x00000001, 1, 0x00000000 ),
    gen_rr_src1_dep_test( 0, "srl", 0xffffffff, 31, 0x00000001 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_test
#-------------------------------------------------------------------------

def gen_srcs_dep_test():
  return [
    gen_rr_srcs_dep_test( 5, "srl", 0x00000020, 1, 0x00000010 ),
    gen_rr_srcs_dep_test( 4, "srl", 0x00000020, 2, 0x00000008 ),
    gen_rr_srcs_dep_test( 3, "srl", 0x80000000, 1, 0x40000000 ),
    gen_rr_srcs_dep_test( 2, "srl", 0xffffffff, 1, 0x7fffffff ),
    gen_rr_srcs_dep_test( 1, "srl", 0x00000001, 1, 0x00000000 ),
    gen_rr_srcs_dep_test( 0, "srl", 0xffffffff, 31, 0x00000001 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
# gen_srcs_dest_test (fixed for srl)
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rr_src0_eq_dest_test( "srl", 0x00000010, 1, 0x00000008 ),

    gen_rr_src1_eq_dest_test( "srl", 0x80000000, 1, 0x40000000 ),

    gen_rr_src0_eq_src1_test( "srl", 0x80000000, 0x80000000 ),

    gen_rr_srcs_eq_dest_test( "srl", 0xffffffff, 0x00000001 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_rr_value_test( "srl", 0x00000010, 1, 0x00000008 ),
    gen_rr_value_test( "srl", 0x00000010, 4, 0x00000001 ),

    gen_rr_value_test( "srl", 0xffffffff, 1, 0x7fffffff ),
    gen_rr_value_test( "srl", 0xffffffff, 31, 0x00000001 ),

    gen_rr_value_test( "srl", 0x80000000, 1, 0x40000000 ),
    gen_rr_value_test( "srl", 0x80000000, 31, 0x00000001 ),

    gen_rr_value_test( "srl", 0x00000010, 32, 0x00000010 ), 
    gen_rr_value_test( "srl", 0x00000010, 33, 0x00000008 ), 
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in range(100):
    src0 = b32( random.randint(0,0xffffffff) )
    src1 = random.randint(0,31)  
    dest = b32( src0.uint() >> src1 )
    asm_code.append( gen_rr_value_test( "srl", src0.uint(), src1, dest.uint() ) )
  return asm_code