import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name='stackstats',
    version='1.0',
    author='Manolis Iliakis',
    description='StackOVerflow answer statistics.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['stackstats', 'tests'],
    install_requires=[
        'setuptools',
        'requests >= 2.25.0'
    ],
    python_requires='>=3.6',
    entry_points="""
    [console_scripts]
    stats=stackstats.stats:main
        """,
    test_suite="tests",

)