# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['surepy']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp[speedups]>=3.6.3,<4.0.0',
 'async-timeout>=3.0.1,<4.0.0',
 'click>=7.1.2,<8.0.0',
 'colorama>=0.4.4,<0.5.0',
 'halo>=0.0.30,<0.0.31',
 'requests>=2.24.0,<3.0.0',
 'rich>=9.1.0,<10.0.0']

entry_points = \
{'console_scripts': ['surepy = surepy.cli:cli']}

setup_kwargs = {
    'name': 'surepy',
    'version': '0.5.0',
    'description': 'Library to interact with the flaps & doors from Sure Petcare.',
    'long_description': '# [![surepy](https://socialify.git.ci/benleb/surepy/image?description=1&descriptionEditable=Library%20%26%20CLI%20to%20interact%20with%20the%20Sure%20Petcare%20API%20to%20monitor%20and%20control%20the%20Sure%20Petcare%20Pet%20Door%2FCat%20Flap%20Connect%20%F0%9F%9A%AA%20and%20the%20Pet%20Feeder%20Connect%20%F0%9F%8D%BD&font=KoHo&forks=1&language=1&logo=https%3A%2F%2Femojipedia-us.s3.dualstack.us-west-1.amazonaws.com%2Fthumbs%2F240%2Fapple%2F237%2Fpaw-prints_1f43e.png&pulls=1&stargazers=1)](https://github.com/benleb/surepy)\n\nLibrary & CLI to interact with the Sure Petcare API. [**surepy**](https://github.com/benleb/surepy) lets you monitor and control the Pet Door/Cat Flap Connect 🚪 and the Pet Feeder Connect 🍽 by [Sure Petcare](https://www.surepetcare.com).\n\n[**surepy**](https://github.com/benleb/surepy) features\n\n🔑 **get an api token** with your account credentials  \n🚪 **lock/unlock** a door or flap  \n🐾 get the **location** of **pets** & **devices**  \n🐈 get the **state** and more attributes of **pets** & **devices**  \n🕰️ get **historic** data & events of pets & devices  \n📬 get a list of (past) **notifications**  \n\n<!-- > **ToC ·** [Getting Started](#getting-started) · [Usage](#usage)· [Used by](#used-by) · [Acknowledgements](#acknowledgements) **·** [Meta](#meta) -->\n\n## Getting Started\n\n[**surepy**](https://github.com/benleb/surepy) is available via [pypi.org](https://pypi.org)\n\n```bash\npython3 -m pip install --upgrade surepy\n# or\npip install --upgrade surepy\n```\n\nthere is also a small cli available\n```bash\n$ surepy --help\nUsage: surepy [OPTIONS] COMMAND [ARGS]...\n\n  surepy cli 🐾\n\n  https://github.com/benleb/surepy\n\nOptions:\n  --version         show surepy version\n  -j, --json        enable json api response output\n  -t, --token TEXT  api token\n  --help            Show this message and exit.\n\nCommands:\n  devices       get devices\n  locking       lock control\n  notification  get notifications\n  pets          get pets\n  position      set pet position\n  report        get pet/household report\n  token         get a token\n```\n>*the cli probably has some bugs, as it is mainly intended for debugging purposes - be careful* 🐾\n\n\n<!-- ### Library\n\nsee (the not yet written) [docs](https://surepy.readthedocs.io/en/latest/) -->\n\n---\n\n## Used by\n\n* [Sure Petcare](https://www.home-assistant.io/integrations/surepetcare/) integration in [Home Assistant](https://www.home-assistant.io/)\n\nFeel free to add you project!\n\n## Acknowledgments\n\n* Thanks to all the people who provided information about devices I do not own myself, thanks!\n* Thanks to [@rcastberg](https://github.com/rcastberg) for hist previous work on the [Sure Petcare](https://www.surepetcare.com) API ([github.com/rcastberg/sure_petcare](https://github.com/rcastberg/sure_petcare))\n* Thanks to [@wei](https://github.com/wei) for the  header image generator ([github.com/wei/socialify](https://github.com/wei/socialify))\n\n## Meta\n\n**Ben Lebherz**: *cat lover 🐾 developer & maintainer* - [@benleb](https://github.com/benleb) | [@ben_leb](https://twitter.com/ben_leb)\n\n<!-- See also the list of [contributors](CONTRIBUTORS) who participated in this project. -->\n\nThis project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details\n',
    'author': 'Ben Lebherz',
    'author_email': 'git@benleb.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/benleb/surepy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
