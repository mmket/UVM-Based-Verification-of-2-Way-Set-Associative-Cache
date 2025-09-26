#=========================================================================
# bltu
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

    # Use x3 to track the control flow pattern
    addi  x3, x0, 0

    csrr  x1, mngr2proc < 2
    csrr  x2, mngr2proc < 1

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

    # This branch should be taken
    bltu   x2, x1, label_a
    addi  x3, x3, 0b01

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

    # Only the second bit should be set if branch was taken
    csrw proc2mngr, x3 > 0b10

  """

def gen_src0_dep_taken_test():
  return [
    gen_br2_src0_dep_test( 5, "bltu", 1, 7, True ),  
    gen_br2_src0_dep_test( 4, "bltu", 1, 2, True ),  
    gen_br2_src0_dep_test( 3, "bltu", 1, 3, True ),  
    gen_br2_src0_dep_test( 2, "bltu", 1, 4, True ),  
    gen_br2_src0_dep_test( 1, "bltu", 1, 5, True ),  
    gen_br2_src0_dep_test( 0, "bltu", 1, 6, True ),  
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_src0_dep_nottaken_test():
  return [
    gen_br2_src0_dep_test( 5, "bltu", 7, 1, False ),
    gen_br2_src0_dep_test( 4, "bltu", 7, 2, False ),
    gen_br2_src0_dep_test( 3, "bltu", 7, 3, False ),
    gen_br2_src0_dep_test( 2, "bltu", 7, 4, False ),
    gen_br2_src0_dep_test( 1, "bltu", 7, 5, False ),
    gen_br2_src0_dep_test( 0, "bltu", 7, 6, False ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_taken_test
#-------------------------------------------------------------------------

def gen_src1_dep_taken_test():
  return [
    gen_br2_src1_dep_test( 5, "bltu", 1, 7, True ),
    gen_br2_src1_dep_test( 4, "bltu", 1, 2, True ),
    gen_br2_src1_dep_test( 3, "bltu", 1, 3, True ),
    gen_br2_src1_dep_test( 2, "bltu", 1, 4, True ),
    gen_br2_src1_dep_test( 1, "bltu", 1, 5, True ),
    gen_br2_src1_dep_test( 0, "bltu", 1, 6, True ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_src1_dep_nottaken_test():
  return [
    gen_br2_src1_dep_test( 5, "bltu", 7, 1, False ),
    gen_br2_src1_dep_test( 4, "bltu", 7, 2, False ),
    gen_br2_src1_dep_test( 3, "bltu", 7, 3, False ),
    gen_br2_src1_dep_test( 2, "bltu", 7, 4, False ),
    gen_br2_src1_dep_test( 1, "bltu", 7, 5, False ),
    gen_br2_src1_dep_test( 0, "bltu", 7, 6, False ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_taken_test
#-------------------------------------------------------------------------

def gen_srcs_dep_taken_test():
  return [
    gen_br2_srcs_dep_test( 5, "bltu", 1, 2, True ),
    gen_br2_srcs_dep_test( 4, "bltu", 2, 3, True ),
    gen_br2_srcs_dep_test( 3, "bltu", 3, 4, True ),
    gen_br2_srcs_dep_test( 2, "bltu", 4, 5, True ),
    gen_br2_srcs_dep_test( 1, "bltu", 5, 6, True ),
    gen_br2_srcs_dep_test( 0, "bltu", 6, 7, True ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_srcs_dep_nottaken_test():
  return [
    gen_br2_srcs_dep_test( 5, "bltu", 2, 1, False ),
    gen_br2_srcs_dep_test( 4, "bltu", 3, 2, False ),
    gen_br2_srcs_dep_test( 3, "bltu", 4, 3, False ),
    gen_br2_srcs_dep_test( 2, "bltu", 5, 4, False ),
    gen_br2_srcs_dep_test( 1, "bltu", 6, 5, False ),
    gen_br2_srcs_dep_test( 0, "bltu", 7, 6, False ),
  ]

#-------------------------------------------------------------------------
# gen_src0_eq_src1_nottaken_test
#-------------------------------------------------------------------------


def gen_src0_eq_src1_test():
  return [
    gen_br2_src0_eq_src1_test( "bltu", 5, False ),  
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_br2_value_test( "bltu",  0,  1, True  ),   
 
    gen_br2_value_test( "bltu",  1,  0, False ),   

    gen_br2_value_test( "bltu", 9,  2147483647, True  ),   
    gen_br2_value_test( "bltu", 2147483647, 9, False ),    
  ]


#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in range(25):
    src0 = b32( random.randint(0,0xffffffff) )
    src1 = b32( random.randint(0,0xffffffff) )

    taken = (src0.uint() < src1.uint())

    asm_code.append( gen_br2_value_test( "bltu", src0.uint(), src1.uint(), taken ) )

  return asm_code

#-------------------------------------------------------------------------
# gen_back_to_back_test
#-------------------------------------------------------------------------

def gen_back_to_back_test():
  return """
     # Test backwards walk (back to back branch taken)

     csrr x3, mngr2proc < 0   # x3 = 0
     csrr x1, mngr2proc < 1   # x1 = 1

     bltu  x3, x1, X0
     csrw proc2mngr, x0
     nop
     a0:
     csrw proc2mngr, x1 > 1
     bltu  x3, x1, y0
     b0:
     bltu  x3, x1, a0
     c0:
     bltu  x3, x1, b0
     d0:
     bltu  x3, x1, c0
     e0:
     bltu  x3, x1, d0
     f0:
     bltu  x3, x1, e0
     g0:
     bltu  x3, x1, f0
     h0:
     bltu  x3, x1, g0
     i0:
     bltu  x3, x1, h0
     X0:
     bltu  x3, x1, i0
     y0:
     bltu  x3, x1, X1
     csrw proc2mngr, x0
     nop
     a1:
     csrw proc2mngr, x1 > 1
     bltu  x3, x1, y1
     b1:
     bltu  x3, x1, a1
     c1:
     bltu  x3, x1, b1
     d1:
     bltu  x3, x1, c1
     e1:
     bltu  x3, x1, d1
     f1:
     bltu  x3, x1, e1
     g1:
     bltu  x3, x1, f1
     h1:
     bltu  x3, x1, g1
     i1:
     bltu  x3, x1, h1
     X1:
     bltu  x3, x1, i1
     y1:
    
     bltu  x3, x1, X2
     csrw proc2mngr, x0
     nop
     a2:
     csrw proc2mngr, x1 > 1
     bltu  x3, x1, y2
     b2:
     bltu  x3, x1, a2
     c2:
     bltu  x3, x1, b2
     d2:
     bltu  x3, x1, c2
     e2:
     bltu  x3, x1, d2
     f2:
     bltu  x3, x1, e2
     g2:
     bltu  x3, x1, f2
     h2:
     bltu  x3, x1, g2
     i2:
     bltu  x3, x1, h2
     X2:
     bltu  x3, x1, i2
     y2:
     bltu  x3, x1, X3
     csrw proc2mngr, x0
     nop
     a3:
     csrw proc2mngr, x1 > 1
     bltu  x3, x1, y3
     b3:
     bltu  x3, x1, a3
     c3:
     bltu  x3, x1, b3
     d3:
     bltu  x3, x1, c3
     e3:
     bltu  x3, x1, d3
     f3:
     bltu  x3, x1, e3
     g3:
     bltu  x3, x1, f3
     h3:
     bltu  x3, x1, g3
     i3:
     bltu  x3, x1, h3
     X3:
     bltu  x3, x1, i3
     y3:
     nop
     nop
     nop
     nop
     nop
     nop
     nop
      """
    