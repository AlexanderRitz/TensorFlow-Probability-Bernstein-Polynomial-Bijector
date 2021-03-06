#!env python3
# AUTHOR INFORMATION ##########################################################
# file    : test_bernstein_bijector.py
# brief   : [Description]
#
# author  : Marcel Arpogaus
# created : 2020-10-16 08:12:04
# changed : 2020-11-23 18:03:28
# DESCRIPTION #################################################################
#
# This project is following the PEP8 style guide:
#
#    https://www.python.org/dev/peps/pep-0008/)
#
# LICENSE #####################################################################
# Copyright 2020 Marcel Arpogaus
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################

# REQUIRED PYTHON MODULES #####################################################
import numpy as np
import tensorflow as tf

from bernstein_flow.bijectors import BernsteinBijector


class BernsteinBijectorTest(tf.test.TestCase):

    def test_inverse(self,
                     batch_shape=[],
                     x_shape=[100],
                     order=10):
        theta = BernsteinBijector.constrain_theta(
            np.ones(batch_shape + [order]).astype(np.float32)
        )
        print(theta)
        x = np.float32(np.random.uniform(
            0 + 1E-2,
            1 - 1E-2,
            x_shape))

        bb = BernsteinBijector(
            theta=theta
        )

        forward_x = bb.forward(x)
        # Use identity to invalidate cache.
        inverse_x = bb.inverse(tf.identity(forward_x))
        forward_inverse_x = bb.forward(inverse_x)

        fldj = bb.forward_log_det_jacobian(x, event_ndims=1)
        # Use identity to invalidate cache.
        ildj = bb.inverse_log_det_jacobian(
            tf.identity(forward_x), event_ndims=1)

        self.assertAllClose(x, inverse_x, rtol=1e-5, atol=1e-4)
        self.assertAllClose(forward_x, forward_inverse_x, rtol=1e-5, atol=1e-4)
        self.assertAllClose(ildj, -fldj, rtol=1e-5, atol=0.)

    def test_inverse_batched(self):
        self.test_inverse(batch_shape=[2],
                          x_shape=[100, 2])

    def test_inverse_batched_multi(self):
        self.test_inverse(batch_shape=[2, 4],
                          x_shape=[100, 2, 4])

    def test_inverse_batched_multi_huge(self):
        self.test_inverse(batch_shape=[16, 48],
                          x_shape=[100, 16, 48])
