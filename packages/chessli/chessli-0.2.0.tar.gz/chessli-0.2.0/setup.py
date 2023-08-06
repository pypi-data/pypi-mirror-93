# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chessli', 'chessli.cli']

package_data = \
{'': ['*']}

install_requires = \
['berserk>=0.10.0,<0.11.0',
 'matplotlib>=3.3.3,<4.0.0',
 'omegaconf>=2.0.6,<3.0.0',
 'pandas>=1.2.0,<2.0.0',
 'python-chess>=1.999,<2.0',
 'rich>=9.9.0,<10.0.0',
 'seaborn>=0.11.1,<0.12.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['chessli = chessli.cli.main:app']}

setup_kwargs = {
    'name': 'chessli',
    'version': '0.2.0',
    'description': 'A free and open source chess improvement app that combines the power of lichess and anki',
    'long_description': "![Thumbnail](https://github.com/pwenker/chessli/blob/main/imgs/chessli.png?raw=true)\n\n_A free and open-source chess improvement app that combines the power of Lichess and Anki._\n\n|  | Chessli |\n| --- | --- |\n| Project                | ![GitHub Repo stars](https://img.shields.io/github/stars/pwenker/chessli?style=social) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/pwenker/chessli) ![Lines of code](https://img.shields.io/tokei/lines/github/pwenker/chessli)\n| Activity & Issue Tracking | ![GitHub last commit](https://img.shields.io/github/last-commit/pwenker/chessli) ![GitHub issues](https://img.shields.io/github/issues-raw/pwenker/chessli) ![GitHub closed issues](https://img.shields.io/github/issues-closed-raw/pwenker/chessli)  |\n| PyPI                      | ![PyPI](https://img.shields.io/pypi/v/chessli)                                                                                                                                  ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/chessli) ![PyPI - Downloads](https://img.shields.io/pypi/dm/chessli) |\n| Build & Health                  | ![GitHub Workflow Status](https://img.shields.io/github/workflow/status/pwenker/chessli/CI) ![Codecov](https://img.shields.io/codecov/c/github/pwenker/chessli) |\n| Docs | ![Documentation Status](https://img.shields.io/badge/Docs-live-green) ![](https://img.shields.io/badge/Tutorial-active-brightgreen) |\n\n## Demos\n\n### CLI Demo (watch whole video on [Youtube](https://www.youtube.com/embed/XbD71Kq7cx4))\n\n![CLI DEMO GIF](https://github.com/pwenker/chessli/blob/main/imgs/chessli_cli_demo.gif?raw=true)\n\n### Anki Cards Demo (watch whole video on [Youtube](https://www.youtube.com/embed/aj-FqJhPyyA))\n\n![CLI CARDS GIF](https://github.com/pwenker/chessli/blob/main/imgs/chessli_cards_demo.gif?raw=true)\n\n## Documentation\nCheck out the [documentation](https://pwenker.com/chessli):\n\n|  | Tutorial |\n| --- | --- |\nSetup chessli | [How to set chessli up](tutorial/how_to_set_up_chessli)\nGames & Mistakes | [How to learn from your games](tutorial/how_to_learn_from_your_games.md)\nOpenings | [How to build an opening repertoire](tutorial/how_to_create_an_opening_repertoire.md)\nTactics | [How to get better at tactics](tutorial/how_to_get_better_at_tactics.md)\nAnki Cards | [How to use chessli's anki cards](tutorial/how_to_use_chesslis_anki_cards.md)\n\n\n## Features\n\n- **Automatically fetch your games** and played tactics puzzles from [`lichess`](https://www.lichess.org) via the [`berserk`](https://github.com/rhgrant10/berserk) python client for the Lichess API.!\n- **Find your mistakes** by parsing your games and analysing them with [`python-chess`](https://github.com/niklasf/python-chess).\n- **Build a simple opening repertoire and list your known openings**\n- **Spaced repetition & Retrieval Practice**: Automatically (via [`apy`](https://github.com/lervag/apy)) or manually (via csv export) add your game mistakes, your openings and your tackled lichess puzzles into [`Anki`](https://apps.ankiweb.net/)\n- **Stats and visualizations**: Seamlessly show `lichess leaderboards` or plot your `rating history`.\n\n\n## Getting Started\n\n### Installation\n1. Install `pip`. See [here](https://pip.pypa.io/en/stable/installing/) for help.\n\n2.  Install chessli with `pip`:\n```console\npip install chessli\n```\nThat's it!\n\n## Basic Usage\nTo get help about `chessli`s commands, open your console and type:\n```console\nchessli --help\n```\nThe same works for subcommands, e.g., :\n```console\nchessli games --help\n```\nYou can find an overview of all availabe cli-commands [here](https://pwenker.com/chessli/cli/) in\nthe docs.\n\n### Youtube-Video: CLI Demo\n\n[![Chessli CLI Demo](https://img.youtube.com/vi/XbD71Kq7cx4/0.jpg)](https://www.youtube.com/embed/XbD71Kq7cx4)\n\nThere is also a short video showing the `chessli`s Anki cards in action:\n\n### Youtube-Video: Anki Cards Demo\n[![Chessli Anki Cards Demo](https://img.youtube.com/vi/aj-FqJhPyyA/0.jpg)](https://www.youtube.com/embed/aj-FqJhPyyA)\n\n\n### Tutorial\nNow as you are familiar with the basics, you might want to walk through the tutorial to get the most\nout of `chessli`!\nStart with [setting up chessli](tutorial/how_to_set_up_chessli.md).\n\n## Acknowledgments\n\n|  | Acknowledgements |\n| --- | --- |\n| [`Lichess`](https://lichess.org) | A free, no-ads, open source chess server that let's everyone play chess! Think about whether to [become a patron](https://lichess.org/patron)! :) |\n| [`Anki`](https://apps.ankiweb.net/) | A free and open-source flashcard program using spaced-repetition, a technique from cognitive science for fast and long-lasting memorization.  I couldn't imagine learning without it anymore. |\n| [`Anki Card Templates`](https://ankiweb.net/shared/info/1082754005) | The interactive chess functionality on Chessli's anki cards is based from [these fantastic cards](https://ankiweb.net/shared/info/1082754005).|\n| [`python-chess`](https://github.com/niklasf/python-chess) | Most of the heavy lifting, e.g. parsing games, finding mistakes, extracting openings, etc. is done with `python-chess`. |\n| [`berserk`](https://github.com/rhgrant10/berserk) |  The communication between `lichess` and `chessli` is performed via `berserk` |\n| [`typer`](https://github.com/tiangolo/typer) | The `chessli` `cli` is built with the great `typer` |\n| [`rich`](https://github.com/willmcgugan/rich) | The rich colors and fancy tables are made possible by `rich` |\n| [`apy`](https://github.com/lervag/apy/) | Importing cards directly into anki without csv-export can be done via `apy` |\n",
    'author': 'Pascal Wenker',
    'author_email': 'pwenker@posteo.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pwenker/chessli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
