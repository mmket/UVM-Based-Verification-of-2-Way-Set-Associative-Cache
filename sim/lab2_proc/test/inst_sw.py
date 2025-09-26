#=========================================================================
# sw
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
    csrr x1, mngr2proc < 0x00002000
    csrr x2, mngr2proc < 0xdeadbeef
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    sw   x2, 0(x1)
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    lw   x3, 0(x1)
    csrw proc2mngr, x3 > 0xdeadbeef

    .data
    .word 0x01020304
  """
#=========================================================================
# sw tests
#=========================================================================


def gen_sw_dest_dep():
  return [
     gen_sd_dest_dep_test(5, "sw", "lw", 0x2000, 0xdeadbeef), 
     gen_sd_dest_dep_test(4, "sw", "lw", 0x2004, 0xcafebabe),
     gen_sd_dest_dep_test(3, "sw", "lw", 0x2008, 0x0badf00d),
     gen_sd_dest_dep_test(2, "sw", "lw", 0x200c, 0x12345678),
     gen_sd_dest_dep_test(1, "sw", "lw", 0x2010, 0xffffffff),
     gen_sd_dest_dep_test(0, "sw", "lw", 0x2014, 0x00000000),
  ]
 
def gen_sw_base_dep():
  return [
     gen_sd_base_dep_test(5, "sw", "lw", 0x2000, 0xdeadbeef), 
     gen_sd_base_dep_test(4, "sw", "lw", 0x2004, 0xcafebabe),
     gen_sd_base_dep_test(3, "sw", "lw", 0x2008, 0x0badf00d),
     gen_sd_base_dep_test(2, "sw", "lw", 0x200c, 0x12345678),
     gen_sd_base_dep_test(1, "sw", "lw", 0x2010, 0xffffffff),
     gen_sd_base_dep_test(0, "sw", "lw", 0x2014, 0x00000000),
  ]

def gen_srcs_dest_test():
  return [
    gen_sd_base_eq_dest_test( "sw", "lw", 0x2000, 0xdeadbeef ),
  ]

#-------------------------------------------------------------------------
# gen_addr_test for sw
#-------------------------------------------------------------------------

def gen_addr_test():
  return [

    gen_sd_value_test( "sw", "lw",   0, 0x00002000, 0xdeadbeef ),
    gen_sd_value_test( "sw", "lw",   4, 0x00002000, 0x00010203 ),
    gen_sd_value_test( "sw", "lw",   8, 0x00002000, 0x04050607 ),
    gen_sd_value_test( "sw", "lw",  12, 0x00002000, 0x08090a0b ),
    gen_sd_value_test( "sw", "lw",  16, 0x00002000, 0x0c0d0e0f ),
    gen_sd_value_test( "sw", "lw",  20, 0x00002000, 0xcafecafe ),

    gen_sd_value_test( "sw", "lw", -20, 0x00002014, 0xdeadbeef ),
    gen_sd_value_test( "sw", "lw", -16, 0x00002014, 0x00010203 ),
    gen_sd_value_test( "sw", "lw", -12, 0x00002014, 0x04050607 ),
    gen_sd_value_test( "sw", "lw",  -8, 0x00002014, 0x08090a0b ),
    gen_sd_value_test( "sw", "lw",  -4, 0x00002014, 0x0c0d0e0f ),
    gen_sd_value_test( "sw", "lw",   0, 0x00002014, 0xcafecafe ),

    gen_sd_value_test( "sw", "lw",  1, 0x00001fff, 0xdeadbeef ),
    gen_sd_value_test( "sw", "lw",  5, 0x00001fff, 0x00010203 ),
    gen_sd_value_test( "sw", "lw",  9, 0x00001fff, 0x04050607 ),
    gen_sd_value_test( "sw", "lw", 13, 0x00001fff, 0x08090a0b ),
    gen_sd_value_test( "sw", "lw", 17, 0x00001fff, 0x0c0d0e0f ),
    gen_sd_value_test( "sw", "lw", 21, 0x00001fff, 0xcafecafe ),

    gen_sd_value_test( "sw", "lw", -21, 0x00002015, 0xdeadbeef ),
    gen_sd_value_test( "sw", "lw", -17, 0x00002015, 0x00010203 ),
    gen_sd_value_test( "sw", "lw", -13, 0x00002015, 0x04050607 ),
    gen_sd_value_test( "sw", "lw",  -9, 0x00002015, 0x08090a0b ),
    gen_sd_value_test( "sw", "lw",  -5, 0x00002015, 0x0c0d0e0f ),
    gen_sd_value_test( "sw", "lw",  -1, 0x00002015, 0xcafecafe ),

    ]



#-------------------------------------------------------------------------
# gen_random_test for sw
#-------------------------------------------------------------------------

import random

def gen_random_test():


  data = []
  for i in range(128):
    data.append( random.randint(0,0xffffffff) )

  asm_code = []
  for i in range(100):

    a = random.randint(0,127)  
    b = random.randint(0,127)  

    base   = 0x2000 + (4*b)
    offset = 4*(a - b)
    value  = data[a]

    asm_code.append( gen_sd_value_test( "sw", "lw", offset, base, value ) )


  asm_code.append( gen_word_data( [0x00000000]*128 ) )

  return asm_code
