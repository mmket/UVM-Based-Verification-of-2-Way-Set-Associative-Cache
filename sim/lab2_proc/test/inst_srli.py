#=========================================================================
# srli
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
    srli x3, x1, 0x03
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 0x10001000
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
    gen_rimm_dest_dep_test( 5, "srli", 0x00000008, 1, 0x00000004 ),
    gen_rimm_dest_dep_test( 4, "srli", 0x00000010, 2, 0x00000004 ),
    gen_rimm_dest_dep_test( 3, "srli", 0x00000018, 3, 0x00000003 ),
    gen_rimm_dest_dep_test( 2, "srli", 0x00000040, 4, 0x00000004 ),
    gen_rimm_dest_dep_test( 1, "srli", 0x000000A0, 5, 0x00000005 ),
    gen_rimm_dest_dep_test( 0, "srli", 0x00000180, 6, 0x00000006 ),
  ]

#-------------------------------------------------------------------------
# gen_src_dep_test
#-------------------------------------------------------------------------

def gen_src_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "srli", 0x00000008, 1, 0x00000004 ),
    gen_rimm_src_dep_test( 4, "srli", 0x0000000C, 1, 0x00000006 ),
    gen_rimm_src_dep_test( 3, "srli", 0x00000010, 1, 0x00000008 ),
    gen_rimm_src_dep_test( 2, "srli", 0x00000014, 1, 0x0000000A ),
    gen_rimm_src_dep_test( 1, "srli", 0x00000018, 1, 0x0000000C ),
    gen_rimm_src_dep_test( 0, "srli", 0x0000001C, 1, 0x0000000E ),
  ]

#-------------------------------------------------------------------------
# gen_imm_dep_test
#-------------------------------------------------------------------------

def gen_imm_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "srli", 0x00000080, 1, 0x00000040 ),
    gen_rimm_src_dep_test( 4, "srli", 0x00000080, 2, 0x00000020 ),
    gen_rimm_src_dep_test( 3, "srli", 0x00000080, 3, 0x00000010 ),
    gen_rimm_src_dep_test( 2, "srli", 0x00000080, 4, 0x00000008 ),
    gen_rimm_src_dep_test( 1, "srli", 0x00000080, 5, 0x00000004 ),
    gen_rimm_src_dep_test( 0, "srli", 0x00000080, 6, 0x00000002 ),
  ]

#-------------------------------------------------------------------------
# gen_src_imm_dep_test
#-------------------------------------------------------------------------

def gen_src_imm_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "srli", 0x000000C0, 1, 0x00000060 ),
    gen_rimm_src_dep_test( 4, "srli", 0x000000C0, 2, 0x00000030 ),
    gen_rimm_src_dep_test( 3, "srli", 0x000000C0, 3, 0x00000018 ),
    gen_rimm_src_dep_test( 2, "srli", 0x000000C0, 4, 0x0000000C ),
    gen_rimm_src_dep_test( 1, "srli", 0x000000C0, 5, 0x00000006 ),
    gen_rimm_src_dep_test( 0, "srli", 0x000000C0, 6, 0x00000003 ),
  ]

#-------------------------------------------------------------------------
# gen_src_eq_dest_test
#-------------------------------------------------------------------------

def gen_src_eq_dest_test():
  return [
    gen_rimm_src_eq_dest_test( "srli", 0x00000008, 1, 0x00000004 ),
    gen_rimm_src_eq_dest_test( "srli", 0x00000010, 2, 0x00000004 ),
    gen_rimm_src_eq_dest_test( "srli", 0x00000018, 3, 0x00000003 ),
    gen_rimm_src_eq_dest_test( "srli", 0x00000040, 4, 0x00000004 ),
    gen_rimm_src_eq_dest_test( "srli", 0x000000A0, 5, 0x00000005 ),
    gen_rimm_src_eq_dest_test( "srli", 0x00000180, 6, 0x00000006 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_rimm_value_test( "srli", 0x00000001, 0, 0x00000001 ),
    gen_rimm_value_test( "srli", 0x00000002, 1, 0x00000001 ),
    gen_rimm_value_test( "srli", 0x80000000, 31, 0x00000001 ),  # logical right shift

    gen_rimm_value_test( "srli", 0xFFFFFFFF, 1, 0x7FFFFFFF ),   # logical shift → zero fill
    gen_rimm_value_test( "srli", 0xFFFFFFFF, 4, 0x0FFFFFFF ),
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in range(100):
    src  = b32( random.randint(0,0xffffffff) )
    imm  = random.randint(0,31)
    dest = b32( (src.uint() >> imm) & 0xffffffff )  # logical right shift
    asm_code.append( gen_rimm_value_test( "srli", src.uint(), imm, dest.uint() ) )
  return asm_code