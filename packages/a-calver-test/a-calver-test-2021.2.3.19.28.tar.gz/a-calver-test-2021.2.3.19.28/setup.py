import time
from setuptools import setup

setup(
    name="a-calver-test",
    version=time.strftime('%Y.%m.%d.%H.%M', time.gmtime()),
    # use_calver="%Y.%m.%d.%H.%M",
    # setup_requires=['calver'],
    description="A CalVer demo",
    author="Jamie Bliss",
    author_email="jamie@ivyleav.es",
    url='https://github.com/AstraLuma/a-calver-test',
    packages=['a_calver_test'],
    install_requires=[],
)
