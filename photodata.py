import config
import os
from debug import debug

# We define the debuger
dbg = debug(os.path.basename(__file__))
dbg.msg('config','path','all_photos',config.PATH)


# Now we will 