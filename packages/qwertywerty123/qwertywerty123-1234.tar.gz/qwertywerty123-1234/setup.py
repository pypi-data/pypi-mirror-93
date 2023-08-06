from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name = "qwertywerty123",
    version = "1234",
    description = "Discrete Event Simulator",
    long_description = readme(),
    long_description_content_type = "text/markdown",
    author = "NUS",
    license = "NUS",
    classsifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"
    ],
    packages = ["o2despy", "o2despy.log", "o2despy.application", "o2despy.demos"],
    include_package_data = True,
)

