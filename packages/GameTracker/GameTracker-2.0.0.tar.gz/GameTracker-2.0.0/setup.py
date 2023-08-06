import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GameTracker",
    version="2.0.0",
    author="Harry Kearney",
    author_email="kearneyharry8@gmail.com",
    description="A simple way to get player stats from a variety of games.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/harrykearney/GameTracker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6',
)