import inspect

def example_function(a, b=2, *args, **kwargs):
    """This is an example function."""
    return a + b

# Get function name
name = example_function.__name__

# Get docstring
docstring = inspect.getdoc(example_function)

# Get signature (arguments and defaults)
signature = str(inspect.signature(example_function))

# Get source code (optional)
source = inspect.getsource(example_function)

# Print all
print(f"Name: {name}")
print(f"Signature: {signature}")
print(f"Docstring: {docstring}")
print(f"Source:\n{source}")
