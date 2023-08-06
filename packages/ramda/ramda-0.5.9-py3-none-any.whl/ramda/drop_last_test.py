from ramda.drop_last import drop_last
from ramda.private.asserts import *


def drop_nocurry_test():
    assert_iterables_equal(drop_last(2, [1, 2, 3, 4]), [1, 2])


def drop_curry_test():
    assert_iterables_equal(drop_last(2)([1, 2, 3, 4]), [1, 2])
