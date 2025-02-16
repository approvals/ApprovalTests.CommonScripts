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
