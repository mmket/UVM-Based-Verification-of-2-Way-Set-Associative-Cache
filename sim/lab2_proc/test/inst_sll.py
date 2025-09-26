#=========================================================================
# sll
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
    csrr x1, mngr2proc < 0x80008000
    csrr x2, mngr2proc < 0x00000003
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    sll x3, x1, x2
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 0x00040000
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
  """


def gen_dest_dep_test():
  return [
    gen_rr_dest_dep_test( 5, "sll", 0x00000001, 1, 0x00000002 ),
    gen_rr_dest_dep_test( 4, "sll", 0x00000001, 2, 0x00000004 ),
    gen_rr_dest_dep_test( 3, "sll", 0x00000001, 3, 0x00000008 ),
    gen_rr_dest_dep_test( 2, "sll", 0x00000001, 4, 0x00000010 ),
    gen_rr_dest_dep_test( 1, "sll", 0x00000001, 5, 0x00000020 ),
    gen_rr_dest_dep_test( 0, "sll", 0x00000001, 6, 0x00000040 ),
  ]


#-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src0_dep_test():
  return [
    gen_rr_src0_dep_test( 5, "sll", 0x00000002, 1, 0x00000004 ),
    gen_rr_src0_dep_test( 4, "sll", 0x00000002, 2, 0x00000008 ),
    gen_rr_src0_dep_test( 3, "sll", 0x00000002, 3, 0x00000010 ),
    gen_rr_src0_dep_test( 2, "sll", 0x00000002, 4, 0x00000020 ),
    gen_rr_src0_dep_test( 1, "sll", 0x00000002, 5, 0x00000040 ),
    gen_rr_src0_dep_test( 0, "sll", 0x00000002, 6, 0x00000080 ),
  ]


#-------------------------------------------------------------------------
# gen_src1_dep_test
#-------------------------------------------------------------------------

def gen_src1_dep_test():
  return [
    gen_rr_src1_dep_test( 5, "sll", 0x00000001, 1, 0x00000002 ),
    gen_rr_src1_dep_test( 4, "sll", 0x00000002, 1, 0x00000004 ),
    gen_rr_src1_dep_test( 3, "sll", 0x00000003, 1, 0x00000006 ),
    gen_rr_src1_dep_test( 2, "sll", 0x00000004, 1, 0x00000008 ),
    gen_rr_src1_dep_test( 1, "sll", 0x00000005, 1, 0x0000000a ),
    gen_rr_src1_dep_test( 0, "sll", 0x00000006, 1, 0x0000000c ),
  ]



#-------------------------------------------------------------------------
# gen_srcs_dep_test
#-------------------------------------------------------------------------

def gen_srcs_dep_test():
  return [
    gen_rr_srcs_dep_test( 5, "sll", 0x00000002, 1, 0x00000004 ),
    gen_rr_srcs_dep_test( 4, "sll", 0x00000023, 2, 0x0000008c ),
    gen_rr_srcs_dep_test( 3, "sll", 0x000000a0, 3, 0x00000500 ),
    gen_rr_srcs_dep_test( 2, "sll", 0x00000008, 4, 0x00000080 ),
    gen_rr_srcs_dep_test( 1, "sll", 0x00000003, 5, 0x00000060 ),
    gen_rr_srcs_dep_test( 0, "sll", 0x00000005, 6, 0x00000140 ),
  ]


#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rr_src0_eq_dest_test( "sll", 0x00000001, 1, 0x00000002 ),
    gen_rr_src1_eq_dest_test( "sll", 0x00000001, 1, 0x00000002 ),
    gen_rr_src0_eq_src1_test( "sll", 0x00000001, 0x00000002 ),
    gen_rr_srcs_eq_dest_test( "sll", 0x00000001, 0x00000002 ),
  ]


#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_rr_value_test( "sll", 0x00000001, 0x00000000, 0x00000001 ),
    gen_rr_value_test( "sll", 0x00000001, 0x00000001, 0x00000002 ),
    gen_rr_value_test( "sll", 0x00000001, 0x0000001f, 0x80000000 ),

    gen_rr_value_test( "sll", 0x00000001, 0x00000020, 0x00000001 ),
    gen_rr_value_test( "sll", 0x00000001, 0x00000021, 0x00000002 ),


    gen_rr_value_test( "sll", 0x80000000, 0x00000001, 0x00000000 ),
    gen_rr_value_test( "sll", 0xffffffff, 0x00000004, 0xfffffff0 ),

  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------


def gen_random_test():
  asm_code = []
  for i in range(100):
    src0 = b32( random.randint(0,0xffffffff) )
    src1 = b32( random.randint(0,31) )  
    dest = b32( (src0.uint() << src1[4:0].uint()) & 0xffffffff )
    asm_code.append( gen_rr_value_test( "sll", src0.uint(), src1[4:0].uint(), dest.uint() ) )
  return asm_code
