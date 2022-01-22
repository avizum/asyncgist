from setuptools import setup

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()


setup(
    name="asyncgist",
    author="avizum",
    version="1.0.1a",
    packages=["asyncgist"],
    url="https://github.com/avizum/asyncgist",
    description="Async wrapper around the GitHub Gist API",
    python_requires=">=3.8.0",
    install_requires=requirements,
    license="MIT",
)
