# Agents

## About the Scripts

ApprovalTests (Java, Python, Go, Node) creates a `.approval_tests_temp/` directory when run,
and will download these scripts into that directory when needed.

### approve_all.py

Batch approves all mismatched approval test files by copying `.received` files to `.approved` files.

**Usage:** `.approval_tests_temp/approve_all.py`

**Behavior:**
- Displays count of mismatched files
- Copies `.received` to `.approved` for each mismatch
- Reports number of files approved

### remove_abandoned_files.py

Identifies and optionally deletes orphaned `.approved` files that no longer have corresponding tests.

**Usage:** `.approval_tests_temp/remove_abandoned_files.py`

**Behavior:**
- Lists all abandoned files found
- Prompts user for confirmation before deletion
- Deletes files only if user confirms
