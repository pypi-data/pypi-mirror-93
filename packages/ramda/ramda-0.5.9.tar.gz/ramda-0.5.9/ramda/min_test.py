from .min import min
from ramda.private.asserts import assert_equal


def min_test():
    assert_equal(min(3, 1), 1)
