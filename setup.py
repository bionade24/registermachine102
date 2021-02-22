from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "rm102",
    version = "0.1",
    description = "Registermachine 102: Better implementation of rm101, a fake assembler for educational purposes.",
    long_description= long_description,
    long_description_content_type="text/markdown",
    url = "https://github.com/bionade24/registermachine102",
    author = "Oskar Roesler (bionade24)",
    author_email = "o.roesler@oscloud.info",
    license = "GPLv3",
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        # Pick your license as you wish
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        "Operating System :: POSIX :: Linux",
    ],
    install_requires = ["argparse", "docker-compose"],
    packages = ["rm102"],
    scripts = ["bin/rm102"]
)
