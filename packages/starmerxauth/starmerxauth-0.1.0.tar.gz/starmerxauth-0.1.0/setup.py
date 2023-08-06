from setuptools import setup, find_packages

setup(
    name="starmerxauth",
    version="0.1.0",
    author="yang",
    author_email="",
    description="starmerx verify jwt",
    license="MIT",
    url="",  # github
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        #"License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    install_requires=[
        "PyJWT== 1.7.1",
        "cryptography==3.3.1"
    ],
    zip_safe=True,
)
