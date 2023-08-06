""" xaview also known as glorot
it is more easy for me because tensorflow uses glorot
"""

from torch.nn.init import (xavier_uniform,
                          xavier_normal)

#simple aliasing
glorot_normal = xavier_uniform
glorot_unified = xavier_normal
