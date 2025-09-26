#=========================================================================
# auipc
#=========================================================================

import random

# Fix the random seed so results are reproducible
random.seed(0xdeadbeef)

from pymtl3 import *
from lab2_proc.test.inst_utils import *
from lab2_proc.test.inst_utils import gen_imm_value_test


#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """
    auipc x1, 0x00010                       # PC=0x200
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw  proc2mngr, x1 > 0x00010200
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
def gen_dest_dep_a_test():
  return """
    auipc x1, 0x00010                       # PC=0x200
    nop
    nop
    nop
    nop
    nop
    csrw  proc2mngr, x1 > 0x00010200
    nop
    nop
    nop
    nop
    nop
  """

def gen_dest_dep_b_test():
  return """
    auipc x1, 0x00010                       # PC=0x200
    nop
    nop
    nop
    nop
    csrw  proc2mngr, x1 > 0x00010200
    nop
    nop
    nop
    nop
  """

def gen_dest_dep_c_test():
  return """
    auipc x1, 0x00010                       # PC=0x200
    nop
    nop
    nop
    csrw  proc2mngr, x1 > 0x00010200
    nop
    nop
    nop
  """

def gen_dest_dep_d_test():
  return """
    auipc x1, 0x00010                       # PC=0x200
    nop
    nop
    csrw  proc2mngr, x1 > 0x00010200
    nop
    nop
  """

def gen_dest_dep_e_test():
  return """
    auipc x1, 0x00010                       # PC=0x200
    nop
    csrw  proc2mngr, x1 > 0x00010200
    nop
  """

def gen_dest_dep_f_test():
  return """
    auipc x1, 0x00010                       # PC=0x200
    csrw  proc2mngr, x1 > 0x00010200
  """
#-------------------------------------------------------------------------
# gen_src_dep_test
#-------------------------------------------------------------------------
def gen_src_dep_a_test():
  return """
    auipc x1, 0x00020                       # PC=0x200
    nop
    nop
    nop
    nop
    nop
    csrw  proc2mngr, x1 > 0x00020200
    nop
    nop
    nop
    nop
    nop
  """

def gen_src_dep_b_test():
  return """
    auipc x1, 0x00010                       # PC=0x200
    nop
    nop
    nop
    nop
    csrw  proc2mngr, x1 > 0x00010200
    nop
    nop
    nop
    nop
  """

def gen_src_dep_c_test():
  return """
    auipc x1, 0x00011                       # PC=0x200
    nop
    nop
    nop
    csrw  proc2mngr, x1 > 0x00011200
    nop
    nop
    nop
  """

def gen_src_dep_d_test():
  return """
    auipc x1, 0x00012                       # PC=0x200
    nop
    nop
    csrw  proc2mngr, x1 > 0x00012200
    nop
    nop
  """

def gen_src_dep_e_test():
  return """
    auipc x1, 0x00070                       # PC=0x200
    nop
    csrw  proc2mngr, x1 > 0x00070200
    nop
  """

def gen_src_dep_f_test():
  return """
    auipc x1, 0x00080                       # PC=0x200
    csrw  proc2mngr, x1 > 0x00080200
  """

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------
# Edge cases:
# imm = 0, small positive, largest positive, and -1 (0xfffff)

def gen_value_test():
  return [
    gen_imm_value_test( "auipc", 0x00000, 0x00000200 ),   
    gen_imm_value_test( "auipc", 0x00010, 0x00010208 ),   
    gen_imm_value_test( "auipc", 0x7ffff, 0x7ffff210 ),   
    gen_imm_value_test( "auipc", 0xfffff, 0xfffff218 ),   
  ]

def gen_random_test():
  asm_code = []
  for i in range(1):
    PC = 0x200
    imm =  b32(random.randint(0,0xffffffff) )
    dest = (PC + b32(imm << 12)) 
    asm_code.append( gen_imm_value_test( "auipc", int(imm[0:20]), int(dest) ) )
  return asm_code