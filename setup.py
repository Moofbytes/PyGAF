import setuptools

long_description = 'Evaluation and display of analytic groundwater solutions.'

setuptools.setup(
    name='pygaf',
    version='0.0.1',
    author='Tony Smith',
    author_email='tony@moofbytes.com',
    description='Python Groundwater Analytic Flow',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Moofbytes/PyGAF',
    project_urls = {
        'Documentation': 'https://pygaf.readthedocs.io/en/latest/index.html',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Hydrology',
        'Development Status :: 3 - Alpha',
    ],
    license='MIT',
    packages=['pygaf', 'pygaf.solutions'],
)
