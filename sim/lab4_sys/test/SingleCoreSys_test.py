#=========================================================================
# SingleCoreSys_test.py
#=========================================================================
# It is as simple as inheriting from FL tests and change the SysType.

from lab4_sys.SingleCoreSys import SingleCoreSys
from lab4_sys.test.SingleCoreSysFL_test import Tests as SingleCoreSysFL_TestsBaseClass

#-------------------------------------------------------------------------
# Tests
#-------------------------------------------------------------------------

class Tests( SingleCoreSysFL_TestsBaseClass ):

  @classmethod
  def setup_class( cls ):
    cls.SysType = SingleCoreSys

