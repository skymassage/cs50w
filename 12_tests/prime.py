# As you begin building larger projects, you may want to consider using test-driven development, 
# a development style where every time you fix a bug, you add a test that checks for that bug to a growing set of tests that are run every time you make changes. 
# This will help you to make sure that additional features you add to a project don't interfere with your existing features.

import math

# Note that this function cannot completely determine whether each non-negative integer is prime,
# because we want the testing program to find the errors.
def is_prime(n): 
    if n < 2:                                    # We know numbers less than 2 are not prime
        return False

    for i in range(2, int(math.sqrt(n))):        # Checking factors up to sqrt(n)
    # for i in range(2, int(math.sqrt(n)) + 1):  # This is the right loop.
        if n % i == 0:                           # If i is a factor, return false
            return False

    return True                                  # If no factors were found, return true