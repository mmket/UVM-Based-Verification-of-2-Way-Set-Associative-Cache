#=========================================================================
# simple_score_test.py
#=========================================================================
# This is primarily just for playing around with little assembly code
# sequences.

from lab4_sys.test.harness    import run_score_test
from lab4_sys.SingleCoreSysFL import SingleCoreSysFL
from lab4_sys.SingleCoreSys   import SingleCoreSys

def test( cmdline_opts ):

  prog="""
    csrr x1, mngr2proc < 5
    csrr x2, mngr2proc < 4
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
    csrw proc2mngr, x3 > 9
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
  """

  run_score_test( SingleCoreSysFL, prog, cmdline_opts=cmdline_opts )

