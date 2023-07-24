from setuptools import setup, find_packages


setup(
    name="drs-uploader",
    version="0.0.1",
    long_description_content_type='text/markdown',
    description="Upload file data and register metadata with Data Repository Service (DRS) web services",  # noqa
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
    ],
    packages=find_packages(),
    install_requires=[
        "crypt4gh",
        "minio",
        "requests",
        "ga4gh-drs-client @ git+https://github.com/PacificAnalytics/pa-DRS-Crypt4GH-Downloader@06c6e83f5c274100d23c6a383f69f45681c2c473",
    ],
    entry_points={
        'console_scripts': [
            'drs-uploader=uploader.main:main',
            'drs-client=uploader.client:cli',
        ],
    }
)
