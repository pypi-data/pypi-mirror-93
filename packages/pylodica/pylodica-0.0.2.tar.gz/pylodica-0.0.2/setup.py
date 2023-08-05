import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pylodica", # Replace with your own username
    version="0.0.2",
    author="Evan Chong",
    author_email="evan.tkchong@gmail.com",
    description="A Python framework for for creating music algorithmically",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/evantkchong/pylodica",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)