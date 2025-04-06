TODO:

- [ ] --dry-run / -n flag
- [ ] make approve all self runnable
- [ ] implement: find abandond files


instructions given to user:
"""
To approve all failing tests, either:
- install uv: https://docs.astral.sh/uv/getting-started/installation/ then run `uv run .approvaltests_temp/approve_all.py`
or
- run `python3 .approvaltests_temp/approve_all.py`
"""

alternate UX:
`uv tool run approvaltests --approve--all`
or
`python -m approvaltests --approve-all`
or
`approvaltests --approve-all`
