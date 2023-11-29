
# c'est vraiment utile?
#
from setuptools import setup
setup(
    name='swarm_app',
    version='0.1.0',
    packages=['swarm_app'],
    install_requires=['invoke', 'python-slugify'],
    entry_points={
        'console_scripts': ['swarm-app = swarm_app.swarm-app:program.run']
    }
)

