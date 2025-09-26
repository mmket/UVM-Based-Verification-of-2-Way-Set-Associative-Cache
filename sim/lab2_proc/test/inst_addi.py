#=========================================================================
# addi
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

    csrr x1, mngr2proc, < 5
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    addi x3, x1, 0x0004
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 9
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
    gen_rimm_dest_dep_test( 5, "addi", 1, 1, 2 ),
    gen_rimm_dest_dep_test( 4, "addi", 2, 1, 3 ),
    gen_rimm_dest_dep_test( 3, "addi", 3, 1, 4 ),
    gen_rimm_dest_dep_test( 2, "addi", 4, 1, 5 ),
    gen_rimm_dest_dep_test( 1, "addi", 5, 1, 6 ),
    gen_rimm_dest_dep_test( 0, "addi", 6, 1, 7 ),
  ]

#-------------------------------------------------------------------------
# gen_src_dep_test
#-------------------------------------------------------------------------
def gen_src_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "addi",  7, 1,  8 ),
    gen_rimm_src_dep_test( 4, "addi",  8, 1,  9 ),
    gen_rimm_src_dep_test( 3, "addi",  9, 1, 10 ),
    gen_rimm_src_dep_test( 2, "addi", 10, 1, 11 ),
    gen_rimm_src_dep_test( 1, "addi", 11, 1, 12 ),
    gen_rimm_src_dep_test( 0, "addi", 12, 1, 13 ),
  ]
#-------------------------------------------------------------------------
# gen_imm_dep_test
#-------------------------------------------------------------------------
def gen_imm_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "addi",  7, 1,  8 ),
    gen_rimm_src_dep_test( 4, "addi",  7, 2,  9 ),
    gen_rimm_src_dep_test( 3, "addi",  7, 3, 10 ),
    gen_rimm_src_dep_test( 2, "addi",  7, 4, 11 ),
    gen_rimm_src_dep_test( 1, "addi",  7, 5, 12 ),
    gen_rimm_src_dep_test( 0, "addi",  7, 6, 13 ),
  ]
#-------------------------------------------------------------------------
# gen_src_imm_dep_test
#-------------------------------------------------------------------------
def gen_src_imm_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "addi",  7, 1,  8 ),
    gen_rimm_src_dep_test( 4, "addi",  8, 2,  10 ),
    gen_rimm_src_dep_test( 3, "addi",  9, 3, 12 ),
    gen_rimm_src_dep_test( 2, "addi",  10, 4, 14 ),
    gen_rimm_src_dep_test( 1, "addi",  11, 5, 16 ),
    gen_rimm_src_dep_test( 0, "addi",  12, 6, 18 ),
  ]
#-------------------------------------------------------------------------
# gen_rimm_src_eq_dest_test
#-------------------------------------------------------------------------

def gen_src_eq_dest_test():
  return [
    gen_rimm_src_eq_dest_test(  "addi", 12, 2, 14 ),
    gen_rimm_src_eq_dest_test(  "addi", 13, 3, 16 ),
    gen_rimm_src_eq_dest_test( "addi", 14, 4, 18 ),
    gen_rimm_src_eq_dest_test( "addi", 15, 5, 20 ),
    gen_rimm_src_eq_dest_test( "addi", 16, 6, 22 ),
    gen_rimm_src_eq_dest_test(  "addi", 17, 7, 24 ),
  ]

#-------------------------------------------------------------------------
# gen_rimm_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_rr_value_test( "add", 0x00000002, 0x00000002, 0x00000004 ),
    gen_rr_value_test( "add", 0x00000001, 0x00000001, 0x00000002 ),
    gen_rr_value_test( "add", 0x00000003, 0x00000007, 0x0000000a ),

  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in range(100):
    src = b32( random.randint(0,0xffffffff) )
    imm = b32( random.randint(0,0xffffffff) )
    dest = src + imm
    asm_code.append( gen_rr_value_test( "add", src.uint(), imm.uint(), dest.uint() ) )
  return asm_code
