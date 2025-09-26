#=========================================================================
# jal
#=========================================================================

from pymtl3 import *
from lab2_proc.test.inst_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """

    # Use r3 to track the control flow pattern
    addi  x3, x0, 0     
                        
    nop                 
    nop                 
    nop                 
    nop                 
    nop                 
    nop                 
    nop                 
    nop                 
                        
    jal   x1, label_a   
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

    # Check the link address
    csrw  proc2mngr, x1 > 0x0228

    # Only the second bit should be set if jump was taken
    csrw  proc2mngr, x3 > 0b10

  """

def gen_multijump_test():
  return """
 
  addi x3, x0, 0 
 
  jal x1, label_a 
  addi x3, x3, 0b000001 
  
   label_b: 
   addi x3, x3, 0b000010 
   addi x5, x1, 0 
   jal x1, label_c 
   addi x1, x3, 0b000100 
  
   label_a:
   addi x3, x3, 0b001000 
   addi x4, x1, 0 
   jal x1, label_b 
   addi x3, x3, 0b010000 
  
   label_c: 
   addi x3, x3, 0b100000 
   addi x6, x1, 0 
  
   csrw proc2mngr, x3 > 0b101010
  
   csrw proc2mngr, x4 > 0x00000208
   csrw proc2mngr, x5 > 0x00000228
   csrw proc2mngr, x6 > 0x00000218
   """ 

def gen_data_test():
  return """

    # Use r3 to track the control flow pattern
    addi  x3, x0, 0     
                        
                        
    jal   x1, label_a   
    addi  x3, x3, 0b01  


  label_a:
    addi  x3, x3, 0b10

    # Check the link address
    csrw  proc2mngr, x1 > 0x0208

    # Only the second bit should be set if jump was taken
    csrw  proc2mngr, x3 > 0b10

  """
def gen_back_to_back_test():
  return """

    addi  x3, x0, 0

    jal   x1, label_b            

  label_b:
    csrw  proc2mngr, x1 > 0x0208

    addi  x3, x3, 1
    csrw  proc2mngr, x3 > 0x1
  """
#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------
def gen_random_test():
  asm_code = []
  for i in range(20):
    offset = (i+1) * 4   
    asm_code.append(f"jal x1, {offset}")
    asm_code.append("nop")
    asm_code.append("nop")
  return "\n".join(asm_code)
