# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_admin', 'fastapi_admin.routes']

package_data = \
{'': ['*']}

install_requires = \
['aiomysql',
 'aiosqlite',
 'bcrypt',
 'colorama',
 'fastapi',
 'jinja2',
 'passlib',
 'prompt_toolkit',
 'pyjwt',
 'python-dotenv',
 'python-rapidjson',
 'tortoise-orm',
 'uvicorn',
 'xlsxwriter']

extras_require = \
{'uvloop': ['uvloop']}

entry_points = \
{'console_scripts': ['fastapi-admin = fastapi_admin.cli:main']}

setup_kwargs = {
    'name': 'fastapi-admin',
    'version': '0.3.3',
    'description': 'Fast Admin Dashboard based on fastapi and tortoise-orm.',
    'long_description': '# FastAPI ADMIN\n\n[![image](https://img.shields.io/pypi/v/fastapi-admin.svg?style=flat)](https://pypi.python.org/pypi/fastapi-admin)\n[![image](https://img.shields.io/github/license/long2ice/fastapi-admin)](https://github.com/long2ice/fastapi-admin)\n[![image](https://github.com/long2ice/fastapi-admin/workflows/gh-pages/badge.svg)](https://github.com/long2ice/fastapi-admin/actions?query=workflow:gh-pages)\n[![image](https://github.com/long2ice/fastapi-admin/workflows/pypi/badge.svg)](https://github.com/long2ice/fastapi-admin/actions?query=workflow:pypi)\n\n[中文文档](https://blog.long2ice.cn/2020/05/fastapi-admin%E5%BF%AB%E9%80%9F%E6%90%AD%E5%BB%BA%E5%9F%BA%E4%BA%8Efastapi%E4%B8%8Etortoise-orm%E7%9A%84%E7%AE%A1%E7%90%86%E5%90%8E%E5%8F%B0/)\n\n## Introduction\n\nFastAPI-Admin is a admin dashboard based on\n[fastapi](https://github.com/tiangolo/fastapi) and\n[tortoise-orm](https://github.com/tortoise/tortoise-orm).\n\nFastAPI-Admin provide crud feature out-of-the-box with just a few\nconfig.\n\n## Live Demo\n\nCheck a live Demo here\n[https://fastapi-admin.long2ice.cn](https://fastapi-admin.long2ice.cn/).\n\n- username: `admin`\n- password: `123456`\n\nData in database will restore every day.\n\n## Screenshots\n\n![image](https://github.com/long2ice/fastapi-admin/raw/master/images/login.png)\n\n![image](https://github.com/long2ice/fastapi-admin/raw/master/images/list.png)\n\n![image](https://github.com/long2ice/fastapi-admin/raw/master/images/view.png)\n\n![image](https://github.com/long2ice/fastapi-admin/raw/master/images/create.png)\n\n## Requirements\n\n- [FastAPI](https://github.com/tiangolo/fastapi) framework as your\n  backend framework.\n- [Tortoise-ORM](https://github.com/tortoise/tortoise-orm) as your orm\n  framework, by the way, which is best asyncio orm so far and I\\\'m one\n  of the contributors😋.\n\n## Quick Start\n\n### Run Backend\n\nLook full example at\n[examples](https://github.com/long2ice/fastapi-admin/tree/dev/examples).\n\n1. `git clone https://github.com/long2ice/fastapi-admin.git`.\n2. `docker-compose up -d --build`.\n3. `docker-compose exec -T mysql mysql -uroot -p123456 < examples/example.sql fastapi-admin`.\n4. That\'s just all, api server is listen at [http://127.0.0.1:8000](http://127.0.0.1:8000) now.\n\n### Run Front\n\nSee\n[restful-admin](https://github.com/long2ice/restful-admin)\nfor reference.\n\n## Backend Integration\n\n```shell\n> pip3 install fastapi-admin\n```\n\n```Python\nfrom fastapi_admin.factory import app as admin_app\n\nfast_app = FastAPI()\n\nregister_tortoise(fast_app, config=TORTOISE_ORM, generate_schemas=True)\n\nfast_app.mount(\'/admin\', admin_app)\n\n@fast_app.on_event(\'startup\')\nasync def startup():\n    await admin_app.init(\n        admin_secret="test",\n        permission=True,\n        site=Site(\n            name="FastAPI-Admin DEMO",\n            login_footer="FASTAPI ADMIN - FastAPI Admin Dashboard",\n            login_description="FastAPI Admin Dashboard",\n            locale="en-US",\n            locale_switcher=True,\n            theme_switcher=True,\n        ),\n    )\n```\n\n## Documentation\n\nSee documentation at [https://long2ice.github.io/fastapi-admin](https://long2ice.github.io/fastapi-admin).\n\n## Deployment\n\nDeploy fastapi app by gunicorn+uvicorn or reference\n<https://fastapi.tiangolo.com/deployment/>.\n\n## Restful API Docs\n\nSee [restful api](https://fastapi-admin-api.long2ice.cn/admin/docs)\ndocs.\n\n## Support this project\n\n| AliPay                                                                                        | WeChatPay                                                                                        | PayPal                                                           |\n| --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------- |\n| <img width="200" src="https://github.com/long2ice/fastapi-admin/raw/dev/images/alipay.jpeg"/> | <img width="200" src="https://github.com/long2ice/fastapi-admin/raw/dev/images/wechatpay.jpeg"/> | [PayPal](https://www.paypal.me/long2ice) to my account long2ice. |\n\n## License\n\nThis project is licensed under the\n[Apache-2.0](https://github.com/long2ice/fastapi-admin/blob/master/LICENSE)\nLicense.\n',
    'author': 'long2ice',
    'author_email': 'long2ice@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/long2ice/fastapi-admin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
