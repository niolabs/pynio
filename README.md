# pynio

A module for interacting with running nio instance's REST API.

## Installation

(Coming Soon) Install from PyPi using [pip](http://www.pip-installer.org/en/latest/), a
package manager for Python.

    pip install pynio

Don't have pip installed? Try installing it, by running this from the command
line:

    $ curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python

Or, you can [download the source code
(ZIP)](https://github.com/neutralio/nio-python/zipball/master "nio-python
source code") for `nio-python`, and then run:

    python setup.py install

You may need to run the above commands with `sudo`.

## Getting Started

To get started, create an `Instance` and you're ready to go.

### Instance configuration

The `Instance` needs a host, port and credentials.

```python
from pynio import Instance

host = "127.0.0.1"
port = 8181
creds = ('User', 'User')
instance = Instance(host, port, creds)
```

The `Instance` has default values, so the same thing could be shortened.

```python
from pynio import Instance
instance = Instance()
```

### Find services a block is used in

```python
from pynio import Instance
instance = Instance()
for b in i.blocks:
    print(b)
    [print(s.name) for s in b.in_use()]
```
