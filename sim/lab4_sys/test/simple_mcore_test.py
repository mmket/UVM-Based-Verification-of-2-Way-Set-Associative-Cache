#=========================================================================
# simple_mcore_test.py
#=========================================================================
# This is primarily just for playing around with little assembly code
# sequences.

from lab4_sys.test.harness   import run_mcore_test
from lab4_sys.MultiCoreSysFL import MultiCoreSysFL
from lab4_sys.MultiCoreSys   import MultiCoreSys

def test( cmdline_opts ):

  prog="""
    csrr x1, mngr2proc < { 5, 6, 7, 8 }
    csrr x2, mngr2proc < { 4, 5, 6, 7 }
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    add x3, x1, x2
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > { 9, 11, 13, 15 }
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
  """

  run_mcore_test( MultiCoreSysFL, prog, cmdline_opts=cmdline_opts )

