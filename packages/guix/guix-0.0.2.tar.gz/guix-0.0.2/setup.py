from setuptools import setup, find_packages

setup(
    name="guix",
    version="0.0.2",
    description="Make faster cross platform GUI",
    long_description=open('README.md').read() + '\n\n',
    url="",
    author="Venkataramana",
    author_email="",
    license="MIT",
    classifiers=[""],
    keywords="Gui",
    packages=find_packages(),
    install_requires=[''],
    py_modules=["guix"],
    package_dir={'':'src'}
)