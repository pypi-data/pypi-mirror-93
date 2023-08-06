from setuptools import find_packages
from setuptools import setup

setup(
    name='currency_exchange',
    version='1.0.0',
    packages=find_packages(),
    author='Vadim Rashkevich',
    author_email='v.rashkevich@godeltech.com',
    url='https://gitlab.godeltech.com/v.rashkevich/currencyexchange',
    python_requires='>=3.6',
    install_requires=['requests', 'pytest'],
    entry_points={
        "console_scripts": [
            "currency_exchange = CurrencyExchange.menu:arg",
        ]
    }
)
