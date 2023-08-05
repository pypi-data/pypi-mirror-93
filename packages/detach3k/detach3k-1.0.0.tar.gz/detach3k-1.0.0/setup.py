# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['detach']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'detach3k',
    'version': '1.0.0',
    'description': 'Fork and detach the current process.',
    'long_description': 'Detach\n======\nFork and detach the current process.\n\n[![Build Status](https://travis-ci.org/BlueDragonX/detach.svg)](https://travis-ci.org/BlueDragonX/detach)\n\nUsage\n-----\nThe `detach` package contains a context manager called `Detach`. It is used\nwith `with` statement to fork the current process and execute code in that\nprocess. The child process exits when the context manager exits. The following\nparameters may be passed to `Detach` to change its behavior:\n\n* `stdout` - Redirect child stdout to this stream.\n* `stderr` - Redirect child stderr to this stream.\n* `stdin` - Redirect his stream to child stdin.\n* `close_fds` - Close all file descriptors in the child excluding stdio.\n* `exclude_fds` - Do not close these file descriptors if close_fds is `True`.\n* `daemonize` - Exit the parent process when the context manager exits.\n\nExamples\n--------\n### Simple Fork with STDOUT\n\n    import detach, os, sys\n\n    with detach.Detach(sys.stdout) as d:\n        if d.pid:\n            print("forked child with pid {}".format(d.pid))\n        else:\n            print("hello from child process {}".format(os.getpid()))\n\n### Daemonize \n\n    import detach\n    from your_app import main\n\n    def main():\n        """Your daemon code here."""\n\n    with detach.Detach(daemonize=True) as d:\n        if d.pid:\n            print("started process {} in background".format(pid))\n        else:\n            main()\n\n### Call External Command\n\n    import detach, sys\n    pid = detach.call([\'bash\', \'-c\', \'echo "my pid is $$"\'], stdout=sys.stdout)\n    print("running external command {}".format(pid)) \n    \n\nLicense\n-------\nCopyright (c) 2014 Ryan Bourgeois. This project and all of its contents is\nlicensed under the BSD-derived license as found in the included [LICENSE][1]\nfile.\n\n[1]: https://github.com/bluedragonx/detach/blob/master/LICENSE "LICENSE"\n',
    'author': 'Julia Patrin',
    'author_email': 'papercrane@reversefold.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/reversefold/detach',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
