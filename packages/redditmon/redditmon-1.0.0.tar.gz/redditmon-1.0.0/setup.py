import pathlib
import setuptools

here = pathlib.Path(__file__).parent


with open(f"{here}/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="redditmon",
    version="1.0.0",
    author="Chris Cummings",
    author_email="nouser@slash64.tech",
    description="A simple package for viewing reddit posts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cummings-chris/redditmon",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['praw'],
    entry_points={
        'console_scripts': [
            'redditmon = redditmon.redditmon:redditmon_cli',
        ],
    },
    python_requires='>=3.6',
)
