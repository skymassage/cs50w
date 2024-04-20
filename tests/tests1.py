# Even though we were able to run tests automatically using the above method, 
# we still might want to avoid having to write out each of those tests. 
# We can use the Python "unittest" library to make this process a little bit easier. 

import unittest
from prime import is_prime

class Tests(unittest.TestCase):  # A class containing all of our tests
    # The name of the functions must begin with "test_" so that the functions could run automatically with the call to "unittest.main()".
    def test_1(self):
        # This is a docstring surrounded by three quotation marks, and not just for the code's readability.
        # When the tests are run, the comment will be displayed as a discription of the test if it fails.
        """Check that 1 is not prime."""
        
        # There are many different assertions you can make including "assertTrue", "assertFalse", "assertEqual", "assertGreater", etc.
        self.assertFalse(is_prime(1))

    def test_2(self):
        """Check that 2 is prime."""
        self.assertTrue(is_prime(2))

    def test_8(self):
        """Check that 8 is not prime."""
        self.assertFalse(is_prime(8))

    def test_11(self):
        """Check that 11 is prime."""
        self.assertTrue(is_prime(11))

    def test_25(self):
        """Check that 25 is not prime."""   # We will see this line in the terminal if this test fails.
        self.assertFalse(is_prime(25))

    def test_28(self):
        """Check that 28 is not prime."""
        self.assertFalse(is_prime(28))


# Run each of the testing functions
if __name__ == "__main__":
    unittest.main()

# Run this file and see the following results in the terminal:
'''
...F.F
======================================================================
FAIL: test_25 (__main__.Tests)
Check that 25 is not prime.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "tests1.py", line 26, in test_25
    self.assertFalse(is_prime(25))
AssertionError: True is not false

======================================================================
FAIL: test_8 (__main__.Tests)
Check that 8 is not prime.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "tests1.py", line 18, in test_8
    self.assertFalse(is_prime(8))
AssertionError: True is not false

----------------------------------------------------------------------
Ran 6 tests in 0.001s

FAILED (failures=2)
'''
# In the first line, it gives us a series of '.' for successes and 'F' for failures in the order our tests were written:
#      ...F.F
# For the first test that failed, we are then given the name of the function that failed: 
#     FAIL: test_25 (__main__.Tests)
# The next line is the descriptive comment we provided earlier:
#     Check that 25 is not prime.
# And a traceback for the exception:
#     Traceback (most recent call last):
#       File "tests1.py", line 26, in test_25
#         self.assertFalse(is_prime(25))
#     AssertionError: True is not false
# Finally, we are given a run through of how many tests were run, how much time they took, and how many failed:
#     Ran 6 tests in 0.001s
#     
#     FAILED (failures=2)

# If we fix the bug by changing the for loop in the "prime.py" file and then run this file again, we will see:
'''
......
----------------------------------------------------------------------
Ran 6 tests in 0.000s

OK
'''