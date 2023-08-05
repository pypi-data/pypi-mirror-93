from setuptools import setup
from codecs import open
from os import path

package_name = "CategoryReplacer"

long_discription = """
Categorical Feature Enginieering.

Include Method:
    CountEncoder
    CombinCountEncoder
    FrequencyEncoder
    NullCounter
    AutoCalcEncoder
"""


setup(
    name = "CategoryReplacer",
    version = "1.0.0",
    description='Categorical Features replace to Numerical Values.',
    long_description = long_discription,
    url = "https://github.com/yoshida121/CategoryReplacer",
    author = "yoshida121",
    author_email = "yoshida.pypi@gmail.com",
    install_requires = [
        "category_encoders",
        "numpy",
        "pandas",
        "scikit-learn"
        ]
)