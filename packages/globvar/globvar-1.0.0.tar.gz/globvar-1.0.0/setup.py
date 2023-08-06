from setuptools import setup
from globvar import __version__

with open('README.md') as f:
    readme = f.read() or ''

setup(
    name='globvar',
    version=__version__,
    description='Extremely simple in-memory global variable manager',
    author='Technofab',
    author_email='globvar.git@technofab.de',
    url='https://gitlab.com/TECHNOFAB/globvar',
    license='MIT',
    packages=["globvar"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    long_description=readme,
    long_description_content_type="text/markdown"
)
