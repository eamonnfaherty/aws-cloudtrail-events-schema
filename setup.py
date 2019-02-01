import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aws-cloudtrail-events-schema",
    version="0.0.6",
    author="Eamonn Faherty",
    author_email="python-packages@designandsolve.co.uk",
    description="Utility to discover AWS CloudTrail events pushed into S3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eamonnfaherty/aws-cloudtrail-events-schema",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'cloudtrail-schema = aws_cloud_trail_events_schema.cli:schema'
    ]},
    install_requires=[
        "botocore",
        "Click",
    ],
)
