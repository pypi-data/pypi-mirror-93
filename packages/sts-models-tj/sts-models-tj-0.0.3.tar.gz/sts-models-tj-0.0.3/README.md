sts models

use python3 setup.py sdist bdist_wheel to make new version
then remove old whl and tar files
then use ```python3 -m twine upload --repository testpypi dist/*``` to reupload

then, in the project the library is to be used in, do
pip uninstall <name>
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple <name>
to get the latest
