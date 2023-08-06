# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['api',
 'api.client',
 'api.client.batch_client',
 'api.client.cfg',
 'api.client.crop_model',
 'api.client.gro_client',
 'api.client.lib',
 'api.client.samples',
 'api.client.samples.analogous_years',
 'api.client.samples.analogous_years.lib',
 'api.client.samples.analogous_years.lib.utils',
 'api.client.samples.batch_queries',
 'api.client.samples.crop_models',
 'api.client.samples.similar_regions',
 'groclient']

package_data = \
{'': ['*'],
 'api.client.samples': ['analysis_kits/stocks_to_use_price_model/*',
                        'anomaly_detection/*',
                        'drought/*',
                        'prevented_plant/*']}

install_requires = \
['numpy', 'pandas', 'requests', 'tornado', 'unicodecsv']

extras_require = \
{'docs': ['sphinx>=3.1.0,<3.2.0',
          'recommonmark',
          'sphinx_rtd_theme',
          'sphinx-multiversion']}

entry_points = \
{'console_scripts': ['gro_client = groclient.__main__:main']}

setup_kwargs = {
    'name': 'groclient',
    'version': '1.107.3',
    'description': "Python client library for accessing Gro Intelligence's agricultural data platform",
    'long_description': '<p align="center"><img width=8% src="https://gro-intelligence.com/images/logo.jpg"></p>\n<h1 align="center">Gro API Client</h1>\n\n<https://www.gro-intelligence.com/products/gro-api>\n\nClient library for accessing Gro Intelligence\'s agricultural data platform.\n\n## Prerequisites\n\n1. [MacOS and Linux](unix-setup.md)\n2. [Windows](windows-setup.md)\n\n## Install Gro API client packages\n\n```sh\npip install groclient\n```\n\nNote that even if you are using [Anaconda](https://www.anaconda.com/), the API Client install should still be performed using pip and not [conda](https://docs.conda.io/en/latest/).\n\nIf you\'re unable to access PyPI, you can install the latest code from Github: `pip install git+https://github.com/gro-intelligence/api-client.git`\n\n## Gro API authentication token\n\nUse the Gro web application to retrieve an authentication token (detailed instructions are on the developers site [here](https://developers.gro-intelligence.com/authentication.html)).\n\n## Examples\n\nNavigate to [api/client/samples/](api/client/samples/) folder and try executing the provided examples.\n\n1. Start with [quick_start.py](api/client/samples/quick_start.py). This script creates an authenticated `GroClient` object and uses the `get_data_series()` and `get_data_points()` methods to find Area Harvested series for Ukrainian Wheat from a variety of different sources and output the time series points to a CSV file. You will likely want to revisit this script as a starting point for building your own scripts.\n\n    Note that the script assumes you have your authentication token set to a `GROAPI_TOKEN` environment variable (see [Saving your token as an environment variable](https://developers.gro-intelligence.com/authentication.html#saving-your-token-as-an-environment-variable)). If you don\'t wish to use environment variables, you can modify the sample script to set [`ACCESS_TOKEN`](https://github.com/gro-intelligence/api-client/blob/0d1aa2bccaa25a033e39712c62363fd89e69eea1/api/client/samples/quick_start.py#L7) in some other way.\n\n    ```sh\n    python quick_start.py\n    ```\n\n    If the API client is installed and your authentication token is set, a csv file called `gro_client_output.csv` should be created in the directory where the script was run.\n\n2. Try out [soybeans.py](api/client/samples/crop_models/soybeans.py) to see the `CropModel` class and its `compute_crop_weighted_series()` method in action. In this example, NDVI ([Normalized difference vegetation index](https://app.gro-intelligence.com/dictionary/items/321)) for provinces in Brazil is weighted against each province\'s historical soybean production to put the latest NDVI values into context. This information is put into a pandas dataframe, the description of which is printed to the console.\n\n    ```sh\n    python crop_models/soybeans.py\n    ```\n\n3. See [brazil_soybeans.ipynb](https://github.com/gro-intelligence/api-client/blob/development/api/client/samples/crop_models/brazil_soybeans.ipynb) for a longer, more detailed demonstration of many of the API\'s capabilities in the form of a Jupyter notebook.\n\n4. You can also use the included `gro_client` tool as a quick way to request a single data series right on the command line. Try the following:\n\n    ```sh\n    gro_client --metric="Production Quantity mass" --item="Corn" --region="United States" --user_email="email@example.com"\n    ```\n\n    The `gro_client` command line interface does a keyword search for the inputs and finds a random matching data series. It displays the data series it picked and the data points to the console. This tool is useful for simple queries, but anything more complex should be done using the provided Python packages.\n\nFurther documentation can be found on the Gro Developers site at <developers.gro-intelligence.com>.\n',
    'author': 'Gro Intelligence developers',
    'author_email': 'dev@gro-intelligence.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.gro-intelligence.com/products/gro-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
