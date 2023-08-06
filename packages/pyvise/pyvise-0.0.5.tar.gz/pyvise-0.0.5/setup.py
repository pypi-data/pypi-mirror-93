import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("VERSION", "r", encoding="utf-8") as fh:
    version = fh.read()

setuptools.setup(
    name="pyvise", # Replace with your own username
    version=version,
    author="Dennis Payonk",
    author_email="dennis@payonk.com",
    description="A small authentication package using FastAPI and magic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dpayonk/pyvise",
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'aiofiles>=0.6.0',
        'dataclasses-json>=0.5.2',
        'fastapi>=0.63.0',
        'fastapi-jwt-auth>=0.5.0',
        'pydantic>=1.7.3',
        'magic-admin>=0.0.4',
        'requests>=2.22.0'
    ]
)