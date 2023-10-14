from setuptools import find_packages, setup

setup(
    name="duck_me",
    packages=find_packages(exclude=["duck_me_tests"]),
    install_requires=[
        "dagster", 
        "dagster-duckdb",
        "pandas",
        "dlt",
        "boto3",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest", "localstack", "awscli", "awscli-local"]},
)
