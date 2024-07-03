from setuptools import find_packages, setup  

with open("../README.md", "r") as f:
    long_description = f.read()
    
setup(
    name="wemonitor",
    version="1.0.0",
    description="A package to monitor the health of a web service",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    package_data={"": ["certs/*", "data/*"]},
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aiven-recruitment/sre-20250531-lbourgeois87",
    author="Laurent Bourgeois",
    author_email="laurent.bourgeois@elekta.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        "requests==2.32.3",
        "kafka-python==2.0.2",
        "pyOpenSSL==20.0.1",
    ],
    extras_require={
        "dev": ["pytest==6.2.4", "twine==3.4.2"],
    },
    python_requires="==3.8.10"
)