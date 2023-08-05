# This file is part of Hypothesis, which may be found at
# https://github.com/HypothesisWorks/hypothesis/
#
# Most of this work is copyright (C) 2013-2021 David R. MacIver
# (david@drmaciver.com), but it contains contributions by others. See
# CONTRIBUTING.rst for a full list of people who may hold copyright, and
# consult the git log if you need to determine who owns an individual
# contribution.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at https://mozilla.org/MPL/2.0/.
#
# END HEADER

import inspect
import math
from random import Random

import attr

from hypothesis.control import should_note
from hypothesis.internal.conjecture import utils as cu
from hypothesis.internal.reflection import define_function_signature
from hypothesis.reporting import report
from hypothesis.strategies._internal import core as st
from hypothesis.strategies._internal.strategies import SearchStrategy


class HypothesisRandom(Random):
    """A subclass of Random designed to expose the seed it was initially
    provided with."""

    def __init__(self, note_method_calls):
        self.__note_method_calls = note_method_calls

    def __deepcopy__(self, table):
        return self.__copy__()

    def __repr__(self):
        raise NotImplementedError()

    def seed(self, seed):
        raise NotImplementedError()

    def getstate(self):
        raise NotImplementedError()

    def setstate(self, state):
        raise NotImplementedError()

    def _hypothesis_log_random(self, method, kwargs, result):
        if not (self.__note_method_calls and should_note()):
            return

        args, kwargs = convert_kwargs(method, kwargs)

        report(
            "%r.%s(%s) -> %r"
            % (
                self,
                method,
                ", ".join(
                    list(map(repr, args))
                    + ["%s=%r" % (k, v) for k, v in kwargs.items()]
                ),
                result,
            )
        )

    def _hypothesis_do_random(self, method, kwargs):
        raise NotImplementedError()


RANDOM_METHODS = [
    name
    for name in [
        "_randbelow",
        "betavariate",
        "choice",
        "choices",
        "expovariate",
        "gammavariate",
        "gauss",
        "getrandbits",
        "lognormvariate",
        "normalvariate",
        "paretovariate",
        "randint",
        "random",
        "randrange",
        "sample",
        "shuffle",
        "triangular",
        "uniform",
        "vonmisesvariate",
        "weibullvariate",
        "randbytes",
    ]
    if hasattr(Random, name)
]


# Fake shims to get a good signature
def getrandbits(self, n: int) -> int:
    raise NotImplementedError()


def random(self) -> float:
    raise NotImplementedError()


def _randbelow(self, n: int) -> int:
    raise NotImplementedError()


STUBS = {f.__name__: f for f in [getrandbits, random, _randbelow]}


SIGNATURES = {}


def sig_of(name):
    try:
        return SIGNATURES[name]
    except KeyError:
        pass

    target = getattr(Random, name)
    result = inspect.signature(STUBS.get(name, target))
    SIGNATURES[name] = result
    return result


def define_copy_method(name):
    target = getattr(Random, name)

    def implementation(self, **kwargs):
        result = self._hypothesis_do_random(name, kwargs)
        self._hypothesis_log_random(name, kwargs, result)
        return result

    spec = inspect.getfullargspec(STUBS.get(name, target))

    result = define_function_signature(target.__name__, target.__doc__, spec)(
        implementation
    )

    result.__module__ = __name__
    result.__qualname__ = "HypothesisRandom." + result.__name__

    setattr(HypothesisRandom, name, result)


for r in RANDOM_METHODS:
    define_copy_method(r)


@attr.s(slots=True)
class RandomState:
    next_states = attr.ib(default=attr.Factory(dict))
    state_id = attr.ib(default=None)


def state_for_seed(data, seed):
    try:
        seeds_to_states = data.seeds_to_states
    except AttributeError:
        seeds_to_states = {}
        data.seeds_to_states = seeds_to_states

    try:
        state = seeds_to_states[seed]
    except KeyError:
        state = RandomState()
        seeds_to_states[seed] = state

    return state


UNIFORM = st.floats(0, 1)


def normalize_zero(f):
    if f == 0.0:
        return 0.0
    else:
        return f


class ArtificialRandom(HypothesisRandom):
    VERSION = 10 ** 6

    def __init__(self, note_method_calls, data):
        HypothesisRandom.__init__(self, note_method_calls=note_method_calls)
        self.__data = data
        self.__state = RandomState()

    def __repr__(self):
        return "HypothesisRandom(generated data)"

    def __copy__(self):
        result = ArtificialRandom(
            note_method_calls=self._HypothesisRandom__note_method_calls,
            data=self.__data,
        )
        result.setstate(self.getstate())
        return result

    def __convert_result(self, method, kwargs, result):
        if method == "choice":
            return kwargs.get("seq")[result]
        if method in ("choices", "sample"):
            seq = kwargs["population"]
            return [seq[i] for i in result]
        if method == "shuffle":
            seq = kwargs["x"]
            original = list(seq)
            for i, i2 in enumerate(result):
                seq[i] = original[i2]
            return
        return result

    def _hypothesis_do_random(self, method, kwargs):
        if method == "choices":
            key = (method, len(kwargs["population"]), kwargs.get("k"))
        elif method == "choice":
            key = (method, len(kwargs["seq"]))
        elif method == "shuffle":
            key = (method, len(kwargs["x"]))
        else:
            key = (method,) + tuple(sorted(kwargs))

        try:
            result, self.__state = self.__state.next_states[key]
        except KeyError:
            pass
        else:
            return self.__convert_result(method, kwargs, result)

        if method == "_randbelow":
            result = cu.integer_range(self.__data, 0, kwargs["n"] - 1)
        elif method in ("betavariate", "random"):
            result = self.__data.draw(UNIFORM)
        elif method == "uniform":
            a = normalize_zero(kwargs["a"])
            b = normalize_zero(kwargs["b"])
            result = self.__data.draw(st.floats(a, b))
        elif method in ("weibullvariate", "gammavariate"):
            result = self.__data.draw(st.floats(min_value=0.0, allow_infinity=False))
        elif method in ("gauss", "normalvariate"):
            mu = kwargs["mu"]
            result = mu + self.__data.draw(
                st.floats(allow_nan=False, allow_infinity=False)
            )
        elif method == "vonmisesvariate":
            result = self.__data.draw(st.floats(0, 2 * math.pi))
        elif method == "randrange":
            if kwargs["stop"] is None:
                stop = kwargs["start"]
                start = 0
            else:
                start = kwargs["start"]
                stop = kwargs["stop"]

            step = kwargs["step"]
            if start == stop:
                raise ValueError(
                    "empty range for randrange(%d, %d, %d)" % (start, stop, step)
                )

            if step != 1:
                endpoint = (stop - start) // step
                if (start - stop) % step == 0:
                    endpoint -= 1

                i = cu.integer_range(self.__data, 0, endpoint)
                result = start + i * step
            else:
                result = cu.integer_range(self.__data, start, stop - 1)
        elif method == "randint":
            result = cu.integer_range(self.__data, kwargs["a"], kwargs["b"])
        elif method == "choice":
            seq = kwargs["seq"]
            result = cu.integer_range(self.__data, 0, len(seq) - 1)
        elif method == "choices":
            k = kwargs["k"]
            result = self.__data.draw(
                st.lists(
                    st.integers(0, len(kwargs["population"]) - 1),
                    min_size=k,
                    max_size=k,
                )
            )
        elif method == "sample":
            k = kwargs["k"]
            seq = kwargs["population"]

            if k > len(seq) or k < 0:
                raise ValueError(
                    "Sample size %d not in expected range 0 <= k <= %d" % (k, len(seq))
                )

            result = self.__data.draw(
                st.lists(
                    st.sampled_from(range(len(seq))),
                    min_size=k,
                    max_size=k,
                    unique=True,
                )
            )

        elif method == "getrandbits":
            result = self.__data.draw_bits(kwargs["n"])
        elif method == "triangular":
            low = normalize_zero(kwargs["low"])
            high = normalize_zero(kwargs["high"])
            mode = normalize_zero(kwargs["mode"])
            if mode is None:
                result = self.__data.draw(st.floats(low, high))
            elif self.__data.draw_bits(1):
                result = self.__data.draw(st.floats(mode, high))
            else:
                result = self.__data.draw(st.floats(low, mode))
        elif method in ("paretovariate", "expovariate", "lognormvariate"):
            result = self.__data.draw(st.floats(min_value=0.0))
        elif method == "shuffle":
            result = self.__data.draw(st.permutations(range(len(kwargs["x"]))))
        # This is tested for but only appears in 3.9 so doesn't appear in coverage.
        elif method == "randbytes":  # pragma: no cover
            n = kwargs["n"]
            result = self.__data.draw(st.binary(min_size=n, max_size=n))
        else:
            raise NotImplementedError(method)

        new_state = RandomState()
        self.__state.next_states[key] = (result, new_state)
        self.__state = new_state

        return self.__convert_result(method, kwargs, result)

    def seed(self, seed):
        self.__state = state_for_seed(self.__data, seed)

    def getstate(self):
        if self.__state.state_id is not None:
            return self.__state.state_id

        try:
            states_for_ids = self.__data.states_for_ids
        except AttributeError:
            states_for_ids = {}
            self.__data.states_for_ids = states_for_ids

        self.__state.state_id = len(states_for_ids)
        states_for_ids[self.__state.state_id] = self.__state

        return self.__state.state_id

    def setstate(self, state):
        self.__state = self.__data.states_for_ids[state]


DUMMY_RANDOM = Random(0)


def convert_kwargs(name, kwargs):
    kwargs = dict(kwargs)

    signature = sig_of(name)

    bound = signature.bind(DUMMY_RANDOM, **kwargs)
    bound.apply_defaults()

    for k in list(kwargs):
        if (
            kwargs[k] is signature.parameters[k].default
            or signature.parameters[k].kind != inspect.Parameter.KEYWORD_ONLY
        ):
            kwargs.pop(k)

    arg_names = list(signature.parameters)[1:]

    args = []

    for a in arg_names:
        if signature.parameters[a].kind == inspect.Parameter.KEYWORD_ONLY:
            break
        args.append(bound.arguments[a])
        kwargs.pop(a, None)

    while args:
        name = arg_names[len(args) - 1]
        if args[-1] is signature.parameters[name].default:
            args.pop()
        else:
            break  # pragma: no cover  # Only on Python < 3.8

    return (args, kwargs)


class TrueRandom(HypothesisRandom):
    def __init__(self, seed, note_method_calls):
        HypothesisRandom.__init__(self, note_method_calls)
        self.__seed = seed
        self.__random = Random(seed)

    def _hypothesis_do_random(self, method, kwargs):
        args, kwargs = convert_kwargs(method, kwargs)

        return getattr(self.__random, method)(*args, **kwargs)

    def __copy__(self):
        result = TrueRandom(
            seed=self.__seed,
            note_method_calls=self._HypothesisRandom__note_method_calls,
        )
        result.setstate(self.getstate())
        return result

    def __repr__(self):
        return "Random(%r)" % (self.__seed,)

    def seed(self, seed):
        self.__random.seed(seed)
        self.__seed = seed

    def getstate(self):
        return self.__random.getstate()

    def setstate(self, state):
        self.__random.setstate(state)


class RandomStrategy(SearchStrategy):
    def __init__(self, note_method_calls, use_true_random):
        self.__note_method_calls = note_method_calls
        self.__use_true_random = use_true_random

    def do_draw(self, data):
        if self.__use_true_random:
            seed = data.draw_bits(64)
            return TrueRandom(seed=seed, note_method_calls=self.__note_method_calls)
        else:
            return ArtificialRandom(
                note_method_calls=self.__note_method_calls, data=data
            )
