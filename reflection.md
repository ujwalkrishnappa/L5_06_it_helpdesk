# Lab 5 Reflection

## 1. What was the purpose of this lab?

I used Pylint, Bandit, and Flake8 to examine a Python helpdesk ticket program.
The tools helped me find code quality, security, and formatting problems.

## 2. What important problems did I fix?

I removed the unsafe shell command and moved the admin password out of the
source code. I also fixed input validation, error handling, and a shared
mutable default argument.

## 3. How did I check that my fixes worked?

I ran all three analysis tools again and saved their before-and-after reports.
The final Pylint score was 10/10, while Bandit had no unsuppressed findings and
Flake8 reported no issues.

## 4. What did I learn from this lab?

I learned that static analysis tools can help identify security, quality, and
style issues, but they do not catch every behavior bug. Testing the program
and reading its output are also important.
