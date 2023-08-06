"""
---
title: Batch Normalization
summary: >
 A PyTorch implementations/tutorials of batch normalization.
---

# Batch Normalization

This is a [PyTorch](https://pytorch.org) implementation of Batch Normalization from paper
 [Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift](https://arxiv.org/abs/1502.03167).

### Internal Covariate Shift

The paper defines *Internal Covariate Shift* as the change in the
distribution of network activations due to the change in
network parameters during training.
For example, let's say there are two layers $l_1$ and $l_2$.
During the beginning of the training $l_1$ outputs (inputs to $l_2$)
could be in distribution $\mathcal{N}(0.5, 1)$.
Then, after some training steps it could move to $\mathcal{N}(0.5, 1)$.
This is *internal covariate shift*.

Internal covriate shift will adversely affect training speed because the later layers
($l_2$ in the above example) has to adapt to this shifted distribution.

By stabilizing the distribution batch normalization minimizes the internal covariate shift.

## Normalization

It is known that whitening improves training speed and convergence.
*Whitening* is linearly transforming inputs to have zero mean, unit variance
and be uncorrelated.

### Normalizing outside gradient computation doesn't work

Normalizing outside the gradient computation using pre-computed (detached)
means and variances doesn't work. For instance. (ignoring variance), let
$$\hat{x} = x - \mathbb{E}[x]$$
where $x = u + b$ and $b$ is a trained bias.
and $\mathbb{E}[x]$ is outside gradient computation (pre-computed constant).

Note that $\hat{x}$ has no effect of $b$.
Therefore,
$b$ will increase or decrease based
$\frac{\partial{\mathcal{L}}}{\partial x}$,
and keep on growing indefinitely in each training update.
Paper notes that similar explosions happen with variances.

### Batch Normalization

Whitening is computationally expensive because you need to de-correlate and
the gradients must flow through the full whitening calculation.

The paper introduces simplified version which they call *Batch Normalization*.
First simplification is that it normalizes each feature independently to have
zero mean and unit variance:
$$\hat{x}^{(k)} = \frac{x^{(k)} - \mathbb{E}[x^{(k)}]}{\sqrt{Var[x^{(k)}]}}$$
where $x = (x^{(1)} ... x^{(d)})$ is the $d$-dimensional input.

The second simplification is to use estimates of mean $\mathbb{E}[x^{(k)}]$
and variance $Var[x^{(k)}]$ from the mini-batch
for normalization; instead of calculating the mean and variance across whole dataset.

Normalizing each feature to zero mean and unit variance could effect what the layer
can represent.
As an example paper illustrates that, if the inputs to a sigmoid are normalized
most of it will be within $[-1, 1]$ range where the sigmoid is linear.
To overcome this each feature is scaled and shifted by two trained parameters
$\gamma^{(k)}$ and $\beta^{(k)}$.
$$y^{(k)} =\gamma^{(k)} \hat{x}^{(k)} + \beta^{(k)}$$
where $y^{(k)}$ is the output of of the batch normalization layer.

Note that when applying batch normalization after a linear transform
like $Wu + b$ the bias parameter $b$ gets cancelled due to normalization.
So you can and should omit bias parameter in linear transforms right before the
batch normalization.

Batch normalization also makes the back propagation invariant to the scale of the weights.
And empirically it improves generalization, so it has regularization effects too.

## Inference

We need to know $\mathbb{E}[x^{(k)}]$ and $Var[x^{(k)}]$ in order to
perform the normalization.
So during inference, you either need to go through the whole (or part of) dataset
and find the mean and variance, or you can use an estimate calculated during training.
The usual practice is to calculate an exponential moving average of
mean and variance during training phase and use that for inference.

Here's [the training code](mnist.html) and a notebook for training
a CNN classifier that use batch normalization for MNIST dataset.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lab-ml/nn/blob/master/labml_nn/normalization/batch_norm/mnist.ipynb)
[![View Run](https://img.shields.io/badge/labml-experiment-brightgreen)](https://web.lab-ml.com/run?uuid=98045f04646d11eb806bacde48001122)
"""

import torch
from torch import nn

from labml_helpers.module import Module


class BatchNorm(Module):
    """
    ## Batch Normalization Layer
    """
    def __init__(self, channels: int, *,
                 eps: float = 1e-5, momentum: float = 0.1,
                 affine: bool = True, track_running_stats: bool = True):
        """
        * `channels` is the number of features in the input
        * `eps` is $\epsilon$, used in $\sqrt{Var[x^{(k)}] + \epsilon}$ for numerical stability
        * `momentum` is the momentum in taking the exponential moving average
        * `affine` is whether to scale and shift the normalized value
        * `track_running_stats` is whether to calculate the moving averages or mean and variance

        We've tried to use the same names for arguments as PyTorch `BatchNorm` implementation.
        """
        super().__init__()

        self.channels = channels

        self.eps = eps
        self.momentum = momentum
        self.affine = affine
        self.track_running_stats = track_running_stats
        # Create parameters for $\gamma$ and $\beta$ for scale and shift
        if self.affine:
            self.scale = nn.Parameter(torch.ones(channels))
            self.shift = nn.Parameter(torch.zeros(channels))
        # Create buffers to store exponential moving averages of
        # mean $\mathbb{E}[x^{(k)}]$ and variance $Var[x^{(k)}]$
        if self.track_running_stats:
            self.register_buffer('exp_mean', torch.zeros(channels))
            self.register_buffer('exp_var', torch.ones(channels))

    def __call__(self, x: torch.Tensor):
        """
        `x` is a tensor of shape `[batch_size, channels, *]`.
        `*` could be any (even *) dimensions.
         For example, in an image (2D) convolution this will be
        `[batch_size, channels, height, width]`
        """
        # Keep the original shape
        x_shape = x.shape
        # Get the batch size
        batch_size = x_shape[0]
        # Sanity check to make sure the number of features is same
        assert self.channels == x.shape[1]

        # Reshape into `[batch_size, channels, n]`
        x = x.view(batch_size, self.channels, -1)

        # We will calculate the mini-batch mean and variance
        # if we are in training mode or if we have not tracked exponential moving averages
        if self.training or not self.track_running_stats:
            # Calculate the mean across first and last dimension;
            # i.e. the means for each feature $\mathbb{E}[x^{(k)}]$
            mean = x.mean(dim=[0, 2])
            # Calculate the squared mean across first and last dimension;
            # i.e. the means for each feature $\mathbb{E}[(x^{(k)})^2]$
            mean_x2 = (x ** 2).mean(dim=[0, 2])
            # Variance for each feature $Var[x^{(k)}] = \mathbb{E}[(x^{(k)})^2] - \mathbb{E}[x^{(k)}]^2$
            var = mean_x2 - mean ** 2

            # Update exponential moving averages
            if self.training and self.track_running_stats:
                self.exp_mean = (1 - self.momentum) * self.exp_mean + self.momentum * mean
                self.exp_var = (1 - self.momentum) * self.exp_var + self.momentum * var
        # Use exponential moving averages as estimates
        else:
            mean = self.exp_mean
            var = self.exp_var

        # Normalize $$\hat{x}^{(k)} = \frac{x^{(k)} - \mathbb{E}[x^{(k)}]}{\sqrt{Var[x^{(k)}] + \epsilon}}$$
        x_norm = (x - mean.view(1, -1, 1)) / torch.sqrt(var + self.eps).view(1, -1, 1)
        # Scale and shift $$y^{(k)} =\gamma^{(k)} \hat{x}^{(k)} + \beta^{(k)}$$
        if self.affine:
            x_norm = self.scale.view(1, -1, 1) * x_norm + self.shift.view(1, -1, 1)

        # Reshape to original and return
        return x_norm.view(x_shape)
