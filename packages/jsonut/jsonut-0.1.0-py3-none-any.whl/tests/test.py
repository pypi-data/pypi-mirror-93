from __future__ import annotations

# noinspection SpellCheckingInspection
__author__ = 'wookjae.jo'

import unittest
from dataclasses import dataclass, field
from typing import *

import jsonut


@dataclass
class SampleObject(jsonut.JsonSerializable):
    name: str = field(default_factory=str)
    numbers: List[int] = field(default_factory=list)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        if self.name != other.name:
            return False

        if self.numbers != other.numbers:
            return False

        return True


class MyTestCase(unittest.TestCase):

    @classmethod
    def create_sample_object(cls):
        return SampleObject(name='sample',
                            numbers=[1, 2, 3])

    def test(self):
        sample_obj = self.create_sample_object()
        serialized = sample_obj.serialize()
        deserialized = jsonut.deserialize(serialized, SampleObject)
        self.assert_(sample_obj == deserialized)


if __name__ == '__main__':
    unittest.main()
