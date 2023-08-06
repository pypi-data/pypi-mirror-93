import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qmusic",
    version="0.0.2",
    author="Joppe Wolters (svenskithesource)",
    author_email="joppe.wolters@icloud.com (discord: svenskithesource#2815)",
    description="An unofficial Qmusic API Wrapper.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/svenskithesource/qmusic",
    packages=setuptools.find_packages("./qmusic"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["requests", "python-dateutil"]
)
