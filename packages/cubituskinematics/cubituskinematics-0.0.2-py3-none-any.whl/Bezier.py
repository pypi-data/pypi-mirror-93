import numpy as np

class Base(object):
    __slots__ = ("_dimension", "_nodes")
    _degree = -1

    def __init__(self, nodes, copy=True):
        nodes_np = self.__sequence_to_array(nodes)
        dimension, _ = nodes_np.shape
        self._dimension = dimension
        if copy: self._nodes = nodes_np.copy(order="F")
        else: self._nodes = nodes_np

    @property
    def nodes(self):
        return self._nodes.copy(order="F")

    def __repr__(self):
        return "<{} (degree={:d}, dimension={:d})>".format(self.__class__.__name__, self._degree, self._dimension)

    def __lossless_to_float(self, array):
        if array.dtype == np.float64:
            return array
        converted = array.astype(np.float64)
        if not np.all(array == converted):
            raise ValueError("Array cannot be converted to floating point")
        return converted

    def __sequence_to_array(self, nodes):
        nodes_np = np.asarray(nodes, order="F")
        if nodes_np.ndim != 2:
            raise ValueError("Nodes must be 2-dimensional, not", nodes_np.ndim)
        return self.__lossless_to_float(nodes_np)

class Curve(Base):
    __slots__ = (
        "_dimension",
        "_nodes",
        "_degree",
    )

    def __init__(self, nodes, degree, *, copy=True, verify=True):
        super(Curve, self).__init__(nodes, copy=copy)
        self._degree = degree
        self._verify_degree(verify)

    def _verify_degree(self, verify):
        if not verify:
            return
        _, num_nodes = self._nodes.shape
        expected_nodes = self._degree + 1
        if expected_nodes == num_nodes:
            return
        msg = (f"A degree {self._degree} curve should have "f"{expected_nodes} nodes, not {num_nodes}.")
        raise ValueError(msg)

    def evaluate(self, s):
        return self.evaluate_multi(self._nodes, np.asfortranarray([s]))

    def evaluate_multi(self, nodes, s_vals):
        one_less = 1.0 - s_vals
        return self.evaluate_multi_barycentric(nodes, one_less, s_vals)

    def evaluate_multi_barycentric(self, nodes, lambda1, lambda2):
        (num_vals,) = lambda1.shape
        dimension, num_nodes = nodes.shape
        degree = num_nodes - 1
        lambda1 = lambda1[np.newaxis, :]
        lambda2 = lambda2[np.newaxis, :]
        result = np.zeros((dimension, num_vals), order="F")
        result += lambda1 * nodes[:, [0]]
        binom_val = 1.0
        lambda2_pow = np.ones((1, num_vals), order="F")
        for index in range(1, degree):
            lambda2_pow *= lambda2
            binom_val = (binom_val * (degree - index + 1)) / index
            result += binom_val * lambda2_pow * nodes[:, [index]]
            result *= lambda1
        result += lambda2 * lambda2_pow * nodes[:, [degree]]
        return result
