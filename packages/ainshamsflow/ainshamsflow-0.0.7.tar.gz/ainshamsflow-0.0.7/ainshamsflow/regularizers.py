"""Regularizers Module.

In this Module, we include our Regularizers such as L1 and L2.
"""

import numpy as np

from ainshamsflow.utils.asf_errors import BaseClassError, NameNotFoundError


def get(reg_name):
	"""Get any Regularizer in this Module by name."""

	regs = [L2, L1, L1_L2]
	for reg in regs:
		if reg.__name__.lower() == reg_name.lower():
			return reg()
	else:
		raise NameNotFoundError(reg_name, __name__)


class Regularizer:
	"""Regularizer Base Class.

	Used to define Regularizer Interface.

	To create a new Regularizer, create a class that inherits from
	this class.
	You then have to add any extra parameters in your constructor
	(while still calling this class' constructor) and redefining
	the __call__() and diff() methods.
	"""

	def __init__(self, lambd=0.01):
		"""Initialize Lambda."""

		self.lambd = lambd

	def __call__(self, weights_list, m):
		raise BaseClassError

	def diff(self, weights_list, m):
		raise BaseClassError


class L2(Regularizer):
	"""L2 Reguarizer."""

	__name__ = 'L2'

	def __call__(self, weights_list, m):
		if isinstance(weights_list, list):
			ans = 0
			for weights in weights_list:
				ans += self.__call__(weights, m)
			return ans
		else:
			return self.lambd * np.sum(np.square(weights_list)) / (2*m)

	def diff(self, weights_list, m):
		if isinstance(weights_list, list):
			ans = []
			for weights in weights_list:
				ans.append(self.diff(weights, m))
			return ans
		else:
			return self.lambd * np.divide(weights_list, m)


class L1(Regularizer):
	"""L1 Regularizer."""

	__name__ = 'L1'

	def __call__(self, weights_list, m):
		if isinstance(weights_list, list):
			ans = 0
			for weights in weights_list:
				ans += self.__call__(weights, m)
			return ans
		else:
			return self.lambd * np.sum(np.abs(weights_list)) / m

	def diff(self, weights_list, m):
		if isinstance(weights_list, list):
			ans = []
			for weights in weights_list:
				ans.append(self.diff(weights, m))
			return ans
		else:
			return self.lambd * np.divide(np.where(weights_list > 0, 1, -1), m)


class L1_L2(Regularizer):
	"""L1_L2 Regularizer."""

	__name__ = 'L1_L2'

	def __init__(self, l1=0.01, l2=0.01):
		super().__init__()
		self.l1_reg = L1(l1)
		self.l2_reg = L2(l2)

	def __call__(self, weights_list, m):
		return self.l1_reg(weights_list, m) + self.l2_reg(weights_list, m)

	def diff(self, weights_list, m):
		if isinstance(weights_list, list):
			ans = []
			for weights in weights_list:
				ans.append(self.diff(weights, m))
			return ans
		else:
			return self.l1_reg.diff(weights_list, m) + self.l2_reg.diff(weights_list, m)
