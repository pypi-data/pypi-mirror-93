ESA Moon Coverage Toolbox
=========================

[
    ![CI/CD](https://gitlab.univ-nantes.fr/esa-juice/moon-coverage/badges/main/pipeline.svg)
    ![Coverage](https://gitlab.univ-nantes.fr/esa-juice/moon-coverage/badges/main/coverage.svg)
](https://gitlab.univ-nantes.fr/esa-juice/moon-coverage/pipelines/main/latest)
[
    ![Version](https://img.shields.io/pypi/v/moon-coverage.svg?label=Lastest%20release&color=lightgrey)
](https://gitlab.univ-nantes.fr/esa-juice/moon-coverage/-/tags)
[
    ![License](https://img.shields.io/pypi/l/moon-coverage.svg?color=lightgrey&label=License)
](https://gitlab.univ-nantes.fr/esa-juice/moon-coverage/-/blob/main/LICENSE.md)
[
    ![PyPI](https://img.shields.io/badge/PyPI-moon--coverage-blue?logo=Python&logoColor=white)
    ![Python](https://img.shields.io/pypi/pyversions/moon-coverage.svg?label=Python&logo=Python&logoColor=white)
](https://pypi.org/project/moon-coverage/)

[
    ![Docs](https://img.shields.io/badge/Docs-esa--juice.univ--nantes.io%2Fmoon--coverage-blue?&color=orange&logo=Read%20The%20Docs&logoColor=white)
](https://esa-juice.univ-nantes.io/moon-coverage)
[
    ![DataLab](https://img.shields.io/badge/ESA%20Datalab-datalabs.edisoft.pt-blue?&color=orange&logo=Jupyter&logoColor=white)
](https://datalabs.edisoft.pt)

Install
-------

```bash
pip install moon-coverage
```

Documentation
-------------

The module documentation and some examples
can be found [here](https://esa-juice.univ-nantes.io/moon-coverage/).

Testing
-------

Setup:
```bash
git clone https://gitlab.univ-nantes.fr/esa-juice/moon-coverage
cd moon-coverage

pip install -e .
pip install -r tests/requirements.txt -r docs/requirements.txt
```

Linter:
```bash
pylint --rcfile=setup.cfg moon_coverage/ tests/**.py setup.py
flake8 moon_coverage/ tests/ setup.py
```

Unit tests (with `pytest`):
```bash
pytest --cov moon_coverage tests/
```

Build the docs (with `sphinx`):
```bash
sphinx-build docs docs/_build --color -W -bhtml
```
