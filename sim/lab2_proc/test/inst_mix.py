import pytest
from pymtl3 import *
from lab2_proc.test.harness import asm_test, run_test
from lab2_proc.ProcFL import ProcFL  
from lab2_proc.test.inst_utils import *

#-------------------------------------------------------------------------
# gen_branch_1
#-------------------------------------------------------------------------
def gen_branch_1():
    return """
        csrr x3, mngr2proc < 1
        csrr x1, mngr2proc < 2
        csrr x5, mngr2proc < 1

        nop
        blt  x3, x1, hello
        addi x3, x0, 0b01

hello:
        mul  x6, x1, x5
        bne  x3, x1, label_a

helloworld:
        beq  x3, x5, hworld
        addi x3, x0, 0b11

        nop
hworld:
        add  x3, x3, x6
        addi x3, x3, 0b10

label_a:
        csrw proc2mngr, x3 > 0x01

        nop
        nop
    """

from pymtl3 import *
from lab2_proc.test.inst_utils import *

def gen_branch_2():
    return """

        csrr x3, mngr2proc < 1
        csrr x1, mngr2proc < 1

        beq x3, x1, hello
        mul x5, x3, x1

    helo:
        beq x3, x1, label_a
        mul x6, x3, x1

    helloworld:
        beq x3, x1, hworld
        mul x7, x3, x1
        
    hello: 
        beq x3, x1, helloworld
        mul x8, x3, x1

    hworld:
        jal x4, helo
        mul x9, x3, x1

    label_a:
        addi x3, x3, 0b10

        # Only the second bit should be set if branch was taken
        csrw proc2mngr, x3 > 0x03
    """


def gen_branch_3():
    return """

        csrr x3, mngr2proc < 1
        csrr x1, mngr2proc < 2

    
        bne x3, x1, hello
        lw   x3, 0(x1)
    
    helo:
        bne x3, x1, label_a
        sw   x3, 0(x1)

    helloworld:
        bne x3, x1, hworld

    hello: 
        bne x3, x1, helloworld

    hworld:
        jal x4, helo
        lw   x3, 0(x1)

    label_a:
    addi  x3, x3, 0b10

    # Only the second bit should be set if branch was taken
    csrw proc2mngr, x3 > 0x03

    out:
        nop
        nop
        nop

        """

#=========================================================================
# inst_mix.py
#=========================================================================
import random
from pymtl3 import *
from lab2_proc.test.inst_utils import *

#-------------------------------------------------------------------------
# gen_mul_lw_add_test
#-------------------------------------------------------------------------
# This test mixes multiplication, memory load, and addition instructions.
# It writes values to memory, loads them, multiplies, then adds.

def gen_branch_4():
  return """
    # Initialize registers
    csrr x1, mngr2proc < 2      # x1 = 2
    csrr x2, mngr2proc < 3      # x2 = 3
    csrr x3, mngr2proc < 4      # x3 = 4

    # Reserve a memory location
    lui  x10, 0x00020           # x10 = 0x20000 (base address)

    # Store x3 to memory
    sw   x3, 0(x10)             # M[x10] = 4

    # Delay
    nop
    nop

    # Load from memory
    lw   x4, 0(x10)             # x4 = M[x10] = 4

    # Multiply values
    mul  x5, x1, x2             # x5 = 2 * 3 = 6

    # Delay
    nop
    nop

    # Add result with loaded value
    add  x6, x4, x5             # x6 = 4 + 6 = 10

    # Final check
    csrw proc2mngr, x6 > 10

    nop
    nop
  """

def gen_branch_5():
    return """

        csrr x3, mngr2proc < 1
        csrr x1, mngr2proc < 1

        beq x3, x1, hello
        mul x5, x3, x1

    helo:
        beq x3, x1, label_a
        mul x6, x3, x1

    helloworld:
        beq x3, x1, hworld
        mul x7, x3, x1
        
    hello: 
        beq x3, x1, helloworld
        mul x8, x3, x1

    hworld:
        lui x10, 0x00020
        sw  x3, 0(x10)
        mul x12, x3, x1
        lw  x11, 0(x10)
        jal x4, helo
        mul x9, x3, x1

    label_a:
        addi x3, x3, 0b10
        csrw proc2mngr, x3 > 0x03
    """

def gen_branch_6():
    return """

        csrr x3, mngr2proc < 1
        csrr x1, mngr2proc < 1

        beq x3, x1, hello
        mul x5, x3, x1

    helo:
        beq x3, x1, label_a
        mul x6, x3, x1

    helloworld:
        beq x3, x1, hworld
        mul x7, x3, x1
        
    hello: 
        beq x3, x1, helloworld
        mul x8, x3, x1

    hworld:
        lui x10, 0x00020
        sw  x3, 0(x10)
        mul x12, x3, x1
        lw  x11, 0(x10)

        lui   x10, 0x00000
        addi  x10, x10, 0x020C  
        jalr  x9, x10, 0
        lw   x3, 0(x1)


        mul x9, x3, x1

    label_a:
        addi x3, x3, 0b10
        csrw proc2mngr, x3 > 0x03
    """

def gen_branch_7():
    return """

        csrr x3, mngr2proc < 1
        csrr x1, mngr2proc < 3

      # Taken: skip the first addi/mul
      sw    x3, 0(x3)
      lw    x4, 0(x3)
      blt   x4, x1, hello
      addi  x3, x3, 1          # skipped
      mul   x5, x3, x1         # skipped

    helo:                     # (unused; safe to delete)
      blt  x3, x1, label_a   # not reached
    
    helloworld:
      blt   x3, x1, hworld
      mul   x7, x3, x1
    
    hello:
      blt   x3, x1, helloworld
      mul   x8, x3, x1
    
    hworld:
      lui   x10, 0x00020
      sw    x3, 0(x10)
      mul   x12, x3, x1
      lw    x11, 0(x10)
    
      # Jump to label_a **via label**, not raw address
      jal   x0, label_a
    
      # Any code here is dead (we just jumped)
    
    label_a:
      addi  x3, x3, 0b10     # 1 + 2 -> 3
      csrw  proc2mngr, x3 > 0x03
    """
