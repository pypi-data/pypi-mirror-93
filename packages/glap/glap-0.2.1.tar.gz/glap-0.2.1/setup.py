# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['glap']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'python-gitlab>=2.6.0,<3.0.0',
 'requests>=2.25.1,<3.0.0',
 'toml>=0.10.2,<0.11.0',
 'yaspin>=1.3.0,<2.0.0']

entry_points = \
{'console_scripts': ['glap = glap.cli:main']}

setup_kwargs = {
    'name': 'glap',
    'version': '0.2.1',
    'description': 'GitLab Artifact Puller / Downloader',
    'long_description': '# glap\n\n![Python package](https://github.com/Mountlex/glap/workflows/Python%20package/badge.svg)\n\nA GitLab Artifact Puller / Downloader\n\n## Quick Start\n\n`glap` is a convenience tool to download artifacts of your frequently used GitLab repositories. Install via\n\n```bash\npip install glap\n```\n\nBefore you can use `glap`, you have to setup your configuration file located at `~/.config/glap/glap.toml` (if such a file cannot be found, it will also search for a local `glap.toml` file). It contains the following information.\n\n* Remotes with corresponding `url`s and access-tokens:\n\n```toml\n[remotes.myremote]\nurl = "https://gitlab.com"\nprivate_token = "<my-private-token>"\noauth_token = "<my-oauth-token>"\njob_token = "<my-job-token>"\n```\n\nNote that there must be exactly one token specified.\n\n* Shortcuts for specific repositories. For example, the following shortcut points at the `PDFs` job of the `main` branch of `https://gitlab.com/name/repo`.\n\n```toml\n[shortcuts.myshortcut]\nremote = "myremote"\nnamespace = "name"\nrepository = "repo"\nbranch = "main"\njob = "PDFs"\n```\n\nAny configured shortcut will appear as a subcommand, i.e. you can use it as follows\n\n```bash\nglap myshortcut\n```\n\nAlternatively, you can specify the namespace and repository directly\n\n```bash\nglap download <namespace> <repository>\n```\n\nIf no remote is given, `glap` will use the first one in the configuration file. Otherwise, you can use\n\n```bash\nglap download <namespace> <repository> -r myremote\n```\n\nwhere `myremote` is the name of the remote in the configuration file.\n\n### Options\n\n* `--job` (`-j`) specifies the job\'s name.\n* `--branch` (`-b`) specifies the branch\'s name.\n* `--output` (`-o`) specifies the download location.\n* `--temp` (`-t`) downloads the artifact to a temporary location and opens the directory.\n* `--silent` (`-s`) enables silent mode (exceptions only).\n* `--verbose` (`-v`) enables verbose mode (e.g. print file list).\n  ',
    'author': 'Alexander Lindermayr',
    'author_email': 'alexander.lindermayr97@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Mountlex/glap',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
