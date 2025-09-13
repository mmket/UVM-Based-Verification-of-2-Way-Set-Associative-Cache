#=========================================================================
# ProcAlt_csr_test.py
#=========================================================================
# It is as simple as inheriting from FL tests and change the ProcType.

from lab2_proc.ProcAlt import ProcAlt
from lab2_proc.test.ProcFL_csr_test import Tests as ProcFL_csr_TestsBaseClass

#-------------------------------------------------------------------------
# Tests
#-------------------------------------------------------------------------

class Tests( ProcFL_csr_TestsBaseClass ):

  @classmethod
  def setup_class( cls ):
    cls.ProcType = ProcAlt

