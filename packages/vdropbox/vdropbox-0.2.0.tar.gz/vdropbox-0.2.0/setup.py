# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vdropbox']

package_data = \
{'': ['*']}

install_requires = \
['dropbox>=10.2.0,<11.0.0', 'oyaml>=1.0,<2.0', 'pandas>=1.1.4,<2.0.0']

setup_kwargs = {
    'name': 'vdropbox',
    'version': '0.2.0',
    'description': 'Utilities to read/write python objects to/from dropbox',
    'long_description': '# vdropbox\n\nUtilities to read/write objects to/from dropbox\n\n## Usage\n\nThe first thing to do is to declare the `Vdropbox` object using a token with:\n\n```python\nfrom vdropbox import Vdropbox\nvdp = Vdropbox("my_secret")\n```\n\nUnlike the official `dropbox` python package it is not needed to have a leading `/` in all names.\n\n### Basic functions\n\n```python\n# Check if a file exists\nvdp.file_exists("my_file.txt")\nvdp.file_exists("folder/my_file.txt")\n\n# Check contents of a foler\nvdp.ls("my_folder")\n\n# Delete a file\nvdp.delete("my_file.txt")\n```\n\n### Reading and writting text files\n\n```python\ndata = "Hello world"\n\n# Write a text file\nvdp.write_file(data, "my_file.txt")\n\n# Read a text file\nvdp.read_file("my_file.txt")\n```\n\n> Internally it is using `oyaml` so all yamls are ordered.\n\n\n### Reading and writting yamls\n\n```python\ndata = {"a": 4, "b": 2}\n\n# Write a yaml file\nvdp.write_yaml(data, "my_file.yaml")\n\n# Read a yaml file\nvdp.read_yaml("my_file.yaml")\n```\n\n> Internally it is using `oyaml` so all yamls are ordered.\n\n### Reading and writting excels with pandas\n\n```python\nimport pandas as pd\n# Dummy dataframe\ndf = pd.DataFrame(list("ABCDE"), columns=["col"])\n\n# Write an excel file\nvdp.write_excel(df, "df.xlsx")\n\n# Read a parquet file\nvdp.read_excel("df.parquet")\n```\n\nIt is possible to pass keyworded arguments to the internal `pd.read_excel` or `df.to_excel` function.\nFor example:\n\n```python\nvdp.write_excel(df, "test.xlsx", index=False)\n```\n\n### Reading and writting parquets with pandas\n\n```python\nimport pandas as pd\n# Dummy dataframe\ndf = pd.DataFrame(list("ABCDE"), columns=["col"])\n\n# Write a parquet file\nvdp.write_parquet(df, "df.parquet")\n\n# Read a parquet file\nvdp.read_parquet("df.parquet")\n```\n\nIt is possible to pass keyworded arguments to the internal `pd.read_parquet` or `df.to_parquet` function.\n\n## Authors\n* [Arnau Villoro](villoro.com)\n\n## License\nThe content of this repository is licensed under a [MIT](https://opensource.org/licenses/MIT).\n',
    'author': 'Arnau Villoro',
    'author_email': 'arnau@villoro.com',
    'maintainer': 'Arnau Villoro',
    'maintainer_email': 'arnau@villoro.com',
    'url': 'https://github.com/villoro/vdropbox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
