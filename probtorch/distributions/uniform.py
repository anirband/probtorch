"""Implements the Uniform distribution."""

import torch
from torch.autograd import Variable
import math
from probtorch.distributions.distribution import *

__all__ = [
    "Uniform"
]

class Uniform(Distribution):
    "The uniform distribution, parameterized by lower and upper."
    def __init__(self, lower = 0.0, upper = 1.0):
        #TODO: needs assert lower<upper
        self._lower = lower
        self._upper = upper
        # TODO: is there a cleaner way to do broadcast sizes?
        super(Uniform, self).__init__((lower+upper).size(),
                                     lower.data.type(),
                                     GradientType.REPARAMETERIZED)
                                     
    @property
    def lower(self):
        return self._lower
    
    @property
    def upper(self):
        return self._upper
    
    @property
    def mean(self):
        return 0.5 * (self._lower + self._upper)

    @property
    def variance(self):
        return (self._upper-self._lower)**2/12.0

    @property
    def std(self):
        return (self._upper-self._lower)/math.sqrt(12.0)

    def sample(self):
        uniform = Variable(torch.rand(self._size)).type(self._type)
        return self._lower + (self._upper-self._lower) * uniform

    def log_prob(self, value):
        mask= Variable((torch.ge(value.data, self._lower.data) \
            & torch.le(value.data, self._upper.data)).type(torch.DoubleTensor))
        return mask * -1.0 * torch.log(self._upper-self._lower) + (1.0 - mask) * self.LOG_0
         