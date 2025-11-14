#=========================================================================
# extra multicore memory tests
#=========================================================================

import random

# Fix the random seed so results are reproducible
random.seed(0xdeadbeef)

from pymtl3 import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """
    csrr x1, mngr2proc < {0x00002000,0x00002004,0x00002008,0x0000200c}
    csrr x2, mngr2proc < {0x0a0b0c0d,0x1a1b1c1d,0x2a2b2c2d,0x3a3b3c3d}
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
    csrw proc2mngr, x3 > {0x0a0b0c0d,0x1a1b1c1d,0x2a2b2c2d,0x3a3b3c3d}

    .data
    .word 0x01020304
    .word 0x11121314
    .word 0x21222324
    .word 0x31323334
  """

# ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Define additional directed and random test cases.
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#-------------------------------------------------------------------------
# CSR test : csrr + csrw
#-------------------------------------------------------------------------

def gen_csr_test():
  return """
    csrr x2, mngr2proc < {1,2,3,4}
    csrw proc2mngr, x2 > {1,2,3,4}
  """

#-------------------------------------------------------------------------
# Reg–Reg test : add, mul
#-------------------------------------------------------------------------

def gen_regreg_test():
  return """
    csrr x1, mngr2proc < {5,10,15,20}
    csrr x2, mngr2proc < {3,4,2,1}

    add x3, x1, x2

    mul x4, x1, x2

    csrw proc2mngr, x3 > {8,14,17,21}
    csrw proc2mngr, x4 > {15,40,30,20}
  """

#-------------------------------------------------------------------------
# Reg–Imm test : addi
#-------------------------------------------------------------------------

def gen_regimm_test():
  return """
    csrr x1, mngr2proc < {100,200,300,400}

    addi x2, x1, 5

    csrw proc2mngr, x2 > {105,205,305,405}
  """

#-------------------------------------------------------------------------
# Memory test : lw, sw (simple)
#-------------------------------------------------------------------------

def gen_memory_test():
  return """
    csrr x1, mngr2proc < {0x00002000,0x00002004,0x00002008,0x0000200c}
    csrr x2, mngr2proc < {0xaa,0xbb,0xcc,0xdd}

    sw x2, 0(x1)

    lw x3, 0(x1)

    csrw proc2mngr, x3 > {0xaa,0xbb,0xcc,0xdd}

    .data
    .word 0
    .word 0
    .word 0
    .word 0
  """

#-------------------------------------------------------------------------
# Branch test : bne
#-------------------------------------------------------------------------

def gen_branch_test():
  return """
csrr x1, mngr2proc < {1,3,4,5}
csrr x2, mngr2proc < {1,2,4,4}

addi x3, x0, 0

bne x1, x2, label_taken

# NOT taken path
addi x3, x3, 1
beq x0, x0, label_end     # unconditional jump

label_taken:
addi x3, x3, 2

label_end:
csrw proc2mngr, x3 > {1,2,1,2}
"""


#-------------------------------------------------------------------------
# Jump test : jal
#-------------------------------------------------------------------------

def gen_jump_test():
  return """
    addi x3, x0, 0

    jal x4, label_jmp
    addi x3, x3, 1     # skipped

  label_jmp:
    addi x3, x3, 2
    addi x3, x3, 3


    csrw proc2mngr, x3 > {5,5,5,5}
  """

#-------------------------------------------------------------------------
# Mixed pipeline stress test
#-------------------------------------------------------------------------

def gen_mixed_test():
  return """
csrr x1, mngr2proc < {10,20,30,40}
csrr x2, mngr2proc < {1,2,3,4}

add  x3, x1, x2
addi x3, x3, 5
mul  x4, x3, x2

sw x4, 0(x1)
lw x5, 0(x1)

bne x5, x4, 8     # branch to fail

addi x6, x5, 1
csrw proc2mngr, x6 > {17, 55, 115, 197}

fail:
addi x6, x0, 0
"""

def gen_random_add_test():
    import random
    random.seed(0xADD123)

    asm = []
    asm.append("")

    # --- Generate 4-core random inputs ------------------------------------

    x1_vals = [ random.randint(0, 50) for _ in range(4) ]
    x2_vals = [ random.randint(0, 50) for _ in range(4) ]

    # Expected results per core
    exp_vals = [ x1_vals[i] + x2_vals[i] for i in range(4) ]

    # --- Load x1 and x2 from manager --------------------------------------

    asm.append(
        f"csrr x1, mngr2proc < {{{x1_vals[0]},{x1_vals[1]},{x1_vals[2]},{x1_vals[3]}}}"
    )
    asm.append(
        f"csrr x2, mngr2proc < {{{x2_vals[0]},{x2_vals[1]},{x2_vals[2]},{x2_vals[3]}}}"
    )

    asm.append("")

    # --- Optional random nops ---------------------------------------------

    for _ in range(random.randint(0,3)):
        asm.append("nop")

    # --- ADD instruction ----------------------------------------------------

    asm.append("add x3, x1, x2")

    # --- Optional random nops after add -----------------------------------

    for _ in range(random.randint(0,3)):
        asm.append("nop")

    asm.append("")

    # --- Send result back to mngr -----------------------------------------

    asm.append(
        f"csrw proc2mngr, x3 > {{{exp_vals[0]},{exp_vals[1]},{exp_vals[2]},{exp_vals[3]}}}"
    )

    # --- return program ----------------------------------------------------
    return "\n".join(asm)

def gen_random_mul_test():
    import random
    random.seed("MUL")

    asm = []
    asm.append("")

    x1_vals = [ random.randint(0, 20) for _ in range(4) ]
    x2_vals = [ random.randint(0, 20) for _ in range(4) ]
    exp_vals = [ x1_vals[i] * x2_vals[i] for i in range(4) ]

    asm.append(
        f"csrr x1, mngr2proc < {{{x1_vals[0]},{x1_vals[1]},{x1_vals[2]},{x1_vals[3]}}}"
    )
    asm.append(
        f"csrr x2, mngr2proc < {{{x2_vals[0]},{x2_vals[1]},{x2_vals[2]},{x2_vals[3]}}}"
    )
    asm.append("")

    for _ in range(random.randint(0,3)):
        asm.append("nop")

    asm.append("mul x3, x1, x2")

    for _ in range(random.randint(0,3)):
        asm.append("nop")

    asm.append(
        f"csrw proc2mngr, x3 > {{{exp_vals[0]},{exp_vals[1]},{exp_vals[2]},{exp_vals[3]}}}"
    )

    return "\n".join(asm)

#-------------------------------------------------------------------------
# ADDI
#-------------------------------------------------------------------------

def gen_random_addi_test():
    import random
    random.seed("ADDI")

    asm = []
    asm.append("")

    x1_vals = [ random.randint(0, 30) for _ in range(4) ]

    # One single immediate for all 4 cores
    imm = random.randint(-10, 10)

    exp_vals = [ x1_vals[i] + imm for i in range(4) ]

    asm.append(
        f"csrr x1, mngr2proc < {{{x1_vals[0]},{x1_vals[1]},{x1_vals[2]},{x1_vals[3]}}}"
    )
    asm.append("")

    asm.append(f"addi x3, x1, {imm}")

    asm.append(
        f"csrw proc2mngr, x3 > {{{exp_vals[0]},{exp_vals[1]},{exp_vals[2]},{exp_vals[3]}}}"
    )

    return "\n".join(asm)