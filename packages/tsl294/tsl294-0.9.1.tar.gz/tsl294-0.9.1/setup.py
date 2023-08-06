import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tsl294",
    version="0.9.1",
    author="Drak Lowell",
    description="Transport secure layer version 294",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/draklowell/TSL294",
    packages=["tsl294", "tsl294.crypto"],
    license='Apache License 2.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
    ],
    install_requires = [
        'func-timeout>=4.3.5',
        'dcn>=2.0.0.4.1.2'
    ],
    python_requires='>=3.8',
)