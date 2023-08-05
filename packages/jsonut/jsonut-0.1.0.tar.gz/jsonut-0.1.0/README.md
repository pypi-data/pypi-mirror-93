#JSONUT
*jsonut* can be used to convert json objects to Python data class objects and vice versa.

## How to Use
### Example
``` python
from dataclasses import dataclass, field
from typing import *

import jsonut

# Sample Dataclass Object
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


# Create an object
# sample_obj = create_sample_object()

# Serialization
serialized = serialize(sample_obj)

# Deserialization
deserialized = deserialize(serialized)
```

## How to Deploy to PyPI
refer with: https://packaging.python.org/tutorials/packaging-projects/