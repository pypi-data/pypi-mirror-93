# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['daffy']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.1,<2.0.0']

setup_kwargs = {
    'name': 'daffy',
    'version': '0.2.0',
    'description': 'Function decorators for Pandas Dataframe column name and data type validation',
    'long_description': '# DAFFY DataFrame Column Validator\n\n\n## Description \n\nIn projects using Pandas, it\'s very common to have functions that take Pandas DataFrames as input or produce them as output.\nIt\'s hard to figure out quickly what these DataFrames contain. This library offers simple decorators to annotate your functions\nso that they document themselves and that documentation is kept up-to-date by validating the input and output on runtime.\n\n## Table of Contents\n* [Installation](#installation)\n* [Usage](#usage)\n* [Contributing](#contributing)\n* [Tests](#tests)\n* [License](#license)\n\n## Installation\n\nInstall with your favorite Python dependency manager like\n\n```sh\npip install daffy\n```\n\nor\n\n```sh\npoetry add daffy\n```\n\n\n## Usage \n\nStart by importing the needed decorators:\n\n```\nfrom daffy import df_in, df_out\n```\n\nTo check a DataFrame input to a function, annotate the function with `@df_in`. For example the following function expects to get\na DataFrame with columns `Brand` and `Price`:\n\n```python\n@df_in(columns=["Brand", "Price"])\ndef process_cars(car_df):\n    # do stuff with cars\n```\n\nIf your function takes multiple arguments, specify the field to be checked with it\'s `name`:\n\n```python\n@df_in(name="car_df", columns=["Brand", "Price"])\ndef process_cars(year, style, car_df):\n    # do stuff with cars\n```\n\nTo check that a function returns a DataFrame with specific columns, use `@df_out` decorator:\n\n```python\n@df_out(columns=["Brand", "Price"])\ndef get_all_cars():\n    # get those cars\n    return all_cars_df\n```\n\nTo check both input and output, just use both annotations on the same function:\n\n```python\n@df_in(columns=["Brand", "Price"])\n@df_out(columns=["Brand", "Price"])\ndef filter_cars(car_df):\n    # filter some cars\n    return filtered_cars_df\n```\n\nIf you want to also check the data types of each column, you can replace the column array:\n\n```python\ncolumns=["Brand", "Price"]\n```\n\nwith a dict:\n\n```python\ncolumns={"Brand": "object", "Price": "int64"}\n```\n\nThis will not only check that the specified columns are found from the DataFrame but also that their `dtype` is the expected.\n\n\n## Contributing\n\nContributions are accepted. Include tests in PR\'s.\n\n## Development\n\nTo run the tests, clone the repository, install dependencies with Poetry and run tests with PyTest:\n\n```sh\npoetry install\npoetry shell\npytest\n```\n\nTo enable linting on each commit, run `pre-commit install`. After that, your every commit will be checked with `isort`, `black` and `flake8`.\n\n## License\n\nMIT\n',
    'author': 'Janne Sinivirta',
    'author_email': 'janne.sinivirta@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fourkind/daffy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
