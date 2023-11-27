## setup.py

"""Python Setup Manager"""

from setuptools import setup
from os.path import abspath, dirname, join

##

this_directory = dirname(abspath(__file__))
requirements_path = join(this_directory, "requirements.txt")

reqs = [line.strip('\n') for line in open(requirements_path, "r").readlines()]

##

VERSION = "1.2"

##

if __name__ == "__main__":
	setup(
		name="accessdata-ftkc-sdk",
		version=VERSION,
		description="Python Library for AccessData's FTKC API",
		author="Thomas Vieth",
		author_email="sriram.appusamy@exterro.com",
		url="https://github.com/AccessDataOps/FTKC-SDK",
		license = "MIT License",
		packages=[
			"accessdata",
			"accessdata.api"
		],
		install_requires=reqs,
		setup_requites=reqs,
		package_dir={"accessdata": "accessdata"},
		include_package_data=True
	)
