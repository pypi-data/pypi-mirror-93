import numpy as np
import pytest

from group_lasso import _subsampling


@pytest.fixture
def row_lengths():
    def _row_lengths():
        for i in range(2, 20):
            yield 2 ** i - 1

    return _row_lengths


def test_random_row_idxes_correct_size_fraction(row_lengths):
    for row_length in row_lengths():
        for fraction in [0.5, 0.1, 1 / np.sqrt(2)]:
            row_idxes = _subsampling._get_random_row_idxes(
                row_length, fraction, np.random
            )
            assert len(row_idxes) == int(row_length * fraction)


def test_random_row_idxes_correct_size_integer(row_lengths):
    for row_length in row_lengths():
        for num in [5, 10, 1000]:
            if num > row_length:
                continue
            row_idxes = _subsampling._get_random_row_idxes(
                row_length, num, np.random
            )
            assert len(row_idxes) == num


def test_random_row_idxes_fails_at_negative_input(row_lengths):
    for row_length in row_lengths():
        with pytest.raises(ValueError):
            row_idxes = _subsampling._get_random_row_idxes(
                row_length, -0.1, np.random
            )
        with pytest.raises(ValueError):
            row_idxes = _subsampling._get_random_row_idxes(
                row_length, -1, np.random
            )
        with pytest.raises(ValueError):
            row_idxes = _subsampling._get_random_row_idxes(
                row_length, 0, np.random
            )
        with pytest.raises(ValueError):
            row_idxes = _subsampling._get_random_row_idxes(
                row_length, row_length + 1, np.random
            )
        with pytest.raises(ValueError):
            row_idxes = _subsampling._get_random_row_idxes(
                row_length, "invalid", np.random
            )


def test_random_row_idxes_sqrt(row_lengths):
    for row_length in row_lengths():
        row_idxes = _subsampling._get_random_row_idxes(
            row_length, "sqrt", np.random
        )
        assert len(row_idxes) == int(np.sqrt(row_length))


def test_random_row_idxes_unique(row_lengths):
    for row_length in row_lengths():
        row_idxes = _subsampling._get_random_row_idxes(
            row_length, "sqrt", np.random
        )
        assert len(row_idxes) == len(set(row_idxes))


class TestSubsampler:
    def test_subsampling_scheme_1_is_identity(self, row_lengths):
        for row_length in row_lengths():
            subsampler = _subsampling.Subsampler(
                row_length, 1, random_state=np.random.RandomState(None)
            )
            X = np.random.standard_normal((row_length, 5))
            assert np.all(subsampler.subsample(X) == X)
            y = np.random.standard_normal(row_length)
            Xs, ys = subsampler.subsample(X, y)
            assert np.all(X == Xs) and np.all(y == ys)
