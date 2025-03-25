from setuptools import setup, find_packages

setup(
    name="emailaiagents",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'yagmail==0.15.293',
        'imbox==0.9.8',
        'python-dotenv==1.0.0',
    ],
) 