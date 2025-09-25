#=========================================================================
# sra
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
    sra x3, x1, x2
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

# ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Define additional directed and random test cases.
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#=========================================================================
# sra tests
#=========================================================================

import random
from pymtl3 import *
from lab2_proc.test.inst_utils import *

#-------------------------------------------------------------------------
# gen_dest_dep_test
#-------------------------------------------------------------------------

def gen_dest_dep_test():
  return [
    gen_rr_dest_dep_test( 5, "sra",  0x00000010, 1, 0x00000008 ),   # 16 >> 1 = 8
    gen_rr_dest_dep_test( 4, "sra",  0x00000010, 2, 0x00000004 ),   # 16 >> 2 = 4
    gen_rr_dest_dep_test( 3, "sra", -0x00000010 & 0xffffffff, 1, 0xfffffff8 ), # -16 >> 1 = -8
    gen_rr_dest_dep_test( 2, "sra", -0x00000010 & 0xffffffff, 2, 0xfffffffc ), # -16 >> 2 = -4
    gen_rr_dest_dep_test( 1, "sra",  0x80000000, 1, 0xc0000000 ),   # 最小负数右移
    gen_rr_dest_dep_test( 0, "sra",  0xffffffff, 4, 0xffffffff ),   # -1 >> n = -1
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src0_dep_test():
  return [
    gen_rr_src0_dep_test( 5, "sra",  0x00000010, 1, 0x00000008 ),
    gen_rr_src0_dep_test( 4, "sra",  0x00000020, 2, 0x00000008 ),
    gen_rr_src0_dep_test( 3, "sra", -0x00000020 & 0xffffffff, 1, 0xfffffff0 ),
    gen_rr_src0_dep_test( 2, "sra", -0x00000020 & 0xffffffff, 2, 0xfffffff8 ),
    gen_rr_src0_dep_test( 1, "sra",  0x7fffffff, 1, 0x3fffffff ),
    gen_rr_src0_dep_test( 0, "sra",  0xffffffff, 1, 0xffffffff ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_test
#-------------------------------------------------------------------------

def gen_src1_dep_test():
  return [
    gen_rr_src1_dep_test( 5, "sra",  0x00000010, 1, 0x00000008 ),
    gen_rr_src1_dep_test( 4, "sra",  0x00000010, 2, 0x00000004 ),
    gen_rr_src1_dep_test( 3, "sra", -0x00000010 & 0xffffffff, 1, 0xfffffff8 ),
    gen_rr_src1_dep_test( 2, "sra", -0x00000010 & 0xffffffff, 2, 0xfffffffc ),
    gen_rr_src1_dep_test( 1, "sra",  0x80000000, 1, 0xc0000000 ),
    gen_rr_src1_dep_test( 0, "sra",  0xffffffff, 4, 0xffffffff ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_test
#-------------------------------------------------------------------------

def gen_srcs_dep_test():
  return [
    gen_rr_srcs_dep_test( 5, "sra",  0x00000020, 1, 0x00000010 ),
    gen_rr_srcs_dep_test( 4, "sra",  0x00000020, 2, 0x00000008 ),
    gen_rr_srcs_dep_test( 3, "sra", -0x00000020 & 0xffffffff, 1, 0xfffffff0 ),
    gen_rr_srcs_dep_test( 2, "sra", -0x00000020 & 0xffffffff, 2, 0xfffffff8 ),
    gen_rr_srcs_dep_test( 1, "sra",  0x00000020, 1, 0x00000010 ),
    gen_rr_srcs_dep_test( 0, "sra",  0xffffffff, 31, 0xffffffff ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rr_src0_eq_dest_test( "sra",  0x00000010, 1, 0x00000008 ),
    gen_rr_src1_eq_dest_test( "sra", -0x00000010 & 0xffffffff, 1, 0xfffffff8 ),
    gen_rr_srcs_eq_dest_test( "sra", -0x00000008 & 0xffffffff, 0xffffffff ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_rr_value_test( "sra", 0x00000010, 1, 0x00000008 ),
    gen_rr_value_test( "sra", 0x00000010, 4, 0x00000001 ),
    
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in range(100):
    src0 = b32( random.randint(0,0xffffffff) )
    src1 = random.randint(0,31)  
    dest = b32( src0.int() >> src1 )  
    asm_code.append( gen_rr_value_test( "sra", src0.uint(), src1, dest.uint() ) )
  return asm_code