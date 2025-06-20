# man2md

This is a Python tool that converts raw man pages to markdown, faithful to the original formatting, content hierarchy and structures.

## Tests
The tests/ dir contains two test suites:

### zshexpn test suite (tests/zshexpn/)
1. zshexpn-raw.txt: the raw man page for zshexpn. The output of `cat /usr/share/man/man1/zshexpn.1` as-is. This will be the input to `man2md`.
2. zshexpn.txt: The parsed man page for zshexpn. The output of `man zshexpn | col -b`. It is not Markdown, but unlike the raw man page source, it is human-readable. This file's only purpose is for you to read and get an intuition of the man page and its structure; it is not the input nor the output of `man2md`.
3. zshexpn-tree.txt: The tree structure of the man page. The output of `mandoc -T tree /usr/share/man/man1/zshexpn.1`. It has a rather peculiar syntax, but it does contain the structure information of the raw man page. In other words, zshexpn-tree.txt describes zshexpn-raw.txt well (not zshexpn.txt). This file can be parsed by `man2md` to get the structure information of the man page.

### fsck_hfs test suite (tests/fsck_hfs/)
1. fsck_hfs_raw.txt: the raw man page for fsck_hfs. The output of `cat /usr/share/man/man8/fsck_hfs.8` as-is. This will be the input to `man2md`.
2. fsck_hfs.txt: The parsed man page for fsck_hfs. The output of `man fsck_hfs | col -b`. It is not Markdown, but unlike the raw man page source, it is human-readable. This file's only purpose is for you to read and get an intuition of the man page and its structure; it is not the input nor the output of `man2md`.
3. fsck_hfs_tree.txt: The tree structure of the man page. The output of `mandoc -T tree /usr/share/man/man8/fsck_hfs.8`. It has a rather peculiar syntax, but it does contain the structure information of the raw man page. In other words, fsck_hfs_tree.txt describes fsck_hfs_raw.txt well (not fsck_hfs.txt). This file can be parsed by `man2md` to get the structure information of the man page.

# Task
Your task is to implement the `man2md` tool autonomously.

## Completed (zshexpn test suite)
- [x] Read the tests/zshexpn/*.txt files to get a sense of what you have to work with.
- [x] Manually (hard-code) write a tests/zshexpn/zshexpn.md, based on zshexpn.txt. This will be your source of truth. This file is the output of `man2md` on the input file tests/zshexpn/zshexpn-raw.txt.
- [x] Implement the tool in @man2md.py. It takes a raw man page path as input (like tests/zshexpn/zshexpn-raw.txt), converts it to markdown, and prints the result to stdout.

## Current task (fsck_hfs test suite)
- [x] Read the tests/fsck_hfs/*.txt files to get a sense of what you have to work with.
- [x] Manually (hard-code) write a tests/fsck_hfs/fsck_hfs.md, based on fsck_hfs.txt. This will be your source of truth. This file is the output of `man2md` on the input file tests/fsck_hfs/fsck_hfs_raw.txt. ATTENTION: This file must be consistent with tests/zshexpn/zshexpn.md. By consistent, I mean that the conversion of fsck_hfs_raw.txt to fsck_hfs.md must be consistent with the conversion of zshexpn-raw.txt to zshexpn.md. This is crucial, because otherwise, the project will end up with two "types" of source of truth, which will make it impossible to test the tool.
- [x] Only after you are confident that the conversions are consistent, test the existing tool with fsck_hfs and fix any issues that arise.

# Rules
1. You must work in TDD. You must work in a think-fix-test cycle.
2. The test file is in tests/test_man2md.py.
3. Work iteratively.
4. Complimentary to point 3, always work on small chunks of the problem; literally, work on the first H1 section first; once you get it right, move on to the next H1 section, and work only on its first paragraph or first few paragraphs; etc. This is to avoid trying to solve the whole problem at once and comparing the result to the entire source of truth.

# Dev Cycle
1. This is a Mac.
2. You are using Python 3.12.
3. The package manager is `uv`.
4. Run Python with `uv run python [python arguments and options...]`.
5. Run tests with `uv run pytest [pytest arguments and options...]`.
6. Try to avoid installing any packages or tools, but if you have to, do it with `uv add ...`.
7. Never use any other means to install packages or tools: not pip, not brew, not npm; only `uv add ...`.
8. Use the terminal's coreutils as you need them. cat, grep, sed, awk, redirect output/input to /tmp, etc.