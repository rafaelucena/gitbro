from setuptools import setup

setup(
    name='gitbro',
    version='0.1',
    description='A bunch of handy commands to do things a bit faster using git command line (imho)',
    url='http://github.com/rafaelucena/gitbro',
    author='Rafael Boszko',
    author_email='rafael.boszko@gmail.com',
    license='MIT',
    entry_points=dict(
        console_scripts=[
            'test=gitbro.mock.main:run'
        ]
    )
)
