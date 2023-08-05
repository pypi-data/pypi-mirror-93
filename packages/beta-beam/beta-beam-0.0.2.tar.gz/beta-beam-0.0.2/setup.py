import setuptools

with open("README", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# recuerda que quieres probar meter el .lnk

setuptools.setup(
    name="beta-beam",
    version="0.0.2",
    author="patod01",
    author_email="patod01@telegmail.com",
    license='WTFPL',
    description="My last hope to get a degree",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/patod01/beta-beam",
    #project_urls={},
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: Freeware",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
    install_requires=['Pillow'],
    python_requires='>=3.9',
    # entry_points={
    #     'console_scripts': [
    #         '',
    #     ],
    # },
)
