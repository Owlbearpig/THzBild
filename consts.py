from pathlib import Path
import os
import numpy as np
from scipy.constants import c as c0
from numpy import pi, inf

cur_os = os.name

um = 10**-6
THz = 10 ** 12

ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

if 'posix' in cur_os:
    data_dir = Path(r"/home/alex/Data/THzBild")
else:
    data_dir = Path(r"E:\measurementdata\THzBild")