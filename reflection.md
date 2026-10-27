# Reflection

The provided handout asks for reflection answers but does not print individual
reflection questions. These four lab-related prompts and answers cover what I
learned from running the tools and fixing the program.

## 1. Which issues were easiest and hardest to fix?

The easiest fixes were the mechanical ones: changing `== None` to `is None`,
removing the unused `t2` variable, adding docstrings, and correcting blank
lines. The tools named the rule and the location, so I could see what to
change.

The hardest issue was the unsafe ping command. The original code put the
hostname into a command string and asked the shell to run it. I changed this
to a list of separate arguments, validated the hostname, and avoided invoking
a shell. I also had to account for the different ping count options on Windows
and Unix-like systems. Moving the admin password to an environment variable
was another important change: the program now needs
`HELPDESK_ADMIN_PASSWORD` set before an administrator can close a ticket.

## 2. Did the tools report false positives or miss real problems?

Bandit's subprocess checks are cautious pattern warnings. It reports the use
of `subprocess` even though the final code passes a fixed argument list and
does not start a shell. I reviewed those calls and used narrowly scoped
`# nosec` codes to document why the warnings do not apply. The after report
states that there are no unsuppressed findings and shows the three suppressed
checks.

The tools did not detect every behavior problem. They did not flag that the
original program accepted urgency values outside 1-5 or silently ignored a
failed ticket-close operation. Running the program and checking its behavior
helped reveal these problems. Static analysis checks code patterns; it does
not replace testing the program.

## 3. How would you use static analysis in a normal development workflow?

I would enable Flake8 and Pylint in my editor so style and code-quality issues
appear while I work. I would run Bandit, Pylint, Flake8, and automated tests
on each proposed code change in continuous integration (CI). CI could fail
when security findings remain, formatting checks fail, or the Pylint score
falls below the team's target. Static analysis should be used with tests and
code review, because each catches different kinds of problems.

## 4. What improvements did you make to the code?

- **Security:** the ping command no longer uses a shell, and the admin
  password is read from the environment instead of the current source file.
- **Reliability:** invalid urgency values are rejected, errors are visible,
  and the ticket file is closed safely even if writing raises an error.
- **Readability:** names use `snake_case`, the code has docstrings, and
  f-strings and PEP 8 spacing make it easier to follow.
- **Maintainability:** the demo only runs when the file is executed directly.
  Pylint improved from 5.53/10 to 10.00/10, and the final Flake8 report is
  empty.
