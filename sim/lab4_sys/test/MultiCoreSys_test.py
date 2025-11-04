#=========================================================================
# MultiCoreSys_test.py
#=========================================================================
# It is as simple as inheriting from FL tests and change the SysType.

from lab4_sys.MultiCoreSys import MultiCoreSys
from lab4_sys.test.MultiCoreSysFL_test import Tests as MultiCoreSysFL_TestsBaseClass

#-------------------------------------------------------------------------
# Tests
#-------------------------------------------------------------------------

class Tests( MultiCoreSysFL_TestsBaseClass ):

  @classmethod
  def setup_class( cls ):
    cls.SysType = MultiCoreSys

