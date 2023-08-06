import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pykidgui", # Replace with your own username
    version="1.1.3",
    author="Ronan Bastos",
    author_email="Ronanbastos@hotmail.com",
    description="Simple gui de python para uso rapido e pratico / Simple python gui for quick and practical use",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ronanbastos/pykidgui",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
