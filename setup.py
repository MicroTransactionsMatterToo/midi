from setuptools import setup, find_packages

setup(
    name="midi",
    version="0.0.1",
    author="Ennis Massey",
    author_email="ennisbaradine@gmail.com",
    description="Standard MIDI file parser for Python",

    license="MIT",
    keywords="midi file parser library",
    packages=find_packages(),
    install_requires=[
        "typing"
    ],
    classifiers=[
        "Developement Status :: 3 - Alpha",
        "Topic :: Utilites",
        "License :: OSI Approved :: MIT License"
    ]
)
