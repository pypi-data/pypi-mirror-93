Features
--------

This package provides means to optimize functions. Newtons and gradient descent methods are provided.

Basic Usage
-----------

```python
func = lambda x: x**2 - 15*x +35
func = Optimization_function(func,show = True,method = 'GradientDescent')
func.optimize()
```
