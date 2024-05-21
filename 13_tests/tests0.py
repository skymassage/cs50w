# We are going to writing a function to test the "is_prime" function in prime.py:

from prime import is_prime
def test_prime(n, expected):
    if is_prime(n) != expected:
        print(f"ERROR on is_prime({n}), expected {expected}")

# Go into the python interpreter (enter the current directory and run "python3" in the terminal) to test out the following code:
'''
>>> from tests0 import test_prime
>>> test_prime(5, True)
>>> test_prime(10, False)
>>> test_prime(25, False)
ERROR on is_prime(25), expected False
'''
# We can see from the output above that 5 and 10 were correctly identified as prime and not prime, 
# but 25 was incorrectly identified as prime, so there must be something wrong with our function. 
