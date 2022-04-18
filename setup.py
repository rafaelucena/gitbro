from setuptools import setup, find_packages

setup(
    name='gitbro',
    version='0.2.0',
    description='A bunch of handy commands to do things a bit faster using git command line (imho)',
    url='http://github.com/rafaelucena/gitbro',
    author='Rafael Boszko',
    author_email='rafael.boszko@gmail.com',
    license='MIT',
    packages=find_packages(),
    entry_points=dict(
        console_scripts=[
            'gitbro=gitbro.mock.main:run',
            'gist=gitbro.gist.main:run',
        ]
    )
)
