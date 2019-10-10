import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='livebook',
    version='0.0.1',
    packages=['livebook'],
    scripts=['livebook_run.py'],
    package_data={
        'livebook': ['static/*.css', 'templates/*.j2'],
    },

    author='GGB Team',
    description='Web service providing interactive adventure books',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/TheElderMindseeker/dads-project',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
