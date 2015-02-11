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

### Running a service

```python
from pynio import Instance
instance = Instance()

service = instance.services.get('my_service')

service.start()
print(service.status) # Started
print(service.pid)
service.stop()
print(service.status) # Stopped
```

### Creating blocks

```python
from pynio import Instance, Block
instance = Instance()

sim = Block('sim', 'Simulator')
instance.add_block(sim) # NOTE: should this be called create instead of add?
logger = Block('logger', 'LoggerBlock')
instance.add_block(logger)

sim.config = {'interval': {'seconds': 5}} # ideally this would be: sim['interval']['seconds'] = 5
sim.save() # Raises Exception if not already added to instance.
```

### Creating services

```python
from pynio import Instance, Service
instance = Instance()

sim = instance.blocks.get('sim')
logger = instance.blocks.get('logger')

service = Service('new_service')
service.connect(sim, logger) # NOTE: should you have to add the blocks to the service first?
instance.add_service(service) # NOTE: should this be called create instead of add?

# now update the service
sim2 = instance.blocks.get('sim2')
service.connect(sim2, logger)
service.save() # Raises Exception if not already added to instance.
```
