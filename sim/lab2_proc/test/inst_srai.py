#=========================================================================
# srai
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
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    srai x3, x1, 0x03
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

#-------------------------------------------------------------------------
# gen_dest_dep_test
#-------------------------------------------------------------------------

def gen_dest_dep_test():
  return [
    gen_rimm_dest_dep_test( 5, "srai", 0x00000010, 1, 0x00000008 ), 
    gen_rimm_dest_dep_test( 4, "srai", 0x00000010, 2, 0x00000004 ), 
    gen_rimm_dest_dep_test( 3, "srai", -0x00000010 & 0xffffffff, 1, 0xfffffff8 ), 
    gen_rimm_dest_dep_test( 2, "srai", -0x00000010 & 0xffffffff, 2, 0xfffffffc ), 
    gen_rimm_dest_dep_test( 1, "srai", 0x7fffffff, 31, 0x00000001 ), 
    gen_rimm_dest_dep_test( 0, "srai", 0xffffffff, 31, 0xffffffff ), 
  ]

#-------------------------------------------------------------------------
# gen_src_dep_test
#-------------------------------------------------------------------------

def gen_src_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "srai", 0x00000020, 1, 0x00000010 ),
    gen_rimm_src_dep_test( 4, "srai", 0x00000020, 2, 0x00000008 ),
    gen_rimm_src_dep_test( 3, "srai", -0x00000020 & 0xffffffff, 1, 0xfffffff0 ),
    gen_rimm_src_dep_test( 2, "srai", -0x00000020 & 0xffffffff, 2, 0xfffffff8 ),
    gen_rimm_src_dep_test( 1, "srai", 0x80000000, 1, 0xc0000000 ), 
    gen_rimm_src_dep_test( 0, "srai", 0xffffffff, 1, 0xffffffff ),
  ]

#-------------------------------------------------------------------------
# gen_imm_dep_test
#-------------------------------------------------------------------------

def gen_imm_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "srai", 0x00000010, 1, 0x00000008 ),
    gen_rimm_src_dep_test( 4, "srai", 0x00000010, 2, 0x00000004 ),
    gen_rimm_src_dep_test( 3, "srai", 0x00000010, 3, 0x00000002 ),
    gen_rimm_src_dep_test( 2, "srai", -0x00000010 & 0xffffffff, 4, 0xfffffffe ),
    gen_rimm_src_dep_test( 1, "srai", 0x7fffffff, 30, 0x00000003 ),
    gen_rimm_src_dep_test( 0, "srai", 0xffffffff, 31, 0xffffffff ),
  ]

#-------------------------------------------------------------------------
# gen_src_imm_dep_test
#-------------------------------------------------------------------------

def gen_src_imm_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "srai", 0x00000030, 1, 0x00000018 ),
    gen_rimm_src_dep_test( 4, "srai", 0x00000030, 2, 0x0000000c ),
    gen_rimm_src_dep_test( 3, "srai", 0x00000030, 3, 0x00000006 ),
    gen_rimm_src_dep_test( 2, "srai", -0x00000030 & 0xffffffff, 1, 0xffffffe8 ),
    gen_rimm_src_dep_test( 1, "srai", -0x00000030 & 0xffffffff, 2, 0xffffffec ),
    gen_rimm_src_dep_test( 0, "srai", -0x00000030 & 0xffffffff, 3, 0xfffffff6 ),
  ]

#-------------------------------------------------------------------------
# gen_rimm_src_eq_dest_test
#-------------------------------------------------------------------------

def gen_src_eq_dest_test():
  return [
    gen_rimm_src_eq_dest_test( "srai", 0x00000040, 1, 0x00000020 ),
    gen_rimm_src_eq_dest_test( "srai", 0x00000040, 2, 0x00000010 ),
    gen_rimm_src_eq_dest_test( "srai", -0x00000040 & 0xffffffff, 1, 0xfffffffe0 ),
    gen_rimm_src_eq_dest_test( "srai", -0x00000040 & 0xffffffff, 2, 0xfffffff0 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    # 正数移位
    gen_rimm_value_test( "srai", 0x00000010, 0, 0x00000010 ), 
    gen_rimm_value_test( "srai", 0x00000010, 1, 0x00000008 ),
    gen_rimm_value_test( "srai", 0x00000010, 4, 0x00000001 ),

    # 负数移位
    gen_rimm_value_test( "srai", -0x00000010 & 0xffffffff, 1, 0xfffffff8 ),
    gen_rimm_value_test( "srai", -0x00000010 & 0xffffffff, 4, 0xfffffffe ),

    # 边界测试
    gen_rimm_value_test( "srai", 0x7fffffff, 31, 0x00000001 ), 
    gen_rimm_value_test( "srai", 0x80000000, 31, 0xffffffff ), 
    gen_rimm_value_test( "srai", 0xffffffff, 31, 0xffffffff ), 

    # 移位截断
    gen_rimm_value_test( "srai", 0x00000010, 32, 0x00000010 ), 
    gen_rimm_value_test( "srai", 0x00000010, 33, 0x00000008 ), 
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in range(100):
    src = b32( random.randint(0,0xffffffff) )
    imm = random.randint(0,31)  
    dest = b32( src.int() >> imm )  
    asm_code.append( gen_rimm_value_test( "srai", src.uint(), imm, dest.uint() ) )
  return asm_code