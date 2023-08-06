# bank
This is an example project demonstrating how to publish a python module to pypi.

##installation

Run the following to install

'''python
pip install bank
'''

##usage

'''python
from bank2 import deposit_amount
from bank2 import withdraw_amount
from bank2 import home_loan
from bank2 import personal_loan
from bank2 import vehicle_loan
from bank2 import home_loan
# if you want deposit a amount
dep_amount=deposit_amount.dep_amount(10000,10000000)
print(dep_amount)
# if you want withdraw a amount
with_amount=withdraw_amount.with_amount(1000,10000)
print(with_amount)

#home_loan
h_loan=home_loan.hm_loan(10000)
print(h_loan)
#personal_loan
per_loan=personal_loan.per_loan(1000)
print(per_loan)
#vehicle_loan

v_loan=vehicle_loan.ve_loan(10000)
print(v_loan)

'''
'''python
pip install -e .[dev]