"""
implementation of he initializer for pytorch

author: anton feldmann <anton.feldmann@gmail.com>
"""
import math

from torch.nn.init import (_calculate_fan_in_and_fan_out,
                          _no_grad_normal_,
                          _no_grad_uniform_)

# pylint: disable=C0103
def he_uniform_(tensor, gain=1., mode="fan_in"):
    # type: (Tensor, float, str) -> Tensor
    r"""Fills the input `Tensor` with values according to the method
    described in `Delving Deep into Rectifiers: Surpassing Human-Level
    Performance on ImageNet Classification' - Kaiming He, Xiangyu Zhang,
    Shaoqing Ren, Jian Sun (2015), using a uniform
    distribution. The resulting tensor will have values sampled from
    :math:`\mathcal{U}(-a, a)` where

    .. math::
        a = \text{gain} \times \sqrt{\frac{2.0}{\text{fan}}}

    Args:
        tensor: an n-dimensional `torch.Tensor`
        gain: an optional scaling factor
        mode: an optional fan mode specifier

    Examples:
        >>> from apu.ml.initializers.he import he_uniform_
        >>> w = torch.empty(3, 5)
        >>> he_uniform_(w, gain=nn.init.calculate_gain('relu'), mode='fan_in')
    """
    fan_in, fan_out = _calculate_fan_in_and_fan_out(tensor)

    if mode == "fan_out":
        std = gain * math.sqrt(2.0 / float(fan_out))
    else:
        std = gain * math.sqrt(2.0 / float(fan_in))

    a = math.sqrt(3.0) * std

    return _no_grad_uniform_(tensor, -a, a)


def he_normal_(tensor, gain=1., mode="fan_in"):
    # type: (Tensor, float, str) -> Tensor
    r"""Fills the input `Tensor` with values according to the method
    described in `Delving Deep into Rectifiers: Surpassing Human-Level
    Performance on ImageNet Classification' - Kaiming He, Xiangyu Zhang,
    Shaoqing Ren, Jian Sun (2015), using a uniform
    distribution.The resulting tensor will have values sampled from
    :math:`\mathcal{N}(0, \text{std}^2)` where

    .. math::
        \text{std} = \text{gain} \times \sqrt{\frac{2.0}{\text{fan}}}

    Args:
        tensor: an n-dimensional `torch.Tensor`
        gain: an optional scaling factor
        mode: an optional fan mode specifier

    Examples:
        >>> from apu.ml.initializers.he import he_normal_
        >>> w = torch.empty(3, 5)
        >>> he_normal_(w, gain=nn.init.calculate_gain('relu'), mode='fan_in')
    """
    fan_in, fan_out = _calculate_fan_in_and_fan_out(tensor)

    if mode == "fan_out":
        std = gain * math.sqrt(2.0 / float(fan_out))
    else:
        std = gain * math.sqrt(2.0 / float(fan_in))

    return _no_grad_normal_(tensor, 0., std)

he_normal = he_normal_
he_uniform = he_uniform_
