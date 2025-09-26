#=========================================================================
# slli
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
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    slli x3, x1, 0x03
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

#-------------------------------------------------------------------------
# gen_dest_dep_test
#-------------------------------------------------------------------------
def gen_dest_dep_test():
  return [
    gen_rimm_dest_dep_test( 5, "slli", 0x00000001, 1, 0x00000002 ),
    gen_rimm_dest_dep_test( 4, "slli", 0x00000002, 2, 0x00000008 ),
    gen_rimm_dest_dep_test( 3, "slli", 0x00000003, 3, 0x00000018 ),
    gen_rimm_dest_dep_test( 2, "slli", 0x00000004, 4, 0x00000040 ),
    gen_rimm_dest_dep_test( 1, "slli", 0x00000005, 5, 0x000000A0 ),
    gen_rimm_dest_dep_test( 0, "slli", 0x00000006, 6, 0x00000180 ),
  ]


#-------------------------------------------------------------------------
# gen_src_dep_test
#-------------------------------------------------------------------------
def gen_src_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "slli", 0x00000002, 1, 0x00000004 ),
    gen_rimm_src_dep_test( 4, "slli", 0x00000003, 1, 0x00000006 ),
    gen_rimm_src_dep_test( 3, "slli", 0x00000004, 1, 0x00000008 ),
    gen_rimm_src_dep_test( 2, "slli", 0x00000005, 1, 0x0000000a ),
    gen_rimm_src_dep_test( 1, "slli", 0x00000006, 1, 0x0000000c ),
    gen_rimm_src_dep_test( 0, "slli", 0x00000007, 1, 0x0000000e ),
  ]

#-------------------------------------------------------------------------
# gen_imm_dep_test
#-------------------------------------------------------------------------
def gen_imm_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "slli", 0x00000001, 1, 0x00000002 ),
    gen_rimm_src_dep_test( 4, "slli", 0x00000001, 2, 0x00000004 ),
    gen_rimm_src_dep_test( 3, "slli", 0x00000001, 3, 0x00000008 ),
    gen_rimm_src_dep_test( 2, "slli", 0x00000001, 4, 0x00000010 ),
    gen_rimm_src_dep_test( 1, "slli", 0x00000001, 5, 0x00000020 ),
    gen_rimm_src_dep_test( 0, "slli", 0x00000001, 6, 0x00000040 ),
  ]

#-------------------------------------------------------------------------
# gen_src_imm_dep_test
#-------------------------------------------------------------------------
def gen_src_imm_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "slli", 0x00000003, 1, 0x00000006 ),
    gen_rimm_src_dep_test( 4, "slli", 0x00000003, 2, 0x0000000c ),
    gen_rimm_src_dep_test( 3, "slli", 0x00000003, 3, 0x00000018 ),
    gen_rimm_src_dep_test( 2, "slli", 0x00000003, 4, 0x00000030 ),
    gen_rimm_src_dep_test( 1, "slli", 0x00000003, 5, 0x00000060 ),
    gen_rimm_src_dep_test( 0, "slli", 0x00000003, 6, 0x000000c0 ),
  ]

#-------------------------------------------------------------------------
# gen_rimm_src_eq_dest_test
#-------------------------------------------------------------------------

def gen_src_eq_dest_test():
  return [
    gen_rimm_src_eq_dest_test( "slli", 0x00000001, 1, 0x00000002 ),
    gen_rimm_src_eq_dest_test( "slli", 0x00000002, 2, 0x00000008 ),
    gen_rimm_src_eq_dest_test( "slli", 0x00000003, 3, 0x00000018 ),
    gen_rimm_src_eq_dest_test( "slli", 0x00000004, 4, 0x00000040 ),
    gen_rimm_src_eq_dest_test( "slli", 0x00000005, 5, 0x000000A0 ),  
    gen_rimm_src_eq_dest_test( "slli", 0x00000006, 6, 0x00000180 ),
  ]

#-------------------------------------------------------------------------
# gen_rimm_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_rimm_value_test( "slli", 0x00000001, 0, 0x00000001 ), 
    gen_rimm_value_test( "slli", 0x00000001, 1, 0x00000002 ), 
    gen_rimm_value_test( "slli", 0x00000001, 31, 0x80000000 ),

    gen_rimm_value_test( "slli", 0x80000000, 1, 0x00000000 ), 
    gen_rimm_value_test( "slli", 0xffffffff, 4, 0xfffffff0 ), 
  ]


#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in range(100):
    src = b32( random.randint(0,0xffffffff) )
    imm = random.randint(0,31)   
    dest = b32( (src.uint() << imm) & 0xffffffff )
    asm_code.append( gen_rimm_value_test( "slli", src.uint(), imm, dest.uint() ) )
  return asm_code