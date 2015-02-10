try:
    from setuptools import setup,
except ImportError:
    from distutils.core import setup

config = {
    name='nioapi',
    version='0.1dev',
    packages = ['nioapi'],
    install_requires = [
        'requests'
    ],
    description="Python interface for n.io REST API",
    url="docs.n.io/en/latest/nio-python.html"
}

setup(**config)
