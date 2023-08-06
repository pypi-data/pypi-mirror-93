from distutils.core import setup
from setuptools import find_packages

def get_version():
    return open('version.txt', 'r').read().strip()

# with open('README.md', 'r') as fh:
#     long_description = fh.read()

setup(
    name='lins_servico',
    version=get_version(),
    packages=find_packages(),
    description='Pacote para gerenciar servicos atraves de threads',
    # long_description=long_description,
    # long_description_content_type='text/markdown',
    url='https://bitbucket.org/grupolinsferrao/pypck-servico/',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
    license='MIT',
    author='Gustavo Schaedler',
    author_email='gustavopoa@gmail.com',
)