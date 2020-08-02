# Quantum calculator

A `%quantum` magic command for evaluating basic quantum circuit calculations using `numpy`. Conveniently displays vector data in dirac notation and pretty prints array values as squares and fractions where possible.

## Example usage

```python
import quantum
%quantum X0 |0>
```

|1>

### Bell state

```python
%quantum CX01 H0 |00>
```

1/√2 |00> + 1/√2 |11>

### Multi-qubit gates

```python
# Index zero starts from left
%quantum X0 X2 X4 |000000>
```

|101010>

#### Kronecker product

```python
%quantum X0*X1*X2
```

[farray([\
[0, 0, 0, 0, 0, 0, 0, 1],\
[0, 0, 0, 0, 0, 0, 1, 0],\
[0, 0, 0, 0, 0, 1, 0, 0],\
[0, 0, 0, 0, 1, 0, 0, 0],\
[0, 0, 0, 1, 0, 0, 0, 0],\
[0, 0, 1, 0, 0, 0, 0, 0],\
[0, 1, 0, 0, 0, 0, 0, 0],\
[1, 0, 0, 0, 0, 0, 0, 0]\
])]

## Run examples

See [notebooks/example.ipynb](notebooks/example.ipynb) for more examples.

### Generate README.ipynb

To generate a Jupyter notebook from this README.md file, run

```markdown
pip install jupytext
jupytext README.md --to ipynb --output notebooks/README.ipynb
```
