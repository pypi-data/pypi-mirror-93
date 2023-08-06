import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
    name='HQProxy',
    version='2.0.0',    
    description='HQ Trivia Proxy UK & USA',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Technology-cell/HQProxy',
    author='Technology-cell',
    author_email='kd2346751@gmail.com',
    packages=['HQProxy'],
    install_requires=['free-proxy','urllib3'],
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
