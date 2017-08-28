"""Sets up tests

Configures the logger for use
"""
#                       MIT License
# 
# Copyright (c) 28/08/17 Ennis Massey
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import logging
from os import mkdir

try:
    mkdir("./logs")
except FileExistsError:
    pass

fmt = logging.Formatter("[%(module)s] || %(asctime)s - %(levelname)s : %(module)s.%(funcName)s || %(message)s")
ch = logging.StreamHandler()

ch.setLevel(logging.CRITICAL)

fh = logging.FileHandler("logs/{}.log".format(__package__))

fh.setLevel(logging.INFO)

logger = logging.getLogger(__package__)
logger.setLevel(logging.INFO)
logger.addHandler(ch)
logger.addHandler(fh)
logger.propagate = False

ch.setFormatter(logging.Formatter("%(message)s"))
fh.setFormatter(logging.Formatter("%(message)s"))

logger.info("\033[1mTESTING STARTED\033[0m")

fh.setFormatter(fmt)
ch.setFormatter(fmt)