from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='floa',
    version='1.0.0',
    author="Ray Sutton",
    author_email="ray.sutton@gmail.com",
    description="My Library of America bookshelf manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rsutton/floa",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'bs4', 'filelock', 'flask', 'flask-login', 'pyOpenSSL', 'requests', 'requests_oauthlib'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)