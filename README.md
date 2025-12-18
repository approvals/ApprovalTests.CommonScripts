# Approval Tests Common Scripts

![Build and Test](https://github.com/approvals/ApprovalTests.CommonScripts/actions/workflows/build-and-test.yml/badge.svg)

<!-- toc -->
## Contents

  * [Approve All](#approve-all)
    * [Example Output](#example-output)
  * [Remove Abandoned Files](#remove-abandoned-files)
    * [Example output](#example-output-1)
  * [See Also](#see-also)<!-- endToc -->

## Approve All

When you make a change that affects a large number of Approval Tests you can quickly approve the new results by running `.approval_tests_temp/approve_all.py`.

### Example Output

<!-- snippet: test_approve_all.test__one_case.approved.txt -->
<a id='snippet-test_approve_all.test__one_case.approved.txt'></a>
```txt
Mismatched file found.
Updating:
  - a.approved.txt

Approved 1 file.
```
<sup><a href='/test_approve_all.test__one_case.approved.txt#L1-L5' title='Snippet source file'>snippet source</a> | <a href='#snippet-test_approve_all.test__one_case.approved.txt' title='Start of snippet'>anchor</a></sup>
<!-- endSnippet -->

## Remove Abandoned Files

Sometimes when using Approval Tests you might end up with some stray `approved` files for tests that no longer exist.

You can quickly identify and eliminate these files by running `.approval_tests_temp/remove_abandoned_files.py`.
Running this will first list all files it believes have been abandoned and then give you the option to delete these files.

### Example output

<!-- snippet: test_remove_abandoned_files.test__reject.approved.txt -->
<a id='snippet-test_remove_abandoned_files.test__reject.approved.txt'></a>
```txt
Unused `.approved.` files found.

 - a.stray.approved.txt (in path/to/)
 - c.stray.approved.txt (in path/to2/)
Delete? [Y/n]
n
No files were deleted.
```
<sup><a href='/test_remove_abandoned_files.test__reject.approved.txt#L1-L7' title='Snippet source file'>snippet source</a> | <a href='#snippet-test_remove_abandoned_files.test__reject.approved.txt' title='Start of snippet'>anchor</a></sup>
<!-- endSnippet -->

## See Also

- [Agents](docs/agents.md) - AI agent instructions and script documentation
- [Map](docs/map.md) - Codebase structure overview
