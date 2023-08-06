import setuptools
import philog


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="philog",
    packages=['philog'],
    version=philog.__version__,
    author="Raphael Hungria",
    author_email="rhja93@gmail.com",
    description="Threaded logger for personal use",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rahungria/philog",
    download_url='https://github.com/rahungria/philog/archive/0.1.3.tar.gz',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)