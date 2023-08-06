# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['manim_plugintemplate', 'manim_plugintemplate.mobjects']

package_data = \
{'': ['*']}

install_requires = \
['manim>=0.3']

entry_points = \
{'manim.plugins': ['manim_plugintemplate = manim_plugintemplate']}

setup_kwargs = {
    'name': 'manim-plugintemplate',
    'version': '0.1.5',
    'description': 'A template project to both illustrate and serve as an example for plugin creations on top of the manim (community edition) engine.',
    'long_description': '# Plugin Template\n\nPlugins are features that extend Manim\'s core functionality. This is a\ntemplate project that demonstrates how you can create and upload a manim\nplugin to PyPI using a PEP 517 compliant build system,\n[Poetry](https://python-poetry.org).\n\nPoetry is **NOT** required to create plugins, but is recommended because\nit provides build isolation and ensures users can reliably install your\nplugin without falling into dependency hell. You may use another build\nsystem (e.g. Flit, Setuptools, Pipenv, etc...) if you wish.\n\n## Creating Plugins\n\nThe only requirement of your preferred build system is that it specifies\nthe `manim.plugins` [entry\npoint](https://packaging.python.org/specifications/entry-points/).\n\n> **note**\n>\n> The plugin naming convention is to add the prefix `manim-`. This\n> allows users to easily search for plugins on organizations like PyPi,\n> but it is not required.\n\n### Installing Poetry\n\nPoetry can be installed on Windows, MacOS and Linux. Please visit the\nofficial poetry website for [installation\ninstructions](https://python-poetry.org/docs/#installation). You may\nwant to see the official documentation for a list of all [available\ncommands](https://python-poetry.org/docs/cli/).\n\n### Setting Up Your Plugin Directory Structure\n\nTo create a Python project suitable for poetry, run:\n\n``` {.sourceCode .bash}\npoetry new --src manim-YourPluginName \n```\n\n> **note**\n>\n> `--src` is both optional and recomended in order to create a src\n> directory where all of your plugin code should live.\n\nThis will create the following project structure: :\n\n    manim-YourPluginName\n    ├── pyproject.toml\n    ├── README.rst\n    ├── src\n    │   └── manim_yourpluginname\n    │       └── __init__.py\n    └── tests\n        ├── __init__.py\n        └── test_manim_yourpluginname.py \n\nIf you have already extended manim\'s functionality, you can instead run:\n\n``` {.sourceCode .bash}\ncd path/to/plugin\npoetry init\n```\n\nThis will prompt you for basic information regarding your plugin and\nhelp create and populate a `pyproject.toml` similar to the one in this\ntemplate; however, you may wish to update your project directory\nstructure similarly.\n\nSee the official documentation for more information on the [init\ncommand](https://python-poetry.org/docs/cli/#init).\n\nFrom now on, when working on your plugin, ensure you are using the\nvirtual environment by running the following at the root of your\nproject:\n\n``` {.sourceCode .bash}\npoetry shell \n```\n\n### Updating Pyproject.toml\n\nThe `pyproject.toml` file is used by Poetry and other build systems to\nmanage and configure your project. Manim uses the package\'s entry point\nmetadata to discover available plugins. The entry point group,\n`"manim.plugins"`, is **REQUIRED** and can be [specified as\nfollows](https://python-poetry.org/docs/pyproject/#plugins):\n\n``` {.sourceCode .toml}\n[tool.poetry.plugins."manim.plugins"]\n"manim_yourpluginname" = "module:object.attr"\n```\n\n> **note**\n>\n> The left hand side represents the entry point name which should be\n> unique among other plugin names. This is the internal name Manim will\n> use to identify and handle plugins.\n>\n> The right hand side should reference a python object (i.e. module,\n> class, function, method, etc...) and will be the first code run in\n> your plugin. In the case of this template repository, the package name\n> is used which Python interprets as the package\'s `__init__.py` module.\n>\n> See the python packaging\n> [documentation](https://packaging.python.org/specifications/entry-points/)\n> for more information on entry points.\n\n### Testing Your Plugin Locally\n\n\n``` {.sourceCode .bash}\npoetry install\n```\n\nThis command will read the `pyproject.toml`, install the dependencies of\nyour plugin, and create a `poetry.lock` file to ensure everyone using\nyour plugin gets the same version of dependencies. It is important that\nyour dependencies are properly annotated with a version constraint (e.g.\n`manim:^0.1.1`, `numpy:*`, etc...). Equally important to the\ndependencies specified here is that they do not directly conflict with\n[Manim\'s](https://github.com/ManimCommunity/manim/blob/master/pyproject.toml).\nIf you want to update the dependencies specified in `pyproject.toml`,\nuse:\n\n``` {.sourceCode .bash}\npoetry update\n```\n\nSee the official documentation for more information on\n[versioning](https://python-poetry.org/docs/dependency-specification/)\nor the [install command](https://python-poetry.org/docs/cli/#install).\n\nPoetry allows for dependencies that are strictly for project developers.\nThese are not installed by users. To add them to your project, update\nthe `pyproject.toml` file with the section followed by the dependencies:\n\n``` {.sourceCode .toml}\n[tool.poetry.dev-dependencies]\npytest = "*"\npylint = "*"\n```\n\nThe `pytest` package is a functional testing framework which you can use\nto run the test within the `manim-YourPluginName/tests` directory. You\nshould create files which test the behavior and functionality of your\nplugin here. Test first development is a good practice to ensure your\ncode behaves as intended before packaging and shipping your code\npublicly. Additionally, you can create Manimations that depend on your\nplugin which is another great way to ensure functionality.\n\n### Uploading Your Project\n\n\nBy default, poetry is set to register the package/plugin to PyPI. You\'ll\nneed to register an account there to upload/update your plugin. As soon\nas your plugin is useful locally, run the following:\n\n``` {.sourceCode .bash}\npoetry publish --build\n```\n\nYour project should now be available on PyPI for users to install via\n`pip install manim-YourPluginName` and usable within their respective\nenvironments.\n\nSee the official documentation for more information on the [publish\ncommand](https://python-poetry.org/docs/cli/#publish).\n\n## Code of Conduct\n\n\nOur full code of conduct, and how we enforce it, can be read on [our website](https://docs.manim.community/en/latest/conduct.html).',
    'author': 'The Manim Community Developers',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ManimCommunity/manim-plugintemplate',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
