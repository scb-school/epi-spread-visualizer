# epi-spread-visualizer
Tool to visualize disease spread based on input data.

![](https://img.shields.io/github/license/scb-school/epi-spread-visualizer)
![](https://img.shields.io/github/issues/scb-school/epi-spread-visualizer)
# Overview
With this library, I am creating a tool that will assist in visualizing the spread of a disease according to an inputted line listing of populations becoming sick over time, translating this data into a map that will change based on a slider simulating the passage of time. My library will use data visualization tools already in place, such as Plotly DASH, as well as some data-processing tools like Python Pandas, combining these two to make the final result.

[![Build Status](https://github.com/scb-school/epi-spread-visualizer/workflows/Build%20Status/badge.svg?branch=main)](https://github.com/scb-school/epi-spread-visualizer/actions?query=workflow%3A%22Build+Status%22)
[![codecov](https://codecov.io/gh/scb-school/epi-spread-visualizer/branch/main/graph/badge.svg)](https://codecov.io/gh/scb-school/epi-spread-visualizer)

## Details
This project is a pure python project using modern tooling. It uses a `Makefile` as a command registry, with the following commands:
- `make`: list available commands
- `make develop`: install and build this library and its dependencies using `pip`
- `make build`: build the library using `setuptools`
- `make lint`: perform static analysis of this library with `flake8` and `black`
- `make format`: autoformat this library using `black`
- `make annotate`: run type checking using `mypy`
- `make test`: run automated tests with `pytest`
- `make coverage`: run automated tests with `pytest` and collect coverage information
- `make dist`: package library for distribution

## Installation
```bash
$ pip3 install epispread
```

## Quick Start
```python
from epispread import EpiSpread

my_epispread_object = EpiSpread(EpiSpread.FILE)
epi_instance.world.to_csv('world.csv', index=False)
epi_instance.plot_all()

