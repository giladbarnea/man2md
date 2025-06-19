# man2md

This is a Python tool that converts raw man pages to markdown, faithful to the original formatting, content hierarchy and structures.

## Tests
The tests/ dir contains three files:
1. zshexpn-raw.txt: the raw man page for zshexpn. The output of `cat /usr/share/man/man1/zshexpn.1` as-is. This will be the input to `man2md`.
2. zshexpn.txt: The parsed man page for zshexpn. The output of `man zshexpn | col -b`. It is not Markdown, but unlike the raw man page source, it is human-readable. This file's only purpose is for you to read and get an intuition of the man page and its structure; it is not the input nor the output of `man2md`.
3. zshexpn-tree.txt: The tree structure of the man page. The output of `mandoc -T tree /usr/share/man/man1/zshexpn.1`. It has a rather peculiar syntax, but it does contain the structure information of the raw man page. In other words, zshexpn-tree.txt describes zshexpn-raw.txt well (not zshexpn.txt). This file can be parsed by `man2md` to get the structure information of the man page.

# Task
Your task is to implement the `man2md` tool autonomously.
1. Read the tests/*.txt file to get a sense of what you have to work with.
2. Manually (hard-code) write a tests/zshexpn.md, based on zshexpn.txt. This will be your source of truth. This file is the output of `man2md` on the input file tests/zshexpn-raw.txt.
3. Implement the tool in @man2md.py. It takes a raw man page path as input (like tests/zshexpn-raw.txt), converts it to markdown, and prints the result to stdout.

# Rules
1. You must work in TDD. You must work in a think-fix-test cycle.
2. Therefore, create the test your need first.
3. Work iteratively.
4. Complimentary to point 3, work on small chunks of the problem; literally, work on the first H1 section first; one you get it right, move on to the next H1 section, and work only on its first paragraph or first few paragraphs; etc. This is to avoid trying to solve the whole problem at once and comparing the result to the entire source of truth.

# Dev Cycle
1. This is a Mac.
2. You are using Python 3.12.
3. The package manager is `uv`.
4. Run Python with `uv run python [python arguments and options...]`.
5. Run tests with `uv run pytest [pytest arguments and options...]`.
6. Try to avoid installing any packages or tools, but if you have to, do it with `uv add ...`.
7. Never use any other means to install packages or tools: not pip, not brew, not npm; only `uv add ...`.
8. Use the terminal's coreutils as you need them. cat, grep, sed, awk, redirect output/input to /tmp, etc.