# coding=utf-8

from typing import List

import numpy as np
import tensorflow as tf

from deepreg.model import layer, layer_util
from deepreg.model.backbone.interface import Backbone
from deepreg.registry import REGISTRY


@REGISTRY.register_backbone(name="global")
class GlobalNet(Backbone):
    """
    Build GlobalNet for image registration.

    Reference:

    - Hu, Yipeng, et al.
      "Label-driven weakly-supervised learning
      for multimodal deformable image registration,"
      https://arxiv.org/abs/1711.01666
    """

    def __init__(
        self,
        image_size: tuple,
        out_channels: int,
        num_channel_initial: int,
        extract_levels: List[int],
        out_kernel_initializer: str,
        out_activation: str,
        name: str = "GlobalNet",
        **kwargs,
    ):
        """
        Image is encoded gradually, i from level 0 to E.
        Then, a densely-connected layer outputs an affine
        transformation.

        :param image_size: tuple, such as (dim1, dim2, dim3)
        :param out_channels: int, number of channels for the output
        :param num_channel_initial: int, number of initial channels
        :param extract_levels: list, which levels from net to extract
        :param out_kernel_initializer: not used
        :param out_activation: not used
        :param name: name of the backbone.
        :param kwargs: additional arguments.
        """
        super().__init__(
            image_size=image_size,
            out_channels=out_channels,
            num_channel_initial=num_channel_initial,
            out_kernel_initializer=out_kernel_initializer,
            out_activation=out_activation,
            name=name,
            **kwargs,
        )

        # save parameters
        assert out_channels == 3
        self._extract_levels = extract_levels
        self._extract_max_level = max(self._extract_levels)  # E
        self.reference_grid = layer_util.get_reference_grid(image_size)
        self.transform_initial = tf.constant_initializer(
            value=list(np.eye(4, 3).reshape((-1)))
        )
        # init layer variables
        num_channels = [
            num_channel_initial * (2 ** level)
            for level in range(self._extract_max_level + 1)
        ]  # level 0 to E
        self._downsample_blocks = [
            layer.DownSampleResnetBlock(
                filters=num_channels[i], kernel_size=7 if i == 0 else 3
            )
            for i in range(self._extract_max_level)
        ]  # level 0 to E-1
        self._conv3d_block = layer.Conv3dBlock(filters=num_channels[-1])  # level E
        self._dense_layer = layer.Dense(
            units=12, bias_initializer=self.transform_initial
        )

    def call(
        self, inputs: tf.Tensor, training=None, mask=None
    ) -> (tf.Tensor, tf.Tensor):
        """
        Build GlobalNet graph based on built layers.

        :param inputs: image batch, shape = (batch, f_dim1, f_dim2, f_dim3, ch)
        :param training: None or bool.
        :param mask: None or tf.Tensor.
        :return:
            ddf shape = (batch, dim1, dim2, dim3, 3)
            theta shape = (batch, 4, 3)
        """
        # down sample from level 0 to E
        h_in = inputs
        for level in range(self._extract_max_level):  # level 0 to E - 1
            h_in, _ = self._downsample_blocks[level](inputs=h_in, training=training)
        h_out = self._conv3d_block(
            inputs=h_in, training=training
        )  # level E of encoding

        # predict affine parameters theta of shape = (batch, 4, 3)
        theta = self._dense_layer(h_out)
        theta = tf.reshape(theta, shape=(-1, 4, 3))

        # warp the reference grid with affine parameters to output a ddf
        grid_warped = layer_util.warp_grid(self.reference_grid, theta)
        ddf = grid_warped - self.reference_grid
        return ddf, theta
