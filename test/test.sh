# One way we can automate our testing is by creating a shell script, or some script that can be run inside our terminal.
# These files require a ".sh" extension, so our file will be called "test.sh". Each of the lines below consists of three parts:
# 1. A "python3" to specify the Python version we’re running
# 2. A "-c" to indicate that we wish to run a command
# 3. A command to run in string format
# You can also directly run the following in the terminal without entering the python interpreter.

python3 -c "from test import test_prime; test_prime(1, False)"
python3 -c "from test import test_prime; test_prime(2, True)"
python3 -c "from test import test_prime; test_prime(8, False)"
python3 -c "from test import test_prime; test_prime(11, True)"
python3 -c "from test import test_prime; test_prime(25, False)"
python3 -c "from test import test_prime; test_prime(28, False)"

# Enter the current directory and run these commands by running "./test.sh" in the terminal, giving us this result:
# ERROR on is_prime(8), expected False
# ERROR on is_prime(25), expected False