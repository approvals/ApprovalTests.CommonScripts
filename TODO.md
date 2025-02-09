TODO:
- [ ] if curl is not installed, use wget
- [ ] write an ADR
- [x] record the UX design
- [ ] how do we publish?
- [ ] --dry-run / -n flag
- [ ] break in to unit tests / use loader

instructions given to user:
"""
To approve all failing tests, either:
- run the following
```
run ./.approvaltests_temp/ensure_uv_installed
uv run approvaltests_temp/approve_all.py
```
or
- run `python3 approvaltests_temp/approve_all.py`
"""

alternate UX:
`uv tool run approvaltests --approve--all`
or
`python -m approvaltests --approve-all`
