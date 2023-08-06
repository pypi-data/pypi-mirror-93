import setuptools

setuptools.setup(
    name="appchance-django",
    version="0.2.1",
    author_email="backend@appchance.com",
    short_description="Appchance Django Extensions",
    description="Common extensions for Django projects.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/appchance/appchance-django/",
    packages=setuptools.find_packages(),
    install_requires=["django", "swapper"],
    scripts=[],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.8",
)
