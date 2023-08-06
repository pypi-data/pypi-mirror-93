# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simpletasks_data']

package_data = \
{'': ['*']}

install_requires = \
['Flask-SQLAlchemy>=2.4.4,<3.0.0',
 'Flask>=1.1.2,<2.0.0',
 'simpletasks>=0.1.1,<0.2.0']

extras_require = \
{'geoalchemy': ['GeoAlchemy2>=0.8.4,<0.9.0']}

setup_kwargs = {
    'name': 'simpletasks-data',
    'version': '0.2.0',
    'description': 'A simple library to import data into a database from different sources (extensible)',
    'long_description': '# simpletasks-data\n\nAdditional tasks for [simpletasks](https://github.com/upOwa/simpletasks) to handle data.\n\nProvides an `ImportTask` to import data into a [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) model, from any source of data.\n\nData sources provided are:\n* CSV (`ImportCsv`)\n* SQLAlchemy query (`ImportTable`)\nCustom data sources can easily be implemented via inheriting `ImportSource`.\n\nOther data sources are provided by other libraries:\n* [gapi-helper](https://github.com/upOwa/gapi-helper) provides Google Sheets as source.\n\n\nSample:\n```python\nimport contextlib\nfrom typing import Iterable, Iterator, List, Optional, Sequence\n\nimport click\n\nfrom simpletasks import Cli, CliParams\nfrom simpletasks_data import ImportSource, ImportTask, Mapping\n\nfrom myapp import db\n\n@click.group()\ndef cli():\n    pass\n\n\nclass Asset(db.Model):\n    """Model to import to"""\n    id = db.Column(db.Integer, primary_key=True)\n    serialnumber = db.Column(db.String(128), index=True)\n    warehouse = db.Column(db.String(128))\n    status = db.Column(db.String(128))\n    product = db.Column(db.String(128))\n    guid = db.Column(db.String(36))\n\n\nclass AssetHistory(db.Model):\n    """Model to keep track of changes"""\n    id = db.Column(db.Integer, primary_key=True)\n    date = db.Column(db.DateTime)\n    asset_id = db.Column(db.Integer, db.ForeignKey("asset.id"), nullable=False, index=True)\n    asset = db.relationship("Asset", foreign_keys=asset_id)\n\n    old_warehouse = db.Column(db.String(128))\n    new_warehouse = db.Column(db.String(128))\n    old_status = db.Column(db.String(128))\n    new_status = db.Column(db.String(128))\n\n\n@Cli(cli, params=[CliParams.progress(), CliParams.dryrun()])\nclass ImportAssetsTask(ImportTask):\n    class _AssetsSource(ImportSource):\n        class _AssetMapping(Mapping):\n            def __init__(self) -> None:\n                super().__init__()\n\n                # Defines mapping between the input data and the fields from the model\n                # self.<name of the field in the model> = self.auto() -- in the order of the input data\n                self.serialnumber = self.auto()\n                self.status = self.auto(keep_history=True)\n                self.warehouse = self.auto(keep_history=True)\n                self.product = self.auto()\n                self.guid = self.auto()\n\n                # If there are gaps in the input data (i.e. fields not being used in the model), you can either:\n                # - use `self.foobar = self.col()` instead of `self.foobar = self.auto()` to specify the column name after the gap\n                # - use `foobar = self.auto()` to still register the gap/column, but not use it in the model\n\n            def get_key_column_name(self) -> str:\n                # By default, we use the "id" field - this overrides it\n                return "serialnumber"\n\n            def get_header_line_number(self) -> int:\n                # By default we skip the first (0-index) line (header) - setting to -1 includes all lines\n                return -1\n\n        @contextlib.contextmanager\n        def getGeneratorData(self) -> Iterator[Iterable[Sequence[str]]]:\n            # Custom data generator\n            output: List[Sequence[str]] = []\n\n            for x in o:\n                output.append([serialnumber, status, warehouse, product, guid])\n\n            yield output\n\n        def __init__(self) -> None:\n            super().__init__(self._AssetMapping())\n\n    def createModel(self) -> Asset:\n        return Asset()\n\n    def createHistoryModel(self, base: Asset) -> Optional[AssetHistory]:\n        o = AssetHistory()\n        o.asset_id = base.id\n        return o\n\n    def __init__(self, *args, **kwargs):\n        super().__init__(model=Asset(), keep_history=True, *args, **kwargs)\n\n    def get_sources(self) -> Iterable[ImportSource]:\n        # Here we can have multiple sources if we wish\n        return [self._AssetsSource()]\n```\n\n## Contributing\n\nTo initialize the environment:\n```\npoetry install --no-root\npoetry install -E geoalchemy\n```\n\nTo run tests (including linting and code formatting checks), please run:\n```\npoetry run pytest --mypy --flake8 && poetry run black --check .\n```\n',
    'author': 'Thomas Muguet',
    'author_email': 'thomas.muguet@upowa.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/upOwa/simpletasks-data',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
