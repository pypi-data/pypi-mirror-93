# -*- coding: utf-8 -*-
#
# This file is part of SIDEKIT.
#
# SIDEKIT is a python package for speaker verification.
# Home page: http://www-lium.univ-lemans.fr/sidekit/
#
# SIDEKIT is a python package for speaker verification.
# Home page: http://www-lium.univ-lemans.fr/sidekit/
#
# SIDEKIT is free software: you can redistribute it and/or modify
# it under the terms of the GNU LLesser General Public License as
# published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# SIDEKIT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with SIDEKIT.  If not, see <http://www.gnu.org/licenses/>.

"""
Copyright 2014-2021 Anthony Larcher and Sylvain Meignier

:mod:`nnet` provides methods to manage Neural Networks using PyTorch
"""


from .augmentation import AddNoise
from .feed_forward import FForwardNetwork
from .feed_forward import kaldi_to_hdf5
from .xsets import XvectorMultiDataset, XvectorDataset, StatDataset
from .xvector import Xtractor, xtrain, extract_embeddings, extract_sliding_embedding
from .res_net import ResBlock, ResNet18
from .rawnet import prepare_voxceleb1, Vox1Set, PreEmphasis
from .sincnet import SincNet

has_pyroom = True
try:
   import pyroomacoustics
except ImportError:
   has_pyroom = False

if has_pyroom:
    from .augmentation import AddReverb


__author__ = "Anthony Larcher and Sylvain Meignier"
__copyright__ = "Copyright 2014-2021 Anthony Larcher and Sylvain Meignier"
__license__ = "LGPL"
__maintainer__ = "Anthony Larcher"
__email__ = "anthony.larcher@univ-lemans.fr"
__status__ = "Production"
__docformat__ = 'reStructuredText'
