## Thème CKAN pour le catalogue de données de VALERIA
https://valeria.science/  
https://catalogue.valeria.science/donneesqc

## Upload ckan theme to pypi
. /usr/lib/ckan/default/bin/activate

python3 -m pip install --upgrade setuptools wheel

python3 setup.py sdist bdist_wheel

python3 -m pip install --upgrade twine

python3 -m twine upload dist/*