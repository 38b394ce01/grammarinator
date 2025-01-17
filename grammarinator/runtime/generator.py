# Copyright (c) 2017-2021 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

from math import inf

from .default_model import DefaultModel


def depthcontrol(fn):
    def controlled_fn(obj, *args, **kwargs):
        obj._max_depth -= 1
        try:
            result = fn(obj, *args, **kwargs)
        finally:
            obj._max_depth += 1
        return result

    controlled_fn.__name__ = fn.__name__
    return controlled_fn


class Generator(object):

    def __init__(self, *, model=None, max_depth=inf):
        self._model = model or DefaultModel()
        self._max_depth = max_depth
        self._listeners = []

    def _enter_rule(self, node):
        for listener in self._listeners:
            listener.enter_rule(node)

    def _exit_rule(self, node):
        for listener in reversed(self._listeners):
            listener.exit_rule(node)
