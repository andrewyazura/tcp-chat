from setuptools import setup

setup(
    name="tcp-chat",
    version="0.1.0",
    py_modules=["server", "client"],
    install_requires=["Click", "colorama"],
    entry_points={"console_scripts": ["server = server:main", "client = client:main"]},
)
