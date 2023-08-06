# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['validator']

package_data = \
{'': ['*'], 'validator': ['locale/*', 'locale/zh_CN/LC_MESSAGES/*']}

install_requires = \
['IPy', 'six>=1.15.0,<2.0.0']

extras_require = \
{'tzinfo': ['pytz']}

setup_kwargs = {
    'name': 'python-validator',
    'version': '0.0.8',
    'description': 'a data validator like Django ORM',
    'long_description': '# python-validator\n\npython-validator 是一个类似于 Django ORM 的数据校验库，适用与任何需要进行数据校验的应用，比较常见的是 Web 后端校验前端的输入数据。\n\n[文档](https://ausaki.github.io/python-validator)\n\n---\n\n[![PyPi](https://img.shields.io/pypi/v/python-validator.svg)\n](https://pypi.org/project/python-validator/)\n[![PyPI - Status](https://img.shields.io/pypi/status/python-validator.svg)](https://pypi.org/project/python-validator/)\n[![PyPi - Python Version](https://img.shields.io/pypi/pyversions/python-validator.svg)](https://pypi.org/project/python-validator/)\n[![PyPI - License](https://img.shields.io/pypi/l/python-validator.svg)](https://pypi.org/project/python-validator/)\n\n![GitHub last commit](https://img.shields.io/github/last-commit/ausaki/python-validator.svg)\n[![Build Status - master](https://travis-ci.org/ausaki/python-validator.svg?branch=master)](https://travis-ci.org/ausaki/python-validator)\n\n---\n\n## 特性\n\n- 支持 python2 和 python3。\n\n- 使用类描述数据结构，数据字段一目了然。另外也支持使用字典定义数据结构。\n\n- 可以自动生成用于测试的 mocking data。\n\n- 可以打印出清晰的数据结构。\n\n- 易于扩展。\n\n\n## 依赖\n\n- six\n\n- IPy\n\n- pytz[可选，`DatetimeField` 的 `tzinfo` 参数需要一个 `tzinfo` 对象]\n\n\n## 安装\n\n`pip install python-validator`\n\n\n## 快速入门\n\n假设现在正在开发一个上传用户信息的接口 `POST /api/user/`，用户信息如下：\n\n| 字段 | 类型 | 描述 |\n|--|--|--|\n|name|String| 必选 |\n|age|integer| 可选，默认 20|\n|sex|String, \'f\'表示女, \'m\'表示男 | 可选, 默认 None|\n\n原始的、枯燥无味的、重复性劳动的数据校验代码可能是下面这样：\n\n```python\ndef user(request):\n    # data = json.loads(request.body)\n    data = {\n        \'age\': \'24f\',\n        \'sex\': \'f\'\n    }\n    name = data.get(\'name\')\n    age = data.get(\'age\', 20)\n    sex = dage.get(\'sex\')\n\n    if name is None or len(name) == 0:\n        return Response(\'必须提供 name\', status=400)\n\n    try:\n        age = int(age)\n    except ValueError as e:\n        return Response(\'age 格式错误\', status=400)\n\n    if sex is not None and sex not in (\'f\', \'m\'):\n        return Response(\'sex 格式错误\', status=400)\n\n    user_info = {\n        \'name\': name,\n        \'age\': age,\n        \'sex\': sex,\n    }\n    ...\n```\n\n上面这段代码总的来说有几个问题：\n\n- 枯燥无味和重复性代码，不断的取出数据，检查字段是否缺失，类型是否合法等等。\n\n- 从数据校验的代码无法轻易看出用户信息的数据结构，即字段是什么类型的，是否可选，默认值是什么。\n\n**使用 python-validator 校验数据**\n\n首先定义一个 UserInfoValidator 类\n\n```python\n# validators.py\nfrom validator import Validator, StringField, IntegerField, EnumField\n\nclass UserInfoValidator(Validator):\n    name = StringField(max_length=50, required=True)\n    age = IntegerField(min_value=1, max_value=120, default=20)\n    sex = EnumField(choices=[\'f\', \'m\'])\n```\n\n接下来使用 `UserInfoValidator` 进行数据校验，\n\n```python\nfrom .validators import UserInfoValidator\n\ndef user(request):\n    # data = json.loads(request.body)\n    data = {\n        \'age\': \'24\',\n        \'sex\': \'f\'\n    }\n    v = UserInfoValidator(data)\n    if not v.is_valid():\n        return Response({\'msg\': v.str_errors, \'code\': 400}, status=400)\n\n    user_info = v.validated_data\n    ...\n```\n\n`v.str_errors` 是一个字段名 - 错误信息的 dict，例如：\n\n```python\n{\'age\': \'got a wrong type: str, expect integer\', \'name\': \'Field is required\'}\n```\n\n错误信息解释：\n\n- `age` 等于 "24"，不是合法的 `int` 类型。\n\n- `name` 是必须提供的，且没有指定默认值。\n\n\nv.validated_data 是校验后合法的数据，例如：\n\n```json\n{\'age\': 24, \'name\': u\'Michael\', \'sex\': \'f\'}\n```\n\n下面是一些错误数据的例子：\n\n```python\ndata:  {\'age\': 24, \'name\': \'abcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabc\', \'sex\': \'f\'}\nis_valid: False\nerrors: {\'name\': \'string is too long, max-lenght is 50\'}\nvalidated_data: None\n```\n\n```python\ndata:  {\'age\': 24, \'name\': \'Michael\', \'sex\': \'c\'}\nis_valid: False\nerrors: {\'sex\': "\'c\' not in the choices"}\nvalidated_data: None\n```\n\n细心的同学可能发现了 `IntegerField` 不接受 “数字字符串”，上面的例子中 `age` 是一个 `IntegerField`，形如 `\'24\'` 这样的值是非法的。在某些情况下，你可能希望 `IntegerField` 不要这么严格，`\'24\'` 这样的值也是可以接受的，那么可以把 `strict` 选项设为 `False`，如：`age = IntegerField(min_value=1, max_value=120, default=20, strict=False)`。当 `strict` 选项为 `False` 时，python-validator 会尝试进行类型转换，假如转换失败则会报错。\n\n接下来你可以 [查看进阶](https://ausaki.github.io/python-validator/advanced/) 了解 python-validator 更多的用法，[查看字段 API](https://ausaki.github.io/python-validator/fields/) 了解字段的详细信息。\n\n\n## 测试\n\n使用 tox 和 pytest 进行代码测试。\n\n推荐使用 [pipenv](https://github.com/pypa/pipenv) 来管理项目依赖。\n\n**假如使用 pipenv：**\n\n- `pipenv install`(安装依赖库)\n\n- `pipenv run test`\n\n**假如使用 pip：**\n\n- `pip install -r requirements.txt`(安装依赖库)\n\n- `tox`\n\n\n## 其它\n\n如果遇到 BUG 或者有任何建议，欢迎提交 issue 或者 PR。\n\n如果希望贡献代码，请尽量编写测试用例并测试你的代码，然后再提交 PR。',
    'author': 'ausaki',
    'author_email': 'ljm51689@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ausaki/python-validator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.0',
}


setup(**setup_kwargs)
