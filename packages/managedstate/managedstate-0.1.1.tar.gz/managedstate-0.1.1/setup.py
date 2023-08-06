from setuptools import setup

with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name="managedstate",
    packages=[
        "managedstate", "managedstate.extensions",
        "managedstate.extensions.listeners", "managedstate.extensions.registrar"
    ],
    version="0.1.1",
    license="MIT",
    description="State management inspired by Redux",
    long_description_content_type="text/markdown",
    long_description=long_description,
    author="immijimmi",
    author_email="imranhamid99@msn.com",
    url="https://github.com/immijimmi/managedstate",
    download_url="https://github.com/immijimmi/managedstate/archive/v0.1.1.tar.gz",
    keywords=[
        "state", "managed", "management", "access", "data"
    ],
    install_requires=[
        "objectextensions>=0.2.0"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],
)
