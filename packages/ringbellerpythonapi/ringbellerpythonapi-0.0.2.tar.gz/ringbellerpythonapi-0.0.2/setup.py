import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
	long_description = fh.read()

setuptools.setup(
	name="ringbellerpythonapi",
	version="0.0.2",
	author="blueinsight",
	author_email="dobreovidiu@yahoo.com",
	description="Ringbeller IoT - Cellular library Python bindings",
	long_description=long_description,
	long_description_content_type="text/markdown",
	packages=setuptools.find_packages(),
	include_package_data = True,
	classifiers=[
		"Programming Language :: Python :: 3",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6'
)