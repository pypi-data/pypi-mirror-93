import numpy as np
import dadi

import importlib
importlib.reload(dadi.Misc)

fs = dadi.Spectrum(np.random.randint(1,10, size=(2+1,2+1)))
#fs.mask[1,1,1] = True

new_fs = dadi.Misc.combine_pops2(fs, [0,1])

print(fs)
print(new_fs)
