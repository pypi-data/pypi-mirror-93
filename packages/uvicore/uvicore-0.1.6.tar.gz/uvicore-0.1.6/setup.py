# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uvicore',
 'uvicore.auth',
 'uvicore.auth.commands',
 'uvicore.auth.config',
 'uvicore.auth.contractsOLD',
 'uvicore.auth.database.seeders',
 'uvicore.auth.database.tables',
 'uvicore.auth.models',
 'uvicore.configuration',
 'uvicore.configuration.commands',
 'uvicore.console',
 'uvicore.console.commands',
 'uvicore.console.commands.stubs',
 'uvicore.container',
 'uvicore.container.commands',
 'uvicore.contracts',
 'uvicore.database',
 'uvicore.database.OBSOLETE',
 'uvicore.database.commands',
 'uvicore.database.commands.stubs',
 'uvicore.events',
 'uvicore.events.commands',
 'uvicore.factories',
 'uvicore.foundation',
 'uvicore.foundation.config',
 'uvicore.foundation.decorators',
 'uvicore.http',
 'uvicore.http.OBSOLETE',
 'uvicore.http.OBSOLETE.controllers',
 'uvicore.http.commands',
 'uvicore.http.routing',
 'uvicore.http.templating',
 'uvicore.logging',
 'uvicore.orm',
 'uvicore.orm.commands',
 'uvicore.orm.commands.stubs',
 'uvicore.package',
 'uvicore.package.commands',
 'uvicore.support',
 'uvicore.typing']

package_data = \
{'': ['*'], 'uvicore.auth': ['http/public/*', 'http/public/assets/js/*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0',
 'aiofiles>=0.6.0,<0.7.0',
 'alembic>=1.5.2,<2.0.0',
 'asyncclick>=7.1.2,<8.0.0',
 'colored>=1.4.2,<2.0.0',
 'databases>=0.4.1,<0.5.0',
 'environs>=9.3.0,<10.0.0',
 'fastapi>=0.63.0,<0.64.0',
 'gunicorn>=20.0.4,<21.0.0',
 'ipython>=7.19.0,<8.0.0',
 'prettyprinter>=0.18.0,<0.19.0',
 'requests>=2.25.1,<3.0.0',
 'uvicorn>=0.13.3,<0.14.0']

setup_kwargs = {
    'name': 'uvicore',
    'version': '0.1.6',
    'description': 'The Async Python Framework for Artisans. An Elegant Fullstack Python Web, API and CLI Framework',
    'long_description': "# Uvicore\n\n**The Async Python Framework for Artisans. An Elegant Fullstack Python Web, API and CLI Framework**\n\n\nThis is a full stack python framework with everything included.  Built on other micro frameworks such as Starlette and FastAPI but resembling neither.  Uvicore feels like no other python framework you have ever used.  Think Laravel instead of Django or Flask.\n\nMore to come later.\n\nUnder heavy development.  Do NOT use this repository yet.\n\n\n## Features\n\n* Super fast, built on Starlette, FastAPI (but feels like neither) and other libraries.\n* Equally well suited for complete CLI apps, Rest APIs with OpenAPI Docs and Traditional web applications.\n* Fully asynchronous including CLI apps for unix socket programming and of course Websockets.\n* Automatic API generation from all ORM models without a single line of View or Controller code.\n* Full OpenAPI 3 automatically generated docs.\n* All apps are packages and all packages are apps.  A modular framework with app override capability for configs, templates, assets, routes, models and more.  Reuse your app inside other apps as libraries for a Python native micro service architecture.  Or use the automatically generated API from ORM models for a Rest based micro service architecture with no extra work.\n* Custom IoC (Inversion of Control) system to swap any concrete implementation without changing imports.\n* Asynchronous database layer for MySQL, SQLite and Postgres.\n* All new custom asynchronous ORM (NOT another django ORM clone) with support for every relationship including polymorphism.  Enjoy Laravel's Eloquent ORM?  You'll love this one.\n* Full python type hinting for IDE code intellisense across every module including ORM model fields and methods.\n\n\n\n## ToDo\n\n* Write complete ORM tests with 100% coverage\n* Need better ORM where AND with OR mixed around.  Currently it only does all ANDs then all WHEREs which won't work for complex queries.  For example grouping 2 where ANDs with an OR like so\n\n```sql\nSELECT DISTINCT posts.id, posts.unique_slug, posts.title, posts.other, posts.creator_id, posts.owner_id, attributes.*\nFROM posts LEFT OUTER JOIN attributes ON attributes.attributable_type = 'posts' AND posts.id = attributes.attributable_id\nWHERE\n(attributes.key = 'post1-test1' and attributes.value = 'value for post1-test1')\nor\n(attributes.key = 'post2-test1' and attributes.value = 'value for post2-test1')\n```\n\n* Cannot update attributes from a parent (post.add('attributes'))...IntegrityError.  See posts seeder for notes.\n",
    'author': 'Matthew Reschke',
    'author_email': 'mail@mreschke.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://uvicore.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
