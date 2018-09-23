# (Set Path) ---------------------------- #
import sys
sys.path[0] = '\\'.join(sys.path[0].split('\\')[0:-1])
# (Import Recommended) ------------------ #
from pydatapack import implementations
from pydatapack import snippets
from pydatapack import debug
from pydatapack import *
# --------------------------------------- #

dp = Datapack('Example','Description')



dp.compile()
debug.move_datapack(dp,'(testing-dir)')