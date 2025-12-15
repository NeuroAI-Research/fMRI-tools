from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="fMRI-tools",
    version="0.0.1",
    author="Ricky Ding",
    author_email="e0134117@u.nus.edu",
    description="???",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NeuroAI-Research/fMRI-tools",
    packages=find_packages(),
    install_requires=open("requirements.txt").read().splitlines(),
    python_requires=">=3.8",
    license="MIT",
    keywords=[],
    classifiers=[],
)
