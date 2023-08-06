
# https://packaging.python.org/tutorials/packaging-projects/

```
touch LICENSE, README.md, setup.py
```

```
python -m pip install --user --upgrade setuptools wheel twine
python setup.py sdist bdist_wheel
```

```
python -m twine upload --repository pypi dist/*
```

```
pip install example-pkg-bradmorg
```