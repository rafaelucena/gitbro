from setuptools import setup, find_packages

setup(
    name='gitbro',
    version='0.13.0',
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
            'giad=gitbro.giad.main:run',
            'gibk=gitbro.gibk.main:run',
            'gilg=gitbro.gilg.main:run',
            'gime=gitbro.gime.main:run',
            'gicm=gitbro.gicm.main:run',
            'gipx=gitbro.gipx.main:run',
        ]
    )
)

# gist - mostly done
# gibr - partially done - planned: return to last used branch, show merged, allow local alias listing
# gidf - mostly done - planned: generating patch, applying it and comparing branches/commits
# giad - mostly done - planned: option to add only the first file matching a string
# gibk - mostly done - planned: show a brief description of a stash when using the index as well
# gilg - mostly done - planned: compare before/after, add by author
# gime - mostly done
# gicm - mostly done
# gipx - mostly done
# gicp - planned
# girs - planned
# gire - planned
