#=========================================================================
# jalr
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

    # Use r3 to track the control flow pattern
    addi  x3, x0, 0           # 0x0200
                              #
    lui x1,      %hi[label_a] # 0x0204
    addi x1, x1, %lo[label_a] # 0x0208
                              #
    nop                       # 0x020c
    nop                       # 0x0210
    nop                       # 0x0214
    nop                       # 0x0218
    nop                       # 0x021c
    nop                       # 0x0220
    nop                       # 0x0224
    nop                       # 0x0228
                              #
    jalr  x31, x1, 0          # 0x022c
    addi  x3, x3, 0b01        # 0x0230

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

  label_a:
    addi  x3, x3, 0b10

    # Check the link address
    csrw  proc2mngr, x31 > 0x0230

    # Only the second bit should be set if jump was taken
    csrw  proc2mngr, x3  > 0b10

  """

def gen_data_test():
  return """

    # Use r3 to track the control flow pattern
    addi  x3, x0, 0           
                              
    lui x1,      %hi[label_a] 
    addi x1, x1, %lo[label_a] 
                              
                              
    jalr  x31, x1, 0          
    addi  x3, x3, 0b01        


  label_a:
    addi  x3, x3, 0b10

    # Check the link address
    csrw  proc2mngr, x31 > 0x0210

    # Only the second bit should be set if jump was taken
    csrw  proc2mngr, x3  > 0b10

  """
def gen_multijump_test():
  return """
    addi  x3, x0, 0

    lui   x1, %hi[label_a]
    addi  x1, x1, %lo[label_a]
    jalr  x5, x1, 0
    addi  x3, x3, 0b000001

  label_b:
    addi  x3, x3, 0b000010
    addi  x6, x5, 0

    lui   x1, %hi[label_c]
    addi  x1, x1, %lo[label_c]
    jalr  x7, x1, 0
    addi  x3, x3, 0b000100

  label_a:
    addi  x3, x3, 0b001000
    addi  x4, x5, 0

    lui   x1, %hi[label_b]
    addi  x1, x1, %lo[label_b]
    jalr  x5, x1, 0
    addi  x3, x3, 0b010000

  label_c:
    addi  x3, x3, 0b100000

    # Verify control flow
    csrw  proc2mngr, x3 > 0b101010

    # Check link addresses
    csrw  proc2mngr, x4 > 0x00000210
    csrw  proc2mngr, x6 > 0x00000240
    csrw  proc2mngr, x7 > 0x00000228
  """

def gen_back_to_back_test():
  return """
    addi  x3, x0, 0

    lui   x1, %hi[label_b]
    addi  x1, x1, %lo[label_b]
    jalr  x31, x1, 0

  label_b:
    csrw  proc2mngr, x31 > 0x0210

    addi  x3, x3, 1
    csrw  proc2mngr, x3 > 0x1
  """

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

import random

def gen_random_test():
  asm_code = []
  random.seed(0x4750)

  for i in range(2):

    imm = 12

    label = f"target_{i}"

    asm_code.append(f"jal x1, {label}")       
    asm_code.append("nop")                    
    asm_code.append("nop")

    asm_code.append(f"jalr x2, x1, {imm}")    
    asm_code.append("nop")
    asm_code.append("nop")

    asm_code.append(f"{label}:")
    asm_code.append("addi x3, x0, 99")
    asm_code.append("csrw proc2mngr, x3 > 99")
  print("\n".join(asm_code))
  return "\n".join(asm_code)