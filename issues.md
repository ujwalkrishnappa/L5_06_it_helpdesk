# Static Analysis Issue Documentation

The line numbers below refer to the original `helpdesk_system.py`. The
corresponding before-and-after reports are in `reports/before/` and
`reports/after/`.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command built from input (`Bandit B602`, High) | Security | 38 | The hostname was concatenated into a shell command, which could let crafted input execute an unintended command. | Validate the hostname and pass ping arguments as a list without a shell. The ping option now also matches Windows (`-n`) and Unix-like systems (`-c`). |
| Hard-coded admin password (`Bandit B105`, Low) | Security | 8 | A password literal in source code can be exposed through source control or file sharing. | Read `HELPDESK_ADMIN_PASSWORD` from the environment and compare it with `hmac.compare_digest`. The original example value remains only in the baseline Git commit/report for this exercise; do not use it as a real credential. |
| Bare exception and silent failure (`Bandit B110`, Pylint W0702, Flake8 E722) | Bug / Security | 22-24 | `except: pass` hid every kind of error. A note for a missing ticket disappeared without explanation. | Catch only `KeyError`, print a useful message, and return `False` when the ticket is missing. |
| `subprocess` heuristic warnings (`Bandit B404`, B603, B607) | Security | 2, 38 | Bandit flags subprocess use even when the shell is not involved. | Keep the needed ping feature with a fixed argument list and hostname validation. Use narrowly scoped `# nosec` codes for these reviewed, safe calls; the final report has no unsuppressed findings and records three suppressed checks. |
| Mutable default list (`Pylint W0102`) | Bug | 10 | The default `audit_trail=[]` was shared between calls, so one call could affect another. | Use `None` as the default and create a fresh list inside `raise_ticket`. |
| Urgency not constrained to 1-5 | Logic bug (not flagged by tools) | 12, 48 | Values such as `-7` or `99` could be stored as ticket priorities. | Validate the converted integer and raise `ValueError` for values outside the allowed range; display the error in `main`. |
| Unknown ticket and bad-password cases were silent | Logic bug (not flagged by tools) | 26-28 | Closing a nonexistent ticket or using a wrong password gave no feedback. | Return `True` only on success and print a clear message for each failure. |
| Global counter and lowercase constant (`Pylint W0603`, C0103) | Quality | 7, 11 | A function changed a global counter, and its name looked like a normal variable. | Replace it with the `TICKET_IDS` iterator and call `next()` to get each new id. |
| CamelCase name and dictionary iteration (`Pylint C0103`, C0206) | Style / Quality | 30-33 | The function did not follow Python's `snake_case` convention and only iterated over dictionary keys. | Rename it to `unresolved_high_priority` and iterate over `.items()` in a list comprehension. |
| Comparison with `None` (`Pylint C0121`, Flake8 E711) | Style / Quality | 33 | `== None` is less precise than checking the `None` singleton by identity. | Use `is None`. |
| File not managed by a context manager (`Pylint R1732`, W1514) | Reliability | 41-43 | The file might not be closed if writing failed, and the text encoding depended on the machine. | Use `with open(..., encoding="utf-8")` and `json.dump`. |
| Unused variable (`Pylint W0612`, Flake8 F841) | Quality | 47 | The result assigned to `t2` was never used. | Create the second ticket without assigning its id. |
| Old string formatting (`Pylint C0209`) | Style | 14 | Percent-formatting was unnecessary and harder to scan. | Use an f-string. |
| Missing docstrings (`Pylint C0114`, C0116) | Documentation | 1, all functions | The module and its functions did not explain their purpose. | Add a short module docstring and function docstrings. |
| PEP 8 layout problems (Flake8 E302, E305, E501) | Style | Multiple | Missing blank lines and overlong lines made the file harder to read. | Add the required top-level spacing and wrap long expressions. |
| Program ran when imported | Maintainability | 58 | Importing the module immediately started the interactive demo. | Call `main()` only under the `if __name__ == "__main__":` guard. |

## Measured Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.53 / 10 | 10.00 / 10 |
| Bandit | 1 High, 3 Low | 0 unsuppressed findings; 3 reviewed checks suppressed with `# nosec` |
| Flake8 | 15 findings | 0 findings |
