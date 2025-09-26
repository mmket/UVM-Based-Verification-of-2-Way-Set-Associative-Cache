#=========================================================================
# lui
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
    lui x1, 0x0001
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x1 > 0x00001000
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
def gen_basic_a_test():
  return """
    lui x1, 0x0001
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x1 > 0x00001000
    nop
    nop
    nop
    nop
    nop
  """

def gen_basic_b_test():
  return """
    lui x1, 0x0001
    nop
    nop
    nop
    csrw proc2mngr, x1 > 0x00001000
    nop
    nop
    nop
  """
def gen_basic_c_test():
  return """
    lui x1, 0x0001
    csrw proc2mngr, x1 > 0x00001000
  """
#-------------------------------------------------------------------------
# gen_src_dep_test
#-------------------------------------------------------------------------
def gen_src_dep_test():
  return """
    lui x1, 0x0002
    csrw proc2mngr, x1 > 0x00002000
  """

def gen_value_test():
  return [
    gen_imm_value_test( "lui", 0x00000, 0x00000000 ),   
    gen_imm_value_test( "lui", 0x00001, 0x00001000 ),   
    gen_imm_value_test( "lui", 0x7ffff, 0x7ffff000 ),   
    gen_imm_value_test( "lui", 0xfffff, 0xfffff000 ),   
  ]

def gen_random_test():
  asm_code = []
  for i in range(1):
    imm =  b32(random.randint(0,0xffffffff) )
    dest =  b32(imm << 12)
    asm_code.append( gen_imm_value_test( "lui", int(imm[0:20]), int(dest) ) )
  return asm_code