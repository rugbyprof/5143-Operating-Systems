## Args & Kwargs

Let's dive into the world of Python function arguments: `args` and `kwargs`. These concepts are incredibly useful when you want to create flexible functions that can handle different numbers of arguments and keyword arguments. Here's an overview along with examples and usage scenarios for both `args` and `kwargs`.

### `args`: Variable-Length Positional Arguments

`*args` is a special syntax that allows a function to accept a variable number of positional arguments. These arguments are collected into a tuple, which you can then iterate over or access like a regular tuple.

**Example:**

```python
def calculate_sum(*args):
    total = sum(args)
    return total

result = calculate_sum(1, 2, 3, 4, 5)
print(result)  # Output: 15
```

**Usage:**

- When you want to create a function that can take any number of arguments without specifying them beforehand.
- Useful when you need to pass a varying number of values to a function.

### `kwargs`: Variable-Length Keyword Arguments

`**kwargs` allows a function to accept a variable number of keyword arguments, which are collected into a dictionary. This gives you the flexibility to pass named arguments to a function without needing to specify them in advance.

**Example:**

```python
def display_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

display_info(name="Alice", age=30, location="Texas")
```

**Usage:**

- When you want to pass named arguments to a function without knowing all possible arguments in advance.
- Useful when you need to provide configuration settings or options to a function.

### Combining `args` and `kwargs`

You can use both `*args` and `**kwargs` in a function signature to create a highly flexible function that can handle both positional and keyword arguments.

**Example:**

```python
def flexible_function(arg1, *args, kwarg1="default", **kwargs):
    print("Fixed argument:", arg1)
    print("Additional arguments:", args)
    print("Keyword argument:", kwarg1)
    print("Additional keyword arguments:", kwargs)

flexible_function("fixed", "extra1", "extra2", kwarg1="custom", key1="value1", key2="value2")
```

**Usage:**

- When you need to create functions that can handle a mix of fixed, variable, and keyword arguments.
- Useful for creating generic utility functions or API endpoints.

In summary, `args` and `kwargs` provide powerful ways to create flexible functions that can handle various input scenarios. Whether you're dealing with unknown numbers of arguments or keyword-based configurations, these concepts allow your Python functions to adapt to different use cases. So go ahead, leverage `args` and `kwargs` to write more versatile and reusable code! 