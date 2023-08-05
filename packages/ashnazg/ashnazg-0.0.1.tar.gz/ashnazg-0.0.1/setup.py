import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
	long_description = fh.read()

setuptools.setup(
	name="ashnazg",
	version="0.0.1",
	author="Xander",
	author_email="xander@ashnazg.com",
	description="A package for handling data in a FAIR way",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://ashnazg.com/docs/lib/fairy/",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)
