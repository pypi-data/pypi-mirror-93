## Thème CKAN pour le catalogue de données de VALERIA
https://valeria.science/  
https://catalogue.valeria.science/

## Upload nouvelle version de ckan theme to pypi

### Prérequis

python3 -m pip install --upgrade setuptools wheel

python3 -m pip install --upgrade twine

### Upload

Incrémenter la version du fichier: /ckanext/valeria/\_\_init\_\_.py

python3 setup.py sdist bdist_wheel

python3 -m twine upload dist/*