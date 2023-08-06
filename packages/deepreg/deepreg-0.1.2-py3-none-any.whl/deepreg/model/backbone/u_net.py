# coding=utf-8


import tensorflow as tf

from deepreg.model import layer
from deepreg.model.backbone.interface import Backbone
from deepreg.registry import REGISTRY


@REGISTRY.register_backbone(name="unet")
class UNet(Backbone):
    """
    Class that implements an adapted 3D UNet.

    Reference:

    - O. Ronneberger, P. Fischer, and T. Brox,
      “U-net: Convolutional networks for biomedical image segmentation,”,
      Lecture Notes in Computer Science, 2015, vol. 9351, pp. 234–241.
      https://arxiv.org/abs/1505.04597
    """

    def __init__(
        self,
        image_size: tuple,
        out_channels: int,
        num_channel_initial: int,
        depth: int,
        out_kernel_initializer: str,
        out_activation: str,
        pooling: bool = True,
        concat_skip: bool = False,
        control_points: (tuple, None) = None,
        name: str = "Unet",
        **kwargs,
    ):
        """
        Initialise UNet.

        :param image_size: (dim1, dim2, dim3), dims of input image.
        :param out_channels: number of channels for the output
        :param num_channel_initial: number of initial channels
        :param depth: input is at level 0, bottom is at level depth
        :param out_kernel_initializer: kernel initializer for the last layer
        :param out_activation: activation at the last layer
        :param pooling: for downsampling, use non-parameterized
                        pooling if true, otherwise use conv3d
        :param concat_skip: when upsampling, concatenate skipped
                            tensor if true, otherwise use addition
        :param control_points: specify the distance between control points (in voxels).
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

        # init layer variables
        num_channels = [num_channel_initial * (2 ** d) for d in range(depth + 1)]

        self._num_channel_initial = num_channel_initial
        self._depth = depth
        self._downsample_blocks = [
            layer.DownSampleResnetBlock(filters=num_channels[d], pooling=pooling)
            for d in range(depth)
        ]
        self._bottom_conv3d = layer.Conv3dBlock(filters=num_channels[depth])
        self._bottom_res3d = layer.Residual3dBlock(filters=num_channels[depth])
        self._upsample_blocks = [
            layer.UpSampleResnetBlock(filters=num_channels[d], concat=concat_skip)
            for d in range(depth)
        ]
        self._output_conv3d = layer.Conv3dWithResize(
            output_shape=image_size,
            filters=out_channels,
            kernel_initializer=out_kernel_initializer,
            activation=out_activation,
        )

        self.resize = (
            layer.ResizeCPTransform(control_points)
            if control_points is not None
            else False
        )
        self.interpolate = (
            layer.BSplines3DTransform(control_points, image_size)
            if control_points is not None
            else False
        )

    def call(self, inputs: tf.Tensor, training=None, mask=None) -> tf.Tensor:
        """
        Builds graph based on built layers.

        :param inputs: shape = [batch, f_dim1, f_dim2, f_dim3, in_channels]
        :param training:
        :param mask:
        :return: shape = [batch, f_dim1, f_dim2, f_dim3, out_channels]
        """

        down_sampled = inputs

        # down sample
        skips = []
        for d_var in range(self._depth):  # level 0 to D-1
            down_sampled, skip = self._downsample_blocks[d_var](
                inputs=down_sampled, training=training
            )
            skips.append(skip)

        # bottom, level D
        up_sampled = self._bottom_res3d(
            inputs=self._bottom_conv3d(inputs=down_sampled, training=training),
            training=training,
        )

        # up sample, level D-1 to 0
        for d_var in range(self._depth - 1, -1, -1):
            up_sampled = self._upsample_blocks[d_var](
                inputs=[up_sampled, skips[d_var]], training=training
            )

        # output
        output = self._output_conv3d(inputs=up_sampled)

        if self.resize:
            output = self.resize(output)
            output = self.interpolate(output)

        return output
