# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bookmarks_converter']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.3.19,<2.0.0', 'beautifulsoup4>=4.9.3,<5.0.0']

setup_kwargs = {
    'name': 'bookmarks-converter',
    'version': '0.1.2',
    'description': 'Parse db/html/json bookmarks file from (Chrome - Firefox - Custom source) and convert it to db/html/json format.',
    'long_description': '# Bookmarks Converter\n\n---\n[![image](https://img.shields.io/github/workflow/status/radam9/bookmarks-converter/build-deploy/main?style=flat-square)](https://github.com/radam9/bookmarks-converter)\n[![image](https://img.shields.io/github/license/radam9/bookmarks-converter?style=flat-square)](https://pypi.org/project/bookmarks-converter/)\n[![image](https://img.shields.io/pypi/pyversions/bookmarks-converter?style=flat-square)](https://pypi.org/project/bookmarks-converter/)\n\n\nBookmarks Converter is a package that converts the webpage bookmarks\nfrom `DataBase`/`HTML`/`JSON` to `DataBase`/`HTML`/`JSON`.\n\n- The Database files supported are custom sqlite database files created by the SQLAlchemy ORM model found in the [`.models.py`](/src/bookmarks_converter/models.py).\n\n- The HTML files supported are Netscape-Bookmark files from either Chrome or Firefox. The output HTML files adhere to the firefox format.\n\n- The JSON files supported are the Chrome `.json` bookmarks file, the Firefox `.json` bookmarks export file, and the custom json file created by this package.\n\nTo see example of the structure or layout of the `DataBase`, `HTML` or `JSON` versions supported by the packege, you can check the corresponding file in the data folder found in the [github page data](data/) or the [bookmarks_file_structure.md](bookmarks_file_structure.md).\n\n---\n### Python and OS Support\nThe package has been tested on Github Actions with the following OSs and Python versions:\n\n| OS \\ Python      |  `3.9`  |  `3.8`  |  `3.7`  |  `3.6`  |\n| :--------------- | :-----: | :-----: | :-----: | :-----: |\n| `macos-latest`   | &check; | &check; | &check; | &check; |\n| `ubuntu-latest`  | &check; | &check; | &check; | &check; |\n| `windows-latest` | &check; | &check; | &check; | &check; |\n\n\n---\n### Dependencies\nThe package relies on the following libraries:\n- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/): used to parse the HTML files.\n- [SQLAlchemy](https://www.sqlalchemy.org/): used to create and manager the database files.\n\n---\n### Install\nBookmarks Converter is available on [PYPI](https://pypi.org/project/bookmarks-converter/)\n```bash\npython -m pip install bookmarks-converter\n```\n\n---\n### Test\nTo test the package you will need to clone the [git repository](https://github.com/radam9/bookmarks-converter).\n\n```bash\n# Cloning with HTTPS\ngit clone https://github.com/radam9/bookmarks-converter.git\n\n# Cloning with SSH\ngit clone git@github.com:radam9/bookmarks-converter.git\n```\nthen you create and install the dependencies using [`Poetry`](https://python-poetry.org/).\n\n```bash\n# navigate to repo\'s folder\ncd bookmarks-converter\n# install the dependencies\npoetry install\n# run the tests\npoetry run pytest\n```\n\n---\n### Usage\n```python\nfrom bookmarks_converter import BookmarksConverter\n\n# initialize the class passing in the path to the bookmarks file to convert\nbookmarks = BookmarksConverter("/path/to/bookmarks_file")\n\n# parse the file passing the format of the source file; "db", "html" or "json"\nbookmarks.parse("html")\n\n# convert the bookmarks to the desired format by passing the fomrat as a string; "db", "html", or "json"\nbookmarks.convert("json")\n\n# at this point the converted bookmarks are stored in the \'bookmarks\' attribute.\n# which can be used directly or exported to a file.\nbookmarks.save()\n```\n\n---\n### License\n[MIT License](LICENSE)',
    'author': 'Adam Saleh',
    'author_email': 'radam9@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/radam9/bookmarks-converter',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
