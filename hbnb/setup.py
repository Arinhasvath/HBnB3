from setuptools import setup, find_packages

setup(
    name="hbnb",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask>=2.0.1",
        "SQLAlchemy>=1.4.23",
        "Flask-SQLAlchemy>=2.5.1",
        "pytest>=7.1.1",
        "pytest-cov>=3.0.0",
        "flask-testing>=0.8.1",
    ],
    python_requires=">=3.7,<3.9",
)
