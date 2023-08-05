# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pushbroom']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['pushbroom = pushbroom.console:run']}

setup_kwargs = {
    'name': 'pushbroom',
    'version': '1.0.0',
    'description': 'Clean up your filesystem',
    'long_description': '# Pushbroom\n\nPushbroom is a tool designed to help keep your filesystem clear of clutter.\nCertain directories, such as your downloads directory, tend to accumulate a\nlarge amount of old files that take up space. Over time, this clutter can\naccumulate to a significant amount of storage space. Pushbroom gives you an\neasy way to remove these old files.\n\nPushbroom is written in Python and should therefore work on any platform that\ncan run Python. For now, it is only officially supported for macOS and Linux.\n\n## Installation\n\n### Homebrew (macOS only)\n\nInstall via Homebrew:\n\n    brew install gpanders/tap/pushbroom\n\nCopy and modify the included `pushbroom.conf` file to\n`~/.config/pushbroom/config` and use `brew services start\ngpanders/tap/pushbroom` to start the automatic launchd daemon:\n\n    cp /usr/local/etc/pushbroom.conf ~/.config/pushbroom/config\n    brew services start gpanders/tap/pushbroom\n\nPushbroom will run once every hour.\n\n### pip\n\nInstall using pip:\n\n    pip install --user pushbroom\n\nYou must also copy the [example configuration file][] to\n`~/.config/pushbroom/config` or create your own from scratch.\n\n[example configuration file]: ./pushbroom.conf\n\n### From source\n\nCheck the [releases][] page for the latest release. Download and extract the\narchive, then install with pip:\n\n    tar xzf pushbroom-vX.Y.Z.tar.gz\n    cd pushbroom-vX.Y.Z\n    pip install --user .\n    cp pushbroom.conf ~/.config/pushbroom/config\n\n[releases]: https://git.sr.ht/~gpanders/pushbroom/refs\n\n## Usage\n\nPushbroom can be run from the command line using:\n\n    pushbroom\n\nUse `pushbroom --help` to see a list of command line options.\n\n## Configuration\n\nThe Pushbroom configuration file is organized into sections where each section\nrepresents a directory path to monitor. The default configuration file looks\nlike this:\n\n    [Downloads]\n    Path = ~/Downloads\n    Trash = ~/.Trash\n    NumDays = 30\n\nThis means that, by default, Pushbroom will monitor your ~/Downloads folder and\nmove any file or folder older than 30 days into your ~/.Trash directory.\n\nIf you don\'t want to move files into ~/.Trash but instead want to just delete\nthem, simply remove the `Trash` option:\n\n    [Downloads]\n    Path = ~/Downloads\n    NumDays = 30\n\nThe name of the section (`Downloads` in this example) is not important and can\nbe anything you want:\n\n    [Home Directory]\n    Path = ~\n    NumDays = 90\n\nYou can also specify an `Ignore` parameter to instruct Pushbroom to ignore any\nfiles or directories that match the given glob:\n\n    [Downloads]\n    Path = ~/Downloads\n    NumDays = 30\n    Ignore = folder_to_keep\n\nSimilarly, you can specify `Match` to have Pushbroom only remove files that\nmatch one of the given patterns:\n\n    [Vim Backup Directory]\n    Path = ~/.cache/vim/backup\n    NumDays = 90\n    Match = *~\n\nBoth `Ignore` and `Match` can be a list of patterns separated by commas.\n\n    [Home Directory]\n    Path = ~\n    NumDays = 365\n    Match = .*\n    Ignore = .local, .config, .cache, .vim\n\nNote that `.*` **is not** a regular expression for "match everything", but\nrather a _glob expression_ for "all files that start with a period".\n\n---\n\nThe following configuration items are recognized in `pushbroom.conf`:\n\n### Path\n\n**Required**\n\nAbsolute path to a directory to monitor. Tildes (`~`) are expanded to the\nuser\'s home directory.\n\n### Trash\n\nSpecify where to move files after deletion. If omitted, files will simply be\ndeleted.\n\n### NumDays\n\n**Required**\n\nNumber of days to keep files in `Path` before they are removed.\n\n### Ignore\n\n**Default**: None\n\nList of glob expression patterns of files or directories to ignore.\n\n### Match\n\n**Default**: `*`\n\nList of glob expression patterns of files or directories to remove. If omitted,\neverything is removed.\n\n### Shred\n\n**Default**: False\n\nSecurely delete files before removing them. Note that this option is mutually\nexclusive with the [`Trash`](#trash) option, with `Trash` taking precedence if\nboth options are used.\n\n### RemoveEmpty\n\n**Default**: True\n\nRemove empty subdirectories from monitored paths.\n\n## Automating\n\nIf installed via Homebrew then Pushbroom can be set to run once every hour\nusing\n\n    brew services start gpanders/tap/pushbroom\n\nAnother option is to install a crontab entry\n\n    0 */1 * * * /usr/local/bin/pushbroom\n\nIf you are using a Linux distribution that uses systemd, you can copy the\n[systemd service][] and [timer][] files to `~/.local/share/systemd/` and enable\nthe service with\n\n    systemctl --user enable --now pushbroom\n\nNote that you may need to change the path to the `pushbroom` script in the\nservice file depending on your method of installation.\n\n[systemd service]: ./contrib/systemd/pushbroom.service\n[timer]: ./contrib/systemd/pushbroom.timer\n\n## Contributing\n\n[Send patches][] and questions to [~gpanders/pushbroom@lists.sr.ht][].\n\nReport a bug or open a ticket at [todo.sr.ht/~gpanders/pushbroom][].\n\n[Send patches]: https://git-send-email.io\n[~gpanders/pushbroom@lists.sr.ht]: https://lists.sr.ht/~gpanders/pushbroom\n[todo.sr.ht/~gpanders/pushbroom]: https://todo.sr.ht/~gpanders/pushbroom\n\n## Similar Work\n\n- [Belvedere](https://github.com/mshorts/belvedere): An automated file manager\n  for Windows\n- [Hazel](https://www.noodlesoft.com/): Automated Organization for your Mac\n',
    'author': 'Gregory Anders',
    'author_email': 'greg@gpanders.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gpanders/pushbroom',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
