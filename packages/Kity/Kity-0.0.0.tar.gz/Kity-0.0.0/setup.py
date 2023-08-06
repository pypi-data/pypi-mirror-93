import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Kity",
    version="0.0.0",
    author="Hrishikesh Arun",
    author_email="hrishikesh28arun@gmail.com",
    description="A simple graphics module.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Topic :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta"
    ],
    install_requires=[
        "Kivy[full]",
        "Kivy >=2.0.0",
        "kivy_examples"
    ],
    python_requires='>=3.8',
)