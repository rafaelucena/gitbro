from setuptools import setup, find_packages

setup(
    name='gitbro',
    version='0.3.0',
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
            'gibr=gitbro.gibr.main:run',
            'gidf=gitbro.gidf.main:run',
        ]
    )
)

# gist - sketch done
# gibr - partially done
# gidf - sketch started
# giad
# gibk
# gicm
# gime
# gilg
# gicp - planned
# girs - planned
# gire - planned
