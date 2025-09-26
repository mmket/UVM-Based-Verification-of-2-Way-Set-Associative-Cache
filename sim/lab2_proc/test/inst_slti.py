#=========================================================================
# slti
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
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    slti x3, x1, 6
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 1
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
  """

#=========================================================================
# slti tests
#=========================================================================

import random
from pymtl3 import *
from lab2_proc.test.inst_utils import *

#-------------------------------------------------------------------------
# gen_dest_dep_test
#-------------------------------------------------------------------------

def gen_dest_dep_test():
  return [
    gen_rimm_dest_dep_test( 5, "slti",  1,  2, 1 ),   # 1 < 2 -> 1
    gen_rimm_dest_dep_test( 4, "slti",  2,  2, 0 ),   # 2 < 2 -> 0
    gen_rimm_dest_dep_test( 3, "slti", -1 & 0xffffffff,  1, 1 ), # -1 < 1 -> 1
    gen_rimm_dest_dep_test( 2, "slti",  5, -3, 0 ),   # 5 < -3 -> 0
    gen_rimm_dest_dep_test( 1, "slti", -5 & 0xffffffff, -3, 1 ), # -5 < -3 -> 1
    gen_rimm_dest_dep_test( 0, "slti",  7,  7, 0 ),   # equal -> 0
  ]

#-------------------------------------------------------------------------
# gen_src_dep_test
#-------------------------------------------------------------------------

def gen_src_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "slti", -8 & 0xffffffff, -7, 1 ),
    gen_rimm_src_dep_test( 4, "slti", -5 & 0xffffffff,  0, 1 ),
    gen_rimm_src_dep_test( 3, "slti",  0, -1, 0 ),
    gen_rimm_src_dep_test( 2, "slti",  5,  10, 1 ),
    gen_rimm_src_dep_test( 1, "slti", 10,  5, 0 ),
    gen_rimm_src_dep_test( 0, "slti",  7,  7, 0 ),
  ]

#-------------------------------------------------------------------------
# gen_src_eq_dest_test
#-------------------------------------------------------------------------

def gen_src_eq_dest_test():
  return [
    gen_rimm_src_eq_dest_test( "slti",  1,  2, 1 ),
    gen_rimm_src_eq_dest_test( "slti", -2 & 0xffffffff, -1, 1 ),
    gen_rimm_src_eq_dest_test( "slti",  5,  5, 0 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_rimm_value_test( "slti", 0x00000000,  0, 0 ),
    gen_rimm_value_test( "slti", 0x00000001,  1, 0 ),
    gen_rimm_value_test( "slti", 0x00000001,  2, 1 ),
    gen_rimm_value_test( "slti", 0x00000002,  1, 0 ),

    gen_rimm_value_test( "slti", -1 & 0xffffffff,  1, 1 ),
    gen_rimm_value_test( "slti",  1, -1, 0 ),

    gen_rimm_value_test( "slti", -5 & 0xffffffff, -3, 1 ),
    gen_rimm_value_test( "slti", -3 & 0xffffffff, -5, 0 ),

    gen_rimm_value_test( "slti", 0x7fffffff, -1, 0 ),
    gen_rimm_value_test( "slti", -0x80000000 & 0xffffffff, 0, 1 ),

    gen_rimm_value_test( "slti",  0,  2047, 1 ),
    gen_rimm_value_test( "slti",  2047, 2047, 0 ),
    gen_rimm_value_test( "slti", -2048 & 0xffffffff, -2048, 0 ),
    gen_rimm_value_test( "slti", -2047 & 0xffffffff, -2048, 0 ),
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in range(100):
    src = b32( random.randint(0,0xffffffff) )
    imm = random.randint(-2048,2047)  
    dest = b32(1 if src.int() < imm else 0)
    asm_code.append( gen_rimm_value_test( "slti", src.uint(), imm, dest.uint() ) )
  return asm_code
