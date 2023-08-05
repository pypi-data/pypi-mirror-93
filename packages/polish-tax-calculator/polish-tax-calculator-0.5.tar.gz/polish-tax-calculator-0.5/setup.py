from setuptools import setup, find_packages

setup(
    name='polish-tax-calculator',
    description="Kalulator podatkowy dla działalności gospodarczej w formie CLI",
    long_description="""
#### Użycie

```shell
ptc --help
```

#### przykład 1. opcje domyślne: pełen zus, podatek liniowy, bez składki chorobowej
```shell
ptc 5000 
```

#### przykład 2: obniżony zus, ryczałt 5%, składka chorobowa, więcej szczegółów (-v)
```shell
ptc -t income -z reduced -si -itr 5 -v 5500 
```
""",
    long_description_content_type='text/markdown',
    version='0.5',
    python_requires='>=3.6',
    author="Kamil Hark",
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'Click'
    ],
    entry_points='''
        [console_scripts]
        ptc=ptc.ptc:cli
    ''',
)