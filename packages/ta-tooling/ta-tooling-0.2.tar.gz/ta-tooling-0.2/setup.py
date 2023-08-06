from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ta-tooling",
    version="0.2",
    description="Various tools for TA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    author="Krerkkiat Chusap",
    author_email="kc555014@ohio.edu",
    license="MIT",
    url="https://github.com/krerkkiat/ta-tooling",
    python_requires=">=3.8",
    package_dir={"": "src"},
    packages=["ta_tooling", "bbutils"],
    install_requires=[
        "click>=7.1.2",
        "flask>=1.1.2",
        "flask-cors>=3.0.10",
        "selenium>=3.141.0" "requests>=2.25.1",
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "ta-tooling=ta_tooling.cli:main",
        ]
    },
)
