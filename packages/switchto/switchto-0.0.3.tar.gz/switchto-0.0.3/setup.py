import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="switchto", # Replace with your own username
    version="0.0.3",
    author="Hanan Beer",
    author_email="email@hanan.beer",
    license='MIT',
    description="switch between dev and prod environments from command line",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hananbeer/switchto",
    packages=setuptools.find_packages(),
    py_modules=['switchto'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
    keywords='cli dev tool'
)
