# Siasearch SDK
Siasearch SDK is a way to programmatically interface with the Siasearch software. It provides an alternative
interface to the GUI and allows users to easily query for, view and manipulate the data fetched.
```python

>>> from siasearch import SiaSearch
>>> sia = SiaSearch.login("http://custom-domain.siasearch.de", "user@example.com", "password")
<SiaSearch object with user `user@example.com` connected to `http://custom-domain.siasearch.de`>
>>> cols = sia.columns()
>>> cols
<Columns object containing columns: ['acceleration_level', 'curved_trajectory', 'dataset_name', 'forward_velocity',...
>>> cols.curved_trajectory.levels
["'LEFT_BEND'", "'NO_BEND'", "'RIGHT_BEND'"]
>>> query = sia.query("dataset_name = 'kitti' AND curved_trajectory = 'LEFT_BEND'")
Query("dataset_name = 'kitti' AND curved_trajectory = 'LEFT_BEND'")
>>> sequences = query.all()
>>> sequences
<Sequences class with 54 segments>
```

# Installing siasearch
Siasearch is available on PyPi
```bash
pip install siasearch
```

# How to use it?
See [docs](https://demo.sia-search.com/sdk_docs/)

## Documentation
To generate simple Sphinx documentation you need to install Sphinx package  
```bash
 pip install -U Sphinx
 pip install sphinx-rtd-theme
```
and run: 
```bash
sphinx-build -b html docs/source docs/build
```
from the package root folder.  
And you would get build html documentation in `docs/build` folder.  
You can serve it running `python -m http.server` from `docs/build` folder.  
