from setuptools import setup, find_packages

setup(
    name="rmpy",
    version="0.1.0",
    description="A Python module for interacting with RateMyProfessors.com",
    author="lumirth",
    author_email="lu@mirth.cc",
    url="https://github.com/lumirth/rmpy",  # Replace with the URL of your project repository
    packages=find_packages(),
    install_requires=[
        "aiohttp",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
)
