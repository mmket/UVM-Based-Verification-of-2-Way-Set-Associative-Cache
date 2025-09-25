#=========================================================================
# mul
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
    csrr x1, mngr2proc < 5
    csrr x2, mngr2proc < 4
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    mul x3, x1, x2
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 20
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
  """

# ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Define additional directed and random test cases.
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#-------------------------------------------------------------------------
# gen_dest_dep_test
#-------------------------------------------------------------------------

def gen_dest_dep_test():
  return [
    gen_rr_dest_dep_test( 5, "mul", 0x00000001, 0x0000000f, 0x0000000f ),
    gen_rr_dest_dep_test( 4, "mul", 0x00000002, 0x0000000f, 0x0000001e ),
    gen_rr_dest_dep_test( 3, "mul", 0x00000004, 0x0000000f, 0x0000003c ),
    gen_rr_dest_dep_test( 2, "mul", 0x00000008, 0x0000000f, 0x00000078 ),
    gen_rr_dest_dep_test( 1, "mul", 0x0000000f, 0x0000000f, 0x000000e1 ),
    gen_rr_dest_dep_test( 0, "mul", 0x000000ff, 0x0000000f, 0x00000ef1 ),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src0_dep_test():
  return [
    gen_rr_src0_dep_test( 5, "mul", 0x00000001, 0x0000000f, 0x0000000f ),
    gen_rr_src0_dep_test( 4, "mul", 0x00000002, 0x0000000f, 0x0000001e ),
    gen_rr_src0_dep_test( 3, "mul", 0x00000004, 0x0000000f, 0x0000003c ),
    gen_rr_src0_dep_test( 2, "mul", 0x00000008, 0x0000000f, 0x00000078 ),
    gen_rr_src0_dep_test( 1, "mul", 0x0000000f, 0x0000000f, 0x000000e1 ),
    gen_rr_src0_dep_test( 0, "mul", 0x000000ff, 0x0000000f, 0x00000ef1 ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_test
#-------------------------------------------------------------------------

def gen_src1_dep_test():
  return [
    gen_rr_src1_dep_test( 5, "mul", 0x0000000f, 0x00000001, 0x0000000f ),
    gen_rr_src1_dep_test( 4, "mul", 0x0000000f, 0x00000002, 0x0000001e ),
    gen_rr_src1_dep_test( 3, "mul", 0x0000000f, 0x00000004, 0x0000003c ),
    gen_rr_src1_dep_test( 2, "mul", 0x0000000f, 0x00000008, 0x00000078 ),
    gen_rr_src1_dep_test( 1, "mul", 0x0000000f, 0x0000000f, 0x000000e1 ),
    gen_rr_src1_dep_test( 0, "mul", 0x0000000f, 0x000000ff, 0x00000ef1 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_test
#-------------------------------------------------------------------------

def gen_srcs_dep_test():
  return [
    gen_rr_srcs_dep_test( 5, "mul", 0x000f0f00, 0x0000ff00, 0xFFF10000 ),
    gen_rr_srcs_dep_test( 4, "mul", 0x00f0f000, 0x000ff000, 0xF1000000 ),
    gen_rr_srcs_dep_test( 3, "mul", 0x0f0f0000, 0x00ff0000, 0x00000000 ),
    gen_rr_srcs_dep_test( 2, "mul", 0xf0f00000, 0x0ff00000, 0x00000000 ),
    gen_rr_srcs_dep_test( 1, "mul", 0x0f00000f, 0xff000000, 0xF1000000 ),
    gen_rr_srcs_dep_test( 0, "mul", 0xf00000f0, 0xf000000f, 0x10000E10 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rr_src0_eq_src1_test( "mul", 0x000f0f00, 0x000f0f00, 0xE1E10000),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_rr_value_test( "mul", 0xff00ff00, 0x0f0f0f0f, 0xF10F1000 ),
    gen_rr_value_test( "mul", 0x0ff00ff0, 0xf0f0f0f0, 0xF10F0E00 ),
    gen_rr_value_test( "mul", 0x00ff00ff, 0x0f0f0f0f, 0xF11E0F1F ),
    gen_rr_value_test( "mul", 0xf00ff00f, 0xf0f0f0f0, 0x0F0E1E10 ),
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in range(100):
    src0 = b32( random.randint(0,0xffffffff) )
    src1 = b32( random.randint(0,0xffffffff) )
    dest = src0 * src1
    asm_code.append( gen_rr_value_test( "mul", src0.uint(), src1.uint(), dest.uint() ) )
  return asm_code