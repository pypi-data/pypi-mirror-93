from setuptools import setup
with open('README.md','r') as file:
    long_description=file.read()
    
setup(
    name='bank2',
    version='0.0.1',
    description='Say bank',
    py_modules=["deposit_amount","home_loan","personal_loan","vehicle_loan","withdraw_amount"],
    package_dir={'':'naga_upputuri_bank'},

    classifiers=[
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.9",
          "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
          "Operating System :: OS Independent",
        ],

     long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "blessings~=1.7",
        ],
    extras_require={
        "dev":["pytest>=3.7",],},

    url="https://github.com/naga99552/bank2",
    author="Nagababu",
    author_email="nagababuupputuri52@gmail.com",
    )
