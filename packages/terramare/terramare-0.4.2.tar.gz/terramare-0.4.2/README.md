![dragon](docs/emoji.png)

# terramare

[![python: 3.6 | 3.7 | 3.8 | 3.9](https://img.shields.io/badge/python-3.6%20|%203.7%20|%203.8%20|%203.9-blue)](https://www.python.org/)
[![license: MIT](https://img.shields.io/badge/license-MIT-blueviolet.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/pypi/v/terramare)](https://pypi.org/project/terramare/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/terramare)](https://pypistats.org/packages/terramare)
[![docs: pages](https://img.shields.io/badge/docs-pages-blue)](https://tomwatson1024.gitlab.io/terramare/)

[![ci status](https://gitlab.com/tomwatson1024/terramare/badges/master/pipeline.svg)](https://gitlab.com/tomwatson1024/terramare/commits/master)
[![coverage](https://gitlab.com/tomwatson1024/terramare/badges/master/coverage.svg)](https://gitlab.com/tomwatson1024/terramare/commits/master)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)

Automatically construct complex objects from simple Python types.

Highlights:

- **No boilerplate:** `terramare` uses Python's standard type hints to determine how to construct instances of a class;
- **Format-agnostic:** `terramare` takes simple Python types as input - pass it the output from `json.load`, `toml.load`, or `yaml.load`;
- **Non-invasive:** `terramare` requires no modifications to your existing classes and functions beyond standard type hints;

Full documentation available at <https://tomwatson1024.gitlab.io/terramare/>.

## Example

### Deserializing a Simple Class

Consider the following simple class, defined using [`attrs`](https://github.com/python-attrs/attrs) for brevity:

```python
>>> from typing import List
>>> import attr
>>> import terramare

>>> @attr.s(auto_attribs=True)
... class Example:
...     words: List[str]
...
...     def __str__(self):
...         return " ".join(self.words)

```

Deserializing an instance of the class from a dictionary is as simple as:

```python
>>> print(terramare.deserialize_into(Example, {"words": ["hello", "world!"]}))
hello world!

```

### Deserializing a More Complex Class

Consider the `Person` class defined below:

```python
>>> from typing import NamedTuple, NewType, Sequence
>>> import attr
>>> import terramare

    # `terramare` handles NamedTuples
>>> class Location(NamedTuple):
...     longitude: float
...     latitude: float


    # `terramare` handles NewType aliases
>>> JobTitle = NewType("JobTitle", str)


    # `terramare` handles custom classes [experimental]
>>> @terramare.experimental.from_(terramare.experimental.DICT)
... class Occupation:
...     def __init__(self, title: JobTitle, field: str):
...         self.title = title
...         self.field = field
...
...     def __eq__(self, other):
...         if isinstance(other, self.__class__):
...             return vars(self) == vars(other)
...         return False
...
...     def __repr__(self):
...         return "Occupation('{0.title}', '{0.field}')".format(self)


>>> @attr.s(auto_attribs=True)
... class Person:
...     name: str
...     age: int
...     friends: Sequence[str]
...
...     # `terramare` handles complex member variable types
...     location: Location
...     occupation: Occupation

```

Again, deserialization is a single function call:

```python
>>> terramare.deserialize_into(
...     Person,
...     {
...         "name": "Alice",
...         "age": 20,
...         "friends": ["Bob", "Charlie"],
...         "location": [51.5074, 0.1278],
...         "occupation": {"title": "programmer", "field": "technology"}
...     }
... )
Person(name='Alice', age=20, friends=['Bob', 'Charlie'], location=Location(longitude=51.5074, latitude=0.1278), occupation=Occupation('programmer', 'technology'))

```

## Installation

Install using [pip](https://pip.pypa.io/en/stable/):

```bash
pip install terramare
```

## Alternatives

Check out:

- [`pydantic`](https://pydantic-docs.helpmanual.io/) - _"Data validation and settings management using python type annotations"_. A much more mature library also using Python's standard type hints for deserialization that requires a little more integration with your code;
- [`schematics`](https://schematics.readthedocs.io/en/latest/) - _"...combine types into structures, validate them, and transform the shapes of your data based on simple descriptions"_. Uses custom types instead of Python's standard type hints;
- [`cerberus`](https://docs.python-cerberus.org/en/stable/) - _"...provides powerful yet simple and lightweight data validation functionality out of the box and is designed to be easily extensible, allowing for custom validation"_. Schema validation that doesn't change the type of the primitive value.
