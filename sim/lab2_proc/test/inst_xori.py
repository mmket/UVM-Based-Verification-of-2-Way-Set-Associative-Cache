#=========================================================================
# xori
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
    csrr x1, mngr2proc < 0x0f0f0f0f
    nop
    xori x3, x1, 0x0f0
    nop
    csrw proc2mngr, x3 > 0x0f0f0fff
    nop
  """

#-------------------------------------------------------------------------
# gen_dest_dep_test
#-------------------------------------------------------------------------

def gen_dest_dep_test():
  return [
    gen_rimm_dest_dep_test( 1, "xori", 0x80000000, 0x800, 0x80000000 ^ 0xfffff800 ),
    gen_rimm_dest_dep_test( 0, "xori", 0x00ff00ff, 0x055, 0x00ff00ff ^ 0x00000055 ),
  ]

#-------------------------------------------------------------------------
# gen_src_dep_test
#-------------------------------------------------------------------------

def gen_src_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "xori", 0x00000f0f, 0x0ff, 0x00000f0f ^ 0x000000ff ),
    gen_rimm_src_dep_test( 4, "xori", 0x0000f0f0, 0x0f0, 0x0000f0f0 ^ 0x000000f0 ),
    gen_rimm_src_dep_test( 1, "xori", 0x13572468, 0x800, 0x13572468 ^ 0xfffff800 ),
    gen_rimm_src_dep_test( 0, "xori", 0x00ff00ff, 0x055, 0x00ff00ff ^ 0x00000055 ),
  ]

#-------------------------------------------------------------------------
# gen_imm_dep_test
#-------------------------------------------------------------------------

def gen_imm_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "xori", 0x11111111, 1,   0x11111111 ^ 0x00000001 ),
    gen_rimm_src_dep_test( 4, "xori", 0x11111111, 2,   0x11111111 ^ 0x00000002 ),
    gen_rimm_src_dep_test( 3, "xori", 0x11111111, 4,   0x11111111 ^ 0x00000004 ),
    gen_rimm_src_dep_test( 2, "xori", 0x11111111, 8,   0x11111111 ^ 0x00000008 ),
    gen_rimm_src_dep_test( 1, "xori", 0x11111111, 16,  0x11111111 ^ 0x00000010 ),
    gen_rimm_src_dep_test( 0, "xori", 0x11111111, 32,  0x11111111 ^ 0x00000020 ),
  ]

#-------------------------------------------------------------------------
# gen_src_imm_dep_test
#-------------------------------------------------------------------------

def gen_src_imm_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "xori", 0x22222222, 1, 0x22222222 ^ 0x00000001 ),
    gen_rimm_src_dep_test( 4, "xori", 0x22222222, 2, 0x22222222 ^ 0x00000002 ),
    gen_rimm_src_dep_test( 3, "xori", 0x22222222, 3, 0x22222222 ^ 0x00000003 ),
    gen_rimm_src_dep_test( 2, "xori", 0x22222222, 4, 0x22222222 ^ 0x00000004 ),
    gen_rimm_src_dep_test( 1, "xori", 0x22222222, 5, 0x22222222 ^ 0x00000005 ),
    gen_rimm_src_dep_test( 0, "xori", 0x22222222, 6, 0x22222222 ^ 0x00000006 ),
  ]

#-------------------------------------------------------------------------
# gen_src_eq_dest_test
#-------------------------------------------------------------------------

def gen_src_eq_dest_test():
  return [
    gen_rimm_src_eq_dest_test( "xori", 0x00000000, 1, 0x00000001 ),
    gen_rimm_src_eq_dest_test( "xori", 0x0000000f, 1, 0x0000000e ),
    gen_rimm_src_eq_dest_test( "xori", 0xffffffff, 1, 0xfffffffe ),
    gen_rimm_src_eq_dest_test( "xori", 0x12345678, 0xfff, 0x12345678 ^ 0xffffffff ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_rimm_value_test( "xori", 0x00000000, 0x000, 0x00000000 ),
    gen_rimm_value_test( "xori", 0xffffffff, 0x000, 0xffffffff ),
    gen_rimm_value_test( "xori", 0xffffffff, 0x001, 0xfffffffe ),
    gen_rimm_value_test( "xori", 0x80000000, 0x800, 0x80000000 ^ 0xfffff800 ),
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in range(100):
    src  = b32( random.randint(0,0xffffffff) )
    imm  = b12( random.randint(0,0xfff) )
    sext_imm = sext( imm, 32 )
    dest = src ^ sext_imm
    asm_code.append( gen_rimm_value_test( "xori", src.uint(), imm.uint(), dest.uint() ) )
  return asm_code