# Approval Tests Common Scripts

![Build and Test](https://github.com/approvals/ApprovalTests.CommonScripts/actions/workflows/build-and-test.yml/badge.svg)

toc 

## Approve All

When you make a change that affects a large number of Approval Tests you can quickly approve the new results by running `.approval_tests_temp/approve_all.py`.

### Example Output

snippet: test_approve_all.test__one_case.approved.txt

## Remove Abandoned Files

Sometimes when using Approval Tests you might end up with some stray `approved` files for tests that no longer exist.

You can quickly identify and eliminate these files by running `.approval_tests_temp/remove_abandoned_files.py`.
Running this will first list all files it believes have been abandoned and then give you the option to delete these files.

### Example output

snippet: test_remove_abandoned_files.test__reject.approved.txt
