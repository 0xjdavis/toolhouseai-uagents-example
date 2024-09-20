# Code Generator Agent

This is a code generator agent built using Toolhouse.ai and the Fetch.ai uagents. It returns code based on user's query.

## Example input

```python
query="Generate a Python code to print Fibonacci series upto 20"
```

## Example output

```
def fibonacci_series(limit):
    fib_sequence = []
    a, b = 0, 1
    while a <= limit:
        fib_sequence.append(a)
        a, b = b, a + b
    return fib_sequence

# Print Fibonacci series up to 20
print(fibonacci_series(20))
```

1. Install the necessary packages:

   ```bash
   pip install toolhouse requests uagents
   ```


3. Run the agent:
   ```bash
   python code-generator-agent.py
   ```

