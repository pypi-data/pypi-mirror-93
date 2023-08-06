# pytechecker

![Tests](https://github.com/dcronqvist/pytechecker/workflows/Tests/badge.svg?branch=main)

**Pytechecker** is a utility library for type checking objects against sample objects.

### Table of Contents
* [A simple example](https://github.com/dcronqvist/pytechecker#a-simple-example)
* [Embedded dicts](https://github.com/dcronqvist/pytechecker#embedded-dicts)
* [What about lists?](https://github.com/dcronqvist/pytechecker#what-about-lists)
* [Dicts as list elements](https://github.com/dcronqvist/pytechecker#dicts-as-list-elements)
* [Tuples](https://github.com/dcronqvist/pytechecker#tuples)
* [Dicts and lists in tuples](https://github.com/dcronqvist/pytechecker#dicts-and-lists-in-tuples)

**Pytechecker** works excellently for checking API payloads. For how it can be used for this, [here's an example of how it can be used together with a flask api](https://github.com/dcronqvist/restberry-api/blob/214a5ca5666fa6488344cc5a4aaf14239f68ad05/api/routes/economy/accounts.py#L12-L38).



# Examples

## The gist of it all
Use pip to install **pytechecker** `python3 -m pip install pytechecker`.

Then you simply use the `check` function from the module.
```python
from pytechecker import check

sample = {
    "name": {
        "required": True,
        "allowed_types": [str]
    },
    "age": {
        "required": True,
        "allowed_types": [int]
    }
}

obj = {
    "name": "dcronqvist",
    "age": 21
}

# succ will be True if it passed type checking
# errors will be an array of strings that tell you
# what went wrong during type checking, if succ is False.
succ, errors = check(sample, obj)
```

## A simple example

Let's start by taking a look at a very simple sample object:

```python
{
    "name": {
        "required": True,
        "allowed_types": [str]
    },
    "age": {
        "required": False,
        "allowed_types": [int]
    }
}
```

Here we have defined a **sample object** which has one required key `name` and one optional key `age`. In the sample object we have also specified that the key `name` can only be of the type `str`, and `age` can only be an `int`. Let's see which objects that fit this sample.

```python
{
    "name": "Daniel",
    "age": 21
}
```

Above we have an object which fits the sample object. It's an object which has the required key `name` and the optional key `age`, and they both are their respective required types.

```python
{
    "name": "Daniel"
}
```

Above is an object that still fits the sample object. Since the key `age` is **optional**, we can omit it from the object without it causing it to be unfit.

```python
{
    "age": 21
}
```

The above object does, however, **NOT** fit the sample object. Upon attempting to match the object against the sample, you'll be met with the following error:

`ERROR: Key 'name' is required, but was absent in supplied object.`

We can also look at an example like this:

```python
{
    "name": "Daniel",
    "age": 21.4
}
```

The above object is unfit since one of its keys is of a type that is not allowed for that key. You'll be met with the following error:

`ERROR: On key 'age', expected one of ['int'], got float.`

So there we have it. That's a very simple example of how it works. 

## Embedded dicts

We don't want to be limited to dicts of only one level, so thankfully **pytechecker** can handle virtually infinite levels of dicts in dicts. Let's look at an example.

```python
{
    "tenant": {
        "required": True,
        "allowed_types": [dict],
        "embedded_dict": {
            "name": {
                "required": True,
                "allowed_types": [str]
            },
            "age": {
                "required": True,
                "allowed_types": [int]
            }
        }
    },
    "room": {
        "required": True,
        "allowed_types": [str]
    }
}
```

Above we have a sample object which has a top level key which is allowed to a dict. We can very easily also specify what this embedded dict must look like for it to fit. Let's look at some objects!

```python
{
    "tenant": {
        "name": "Daniel",
        "age": 21
    },
    "room": "RM-212512"
}
```

This is an object which fits, like a glove! We have the key `tenant` which of course is a dict (or object) and then the key `room` which is a string, like specified! We can also see that all keys inside of `tenant` are required, so leaving one out would result in something like the following:

`ERROR: Key 'tenant.age' is required, but was absent in supplied object.`

**Pytechecker** is very nice and also tells you the entire key from top level and down, and won't just say that `age` is missing.

Like said, this works for a virtually infinite amount of dicts in dicts - it's done via recursion!

## What about lists?

Lists are handled very nicely by **pytechecker**. It will go through all elements in the list and type check them for you. You can even have list elements that are dicts, and they'll also be handled! Let's look at a simple example with lists to begin with.

```python
{
    "nums": {
        "required": True,
        "allowed_types": [list],
        "list_element": {
            "allowed_types": [int, float]
        }
    }
}
```
Here we have a sample object with a required key `nums` which must be a `list` of numbers.

```python
{
    "nums": [5, 1.2, 9, 12.4]
}
```

Above here is an object which fits since it has they key `nums` and all elements are of the correct types.

```python
{
    "nums": [5, 1.2, 9, 12.4, "5"]
}
```
Having something like the object above would give an error like the following:

`ERROR: On key 'nums[4]', expected one of ['int', 'float'], got str.`

See that `[4]`? **Pytechecker** also tells you which element(s) that are wrong in a list. If we would have multiple wrong elements:

```python
{
    "nums": [5, "1.2", 9, 12.4, "5"]
}
```

We would get multiple errors like this:

```python
[
    "ERROR: On key 'nums[1]', expected one of ['int', 'float'], got str.", 
    "ERROR: On key 'nums[4]', expected one of ['int', 'float'], got str."
]

```

*Important to note is that all errors that have been shown before this example have also been part of an array, they have just been the only element in that array of errors.*

## Dicts as list elements

```python
{
    "people": {
        "required": True,
        "allowed_types": [list],
        "list_element": {
            "allowed_types": [dict],
            "embedded_dict": {
                "name": {
                    "required": True,
                    "allowed_types": [str]
                },
                "age": {
                    "required": False,
                    "allowed_types": [int]
                }
            }
        }
    }
}
```
Right, so here we have a sample object which contains a key `people` which should contain a list of objects with a required key `name` and optional key `age`. Let's look at some objects.

```python
{
    "people": [
        {
            "name": "Daniel",
            "age": 21
        },
        {
            "name": "John",
            "age": 42
        },
        {
            "name": "Betty"
        }
    ]
}
```
Here is our list of people with their names and optional age. This object fits, so let's look at one that doesn't fit.

```python
{
    "people": [
        {
            "name": "Daniel",
            "age": 21
        },
        {
            "name": "John",
            "age": 42
        },
        {
            "age": 35
        }
    ]
}
```

The person `Betty` now doesn't have a name, instead it only has an age. This will result in the following error:

`ERROR: Key 'people[2].name' is required, but was absent in supplied object.`

Once again, **pytechecker** tells you which of these objects that is unfit, and also what about that object that is unfit.

## Tuples

Tuples are much like lists, and handled a lot like them. However, tuples are specified by type order, so that the supplied object must match type order as well, let's look at an example.

```python
{
    "tuple": {
        "required": True,
        "allowed_types": [tuple],
        "tuple_order": [str, int, int, float]
    }
}
```

Here we have a sample object which specifies a tuple with the specific order of `(str, int, int, float)`. Let's look at objects!

```python
{
    "tuple": ("Hello there!", 5, 2, 1.1)
}
```
There we are, an object which fits the tuple description perfectly. If we, however, were to flip around some values to not be in the same type order:
```python
{
    "tuple": ("Hello there!", 5, 1.1, 2)
}
```
Then we'd be met with the following error:

`ERROR: On key 'tuple', expected tuple with order (str,int,int,float), got tuple with order (str,int,float,int).`

## Dicts and lists in tuples

```python
{
    "tuple": {
        "required": True,
        "allowed_types": [tuple],
        "tuple_order": [list, int, dict],
        "list_element": {
            "allowed_types": [dict],
            "embedded_dict": {
                "name": {
                    "required": True,
                    "allowed_types": [str]
                }
            }
        },
        "embedded_dict": {
            "num": {
                "required": True,
                "allowed_types": [int, float]
            }
        }
    }
}
```
A sample object which should contain a key `tuple`, which also should be a tuple. This tuple should, respectively, contain a `list` of objects, an `int` and a `dict`.

```python
{
    "tuple": (
        [
            {
                "name": "Daniel"
            },
            {
                "name": "John"
            }
        ], 
        5, 
        {
            "num": 25
        }
    )
}
```
The above object fits like a glove!





