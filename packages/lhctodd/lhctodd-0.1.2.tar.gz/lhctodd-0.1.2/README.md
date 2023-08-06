# LHCToDD

[![Documentation Status][rtd-badge]][rtd-link]
[![PyPI version][pypi-version]][pypi-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

[pypi-link]:                https://pypi.org/project/lhctodd/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/lhctodd
[pypi-version]:             https://badge.fury.io/py/lhctodd.svg
[rtd-badge]:                https://readthedocs.org/projects/lhctodd/badge/?version=latest
[rtd-link]:                 https://lhctodd.readthedocs.io/en/latest/?badge=latest

## Quick start

```python
import lhctodd
# Listing all the available DD limits 
lhctodd.list()
```

You can get then any limit

```python
# Geeting the XENON1T limits
limit = dd.DD(arxiv="1805.12562")

# cross-section limit values at 100 GeV
limit.sigma(100)

# plot the limit 
limit.plot()

# get the data
data = limit.data() 
# or
data = limit.to_pandas()
```

to translate LHC limit to DD 

```python
axial_model = lhctodd.SD(g_chi=1.0, g_g=0.25, g_l=0.0, label="CMS MonoZ")
axial_dd = axial_model.from_csv("limit-EXO-19-003-SD-90CL.csv")
axial_model.plot()

# or

import matplotlib.pyplot as plt
plt.plot(axial_dd[:,0], axial_dd[:,1])
plt.xlabel("DM mass")
plt.ylabel("DM-Nucleon cross-section (cm2)")
```

*note:  all the limits should be at 90%CL* 

## installation
To install `lhctodd` from PyPI

```bash
pip install lhctodd
```
