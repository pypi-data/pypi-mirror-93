import setuptools

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setuptools.setup(
    name='api-display-purposes',
    version='0.0.3',
    author='Kevin Nelson',
    author_email='keronels@ucsc.edu',
    description='python wrapper for displaypurposes.com\'s api ',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/KevinRNelson/displaypurposes',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
