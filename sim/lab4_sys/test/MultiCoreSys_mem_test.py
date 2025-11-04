#=========================================================================
# MultiCoreSys_mem_test.py
#=========================================================================
# It is as simple as inheriting from FL tests and change the SysType.

from lab4_sys.MultiCoreSys import MultiCoreSys
from lab4_sys.test.MultiCoreSysFL_mem_test import Tests as MultiCoreSysFL_mem_TestsBaseClass

#-------------------------------------------------------------------------
# Tests
#-------------------------------------------------------------------------

class Tests( MultiCoreSysFL_mem_TestsBaseClass ):

  @classmethod
  def setup_class( cls ):
    cls.SysType = MultiCoreSys

