import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="EngineeringToolbox-JP", # Replace with your own username
    version="0.0.1",
    author="Joshua H. Phillips",
    description="Package containing python programs for common problems in mechanical engineering curriculum.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jhphillips1029/EngineeringToolbox",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
    	'json',
    	'math',
    	'matplotlib',
    	'numpy',
    	'pandas',
    	'sympy',
    	'warnings'
    ],
    python_requires='>=3.6',
)
