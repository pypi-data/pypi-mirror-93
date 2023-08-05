[![Automated tests status](https://github.com/rsokl/BWSIGrader/workflows/Tests/badge.svg)](https://github.com/rsokl/BWSIGrader/actions?query=workflow%3ATests+branch%3Amain)
![Python version support](https://img.shields.io/badge/python-3.6%20--%203.9-blue.svg)
[![PyPi version](https://img.shields.io/pypi/v/bwsi_grader.svg)](https://pypi.python.org/pypi/bwsi_grader)

# BWSIGrader
Utility functions for grading BWSI-online homework 

Solutions can be viewed [here](https://github.com/CogWorksBWSI/BWSIGrader/tree/master/solutions/src/bwsi_solutions)

Graders can be viewed [here](https://github.com/CogWorksBWSI/BWSIGrader/tree/master/bwsi_grader)

To run the tests, you must install bwsi_solutions. From `BWSIGrader/` run: 
`python solutions/setup.py develop` 

A better, simpler way to run the tests in a rigorous way is to run tox. Simply install tox via:

```shell
pip install tox
``` 

and then run tox from `BWSIGrader/` with the single command:

```shell
tox
```

This will install and build separate virtual environments (one for py36, one for py37 etc) and will do a fresh install of bwsi_grader on them. Then, all of the unit tests will be run. 
