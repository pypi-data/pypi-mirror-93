from setuptools import setup

with open("README.md", 'r') as fh:
    long_description = fh.read()

setup(
    name='helloworld-23487978234789',
    version='0.0.1',
    description='Say Hello!',
    py_modules=['helloworld'],
    package_dir={'': 'src'},
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires = [
        'blessings ~= 1.7'
        ],
    extras_require = {
            "dev": [
                "pytest>=3.7"
                ]
        },
    url="https://github.com/ashutoshc8101/helloworld",
    author="ashutoshc8101",
    author_email="ashutoshc8101@gmail.com"

)
