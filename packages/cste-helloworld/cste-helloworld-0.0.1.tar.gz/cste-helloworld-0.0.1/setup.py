from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
	name="cste-helloworld",
	version="0.0.1",
	description="Say hello cste!",
	py_modules=["cstehelloworld"],
	package_dir={"": "src"},
	long_description=long_description,
	long_description_content_type="text/markdown",
	# https://pypi.org/classifiers/
	classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://bitbucket.org/corporativo-ste/cste-helloworld",
    author="Corporativo STE",
    author_email="corporativoste7@gmail.com",
    install_requires = [
        "blessings ~= 1.7",
    ],
    extras_require = {
        "dev": [
            "pytest >= 3.7",
            "check-manifest",
            "twine",
        ],
    },
)