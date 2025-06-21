GIT-DIFF(1) | Git Manual | GIT-DIFF(1)  
---|---|---  
# NAME

git-diff - Show changes between commits, commit and working tree, etc

# SYNOPSIS

[code]

    *git diff* [<options>] [<commit>] [--] [<path>...]
    *git diff* [<options>] --cached [--merge-base] [<commit>] [--] [<path>...]
    *git diff* [<options>] [--merge-base] <commit> [<commit>...] <commit> [--] [<path>...]
    *git diff* [<options>] <commit>...<commit> [--] [<path>...]
    *git diff* [<options>] <blob> <blob>
    *git diff* [<options>] --no-index [--] <path> <path>
[/code]

# DESCRIPTION

Show changes between the working tree and the index or a tree, changes between
the index and a tree, changes between two trees, changes resulting from a
merge, changes between two blob objects, or changes between two files on disk.

*git diff* [<options>] [--] [<path>...]
This form is to view the changes you made relative to the index (staging area
for the next commit). In other words, the differences are what you *could*
tell Git to further add to the index but you still haven’t. You can stage
these changes by using __git-add__(1).

*git diff* [<options>] --no-index [--] <path> <path>
This form is to compare the given two paths on the filesystem. You can omit
the __\--no-index__ option when running the command in a working tree
controlled by Git and at least one of the paths points outside the working
tree, or when running the command outside a working tree controlled by Git.
This form implies __\--exit-code__.

*git diff* [<options>] --cached [--merge-base] [<commit>] [--] [<path>...]
This form is to view the changes you staged for the next commit relative to
the named <commit>. Typically you would want comparison with the latest
commit, so if you do not give <commit>, it defaults to HEAD. If HEAD does not
exist (e.g. unborn branches) and <commit> is not given, it shows all staged
changes. --staged is a synonym of --cached.

If --merge-base is given, instead of using <commit>, use the merge base of
<commit> and HEAD. __git diff --cached --merge-base A__ is equivalent to __git
diff --cached $(git merge-base A HEAD)__.

*git diff* [<options>] [--merge-base] <commit> [--] [<path>...]
This form is to view the changes you have in your working tree relative to the
named <commit>. You can use HEAD to compare it with the latest commit, or a
branch name to compare with the tip of a different branch.

If --merge-base is given, instead of using <commit>, use the merge base of
<commit> and HEAD. __git diff --merge-base A__ is equivalent to __git diff
$(git merge-base A HEAD)__.

*git diff* [<options>] [--merge-base] <commit> <commit> [--] [<path>...]
This is to view the changes between two arbitrary <commit>.

If --merge-base is given, use the merge base of the two commits for the
"before" side. __git diff --merge-base A B__ is equivalent to __git diff $(git
merge-base A B) B__.

*git diff* [<options>] <commit> <commit>... <commit> [--] [<path>...]
This form is to view the results of a merge commit. The first listed <commit>
must be the merge itself; the remaining two or more commits should be its
parents. Convenient ways to produce the desired set of revisions are to use
the suffixes __^@__ and __^!__. If A is a merge commit, then __git diff A
A^@__ , __git diff A^!__ and __git show A__ all give the same combined diff.

*git diff* [<options>] <commit>..<commit> [--] [<path>...]
This is synonymous to the earlier form (without the __..__) for viewing the
changes between two arbitrary <commit>. If <commit> on one side is omitted, it
will have the same effect as using HEAD instead.

*git diff* [<options>] <commit>...<commit> [--] [<path>...]
This form is to view the changes on the branch containing and up to the second
<commit>, starting at a common ancestor of both <commit>. __git diff A...B__
is equivalent to __git diff $(git merge-base A B) B__. You can omit any one of
<commit>, which has the same effect as using HEAD instead.

Just in case you are doing something exotic, it should be noted that all of
the <commit> in the above description, except in the __\--merge-base__ case
and in the last two forms that use __..__ notations, can be any <tree>.

For a more complete list of ways to spell <commit>, see "SPECIFYING REVISIONS"
section in __gitrevisions__(7). However, "diff" is about comparing two
*endpoints* , not ranges, and the range notations (__< commit>..<commit>__ and
__< commit>...<commit>__) do not mean a range as defined in the "SPECIFYING
RANGES" section in __gitrevisions__(7).

*git diff* [<options>] <blob> <blob>
This form is to view the differences between the raw contents of two blob
objects.

# OPTIONS

-p, -u, --patch
Generate patch (see section on generating patches). This is the default.

-s, --no-patch
Suppress diff output. Useful for commands like __git show__ that show the
patch by default, or to cancel the effect of __\--patch__.

-U<n>, --unified=<n>
Generate diffs with <n> lines of context instead of the usual three. Implies
__\--patch__.

\--output=<file>

Output to a specific file instead of stdout.

\--output-indicator-new=<char>, \--output-indicator-old=<char>, \--output-
indicator-context=<char>

Specify the character used to indicate new, old or context lines in the
generated patch. Normally they are *+* , *-* and ' ' respectively.

\--raw

Generate the diff in raw format.

\--patch-with-raw

Synonym for __-p --raw__.

\--indent-heuristic

Enable the heuristic that shifts diff hunk boundaries to make patches easier
to read. This is the default.

\--no-indent-heuristic

Disable the indent heuristic.

\--minimal

Spend extra time to make sure the smallest possible diff is produced.

\--patience

Generate a diff using the "patience diff" algorithm.

\--histogram

Generate a diff using the "histogram diff" algorithm.

\--anchored=<text>

Generate a diff using the "anchored diff" algorithm.

This option may be specified more than once.

If a line exists in both the source and destination, exists only once, and
starts with this text, this algorithm attempts to prevent it from appearing as
a deletion or addition in the output. It uses the "patience diff" algorithm
internally.

\--diff-algorithm={patience|minimal|histogram|myers}

Choose a diff algorithm. The variants are as follows:

__default__ , __myers__

The basic greedy diff algorithm. Currently, this is the default.

__minimal__

Spend extra time to make sure the smallest possible diff is produced.

__patience__

Use "patience diff" algorithm when generating patches.

__histogram__

This algorithm extends the patience algorithm to "support low-occurrence
common elements".

For instance, if you configured the __diff.algorithm__ variable to a non-
default value and want to use the default one, then you have to use __\--diff-
algorithm=default__ option.

\--stat[=<width>[,<name-width>[,<count>]]]

Generate a diffstat. By default, as much space as necessary will be used for
the filename part, and the rest for the graph part. Maximum width defaults to
terminal width, or 80 columns if not connected to a terminal, and can be
overridden by __< width>__. The width of the filename part can be limited by
giving another width __< name-width>__ after a comma. The width of the graph
part can be limited by using __\--stat-graph-width= <width>__ (affects all
commands generating a stat graph) or by setting __diff.statGraphWidth=
<width>__ (does not affect __git format-patch__). By giving a third parameter
__< count>__, you can limit the output to the first __< count>__ lines,
followed by __...__ if there are more.

These parameters can also be set individually with __\--stat-width= <width>__,
__\--stat-name-width= <name-width>__ and __\--stat-count= <count>__.

\--compact-summary

Output a condensed summary of extended header information such as file
creations or deletions ("new" or "gone", optionally "+l" if it’s a symlink)
and mode changes ("+x" or "-x" for adding or removing executable bit
respectively) in diffstat. The information is put between the filename part
and the graph part. Implies __\--stat__.

\--numstat

Similar to __\--stat__ , but shows number of added and deleted lines in
decimal notation and pathname without abbreviation, to make it more machine
friendly. For binary files, outputs two __-__ instead of saying __0 0__.

\--shortstat

Output only the last line of the __\--stat__ format containing total number of
modified files, as well as number of added and deleted lines.

-X[<param1,param2,...>], \--dirstat[=<param1,param2,...>]
Output the distribution of relative amount of changes for each sub-directory.
The behavior of __\--dirstat__ can be customized by passing it a comma
separated list of parameters. The defaults are controlled by the
__diff.dirstat__ configuration variable (see __git-config__(1)). The following
parameters are available:

__changes__

Compute the dirstat numbers by counting the lines that have been removed from
the source, or added to the destination. This ignores the amount of pure code
movements within a file. In other words, rearranging lines in a file is not
counted as much as other changes. This is the default behavior when no
parameter is given.

__lines__

Compute the dirstat numbers by doing the regular line-based diff analysis, and
summing the removed/added line counts. (For binary files, count 64-byte chunks
instead, since binary files have no natural concept of lines). This is a more
expensive __\--dirstat__ behavior than the __changes__ behavior, but it does
count rearranged lines within a file as much as other changes. The resulting
output is consistent with what you get from the other __\--*stat__ options.

__files__

Compute the dirstat numbers by counting the number of files changed. Each
changed file counts equally in the dirstat analysis. This is the
computationally cheapest __\--dirstat__ behavior, since it does not have to
look at the file contents at all.

__cumulative__

Count changes in a child directory for the parent directory as well. Note that
when using __cumulative__ , the sum of the percentages reported may exceed
100%. The default (non-cumulative) behavior can be specified with the
__noncumulative__ parameter.

<limit>

An integer parameter specifies a cut-off percent (3% by default). Directories
contributing less than this percentage of the changes are not shown in the
output.

Example: The following will count changed files, while ignoring directories
with less than 10% of the total amount of changed files, and accumulating
child directory counts in the parent directories:
__\--dirstat=files,10,cumulative__.

\--cumulative

Synonym for --dirstat=cumulative

\--dirstat-by-file[=<param1,param2>...]

Synonym for --dirstat=files,param1,param2...

\--summary

Output a condensed summary of extended header information such as creations,
renames and mode changes.

\--patch-with-stat

Synonym for __-p --stat__.

-z
When __\--raw__ , __\--numstat__ , __\--name-only__ or __\--name-status__ has
been given, do not munge pathnames and use NULs as output field terminators.

Without this option, pathnames with "unusual" characters are quoted as
explained for the configuration variable __core.quotePath__ (see __git-
config__(1)).

\--name-only

Show only names of changed files. The file names are often encoded in UTF-8.
For more information see the discussion about encoding in the __git-log__(1)
manual page.

\--name-status

Show only names and status of changed files. See the description of the
__\--diff-filter__ option on what the status letters mean. Just like
__\--name-only__ the file names are often encoded in UTF-8.

\--submodule[=<format>]

Specify how differences in submodules are shown. When specifying
__\--submodule=short__ the *short* format is used. This format just shows the
names of the commits at the beginning and end of the range. When
__\--submodule__ or __\--submodule=log__ is specified, the *log* format is
used. This format lists the commits in the range like __git-submodule__(1)
__summary__ does. When __\--submodule=diff__ is specified, the *diff* format
is used. This format shows an inline diff of the changes in the submodule
contents between the commit range. Defaults to __diff.submodule__ or the
*short* format if the config option is unset.

\--color[=<when>]

Show colored diff. __\--color__ (i.e. without *= <when>*) is the same as
__\--color=always__. *< when>* can be one of __always__ , __never__ , or
__auto__. It can be changed by the __color.ui__ and __color.diff__
configuration settings.

\--no-color

Turn off colored diff. This can be used to override configuration settings. It
is the same as __\--color=never__.

\--color-moved[=<mode>]

Moved lines of code are colored differently. It can be changed by the
__diff.colorMoved__ configuration setting. The <mode> defaults to *no* if the
option is not given and to *zebra* if the option with no mode is given. The
mode must be one of:

no

Moved lines are not highlighted.

default

Is a synonym for __zebra__. This may change to a more sensible mode in the
future.

plain

Any line that is added in one location and was removed in another location
will be colored with *color.diff.newMoved*. Similarly *color.diff.oldMoved*
will be used for removed lines that are added somewhere else in the diff. This
mode picks up any moved line, but it is not very useful in a review to
determine if a block of code was moved without permutation.

blocks

Blocks of moved text of at least 20 alphanumeric characters are detected
greedily. The detected blocks are painted using either the
*color.diff.{old,new}Moved* color. Adjacent blocks cannot be told apart.

zebra

Blocks of moved text are detected as in *blocks* mode. The blocks are painted
using either the *color.diff.{old,new}Moved* color or
*color.diff.{old,new}MovedAlternative*. The change between the two colors
indicates that a new block was detected.

dimmed-zebra

Similar to *zebra* , but additional dimming of uninteresting parts of moved
code is performed. The bordering lines of two adjacent blocks are considered
interesting, the rest is uninteresting. __dimmed_zebra__ is a deprecated
synonym.

\--no-color-moved

Turn off move detection. This can be used to override configuration settings.
It is the same as __\--color-moved=no__.

\--color-moved-ws=<modes>

This configures how whitespace is ignored when performing the move detection
for __\--color-moved__. It can be set by the __diff.colorMovedWS__
configuration setting. These modes can be given as a comma separated list:

no

Do not ignore whitespace when performing move detection.

ignore-space-at-eol

Ignore changes in whitespace at EOL.

ignore-space-change

Ignore changes in amount of whitespace. This ignores whitespace at line end,
and considers all other sequences of one or more whitespace characters to be
equivalent.

ignore-all-space

Ignore whitespace when comparing lines. This ignores differences even if one
line has whitespace where the other line has none.

allow-indentation-change

Initially ignore any whitespace in the move detection, then group the moved
code blocks only into a block if the change in whitespace is the same per
line. This is incompatible with the other modes.

\--no-color-moved-ws

Do not ignore whitespace when performing move detection. This can be used to
override configuration settings. It is the same as __\--color-moved-ws=no__.

\--word-diff[=<mode>]

Show a word diff, using the <mode> to delimit changed words. By default, words
are delimited by whitespace; see __\--word-diff-regex__ below. The <mode>
defaults to *plain* , and must be one of:

color

Highlight changed words using only colors. Implies __\--color__.

plain

Show words as __[-removed-]__ and __{+added+}__. Makes no attempts to escape
the delimiters if they appear in the input, so the output may be ambiguous.

porcelain

Use a special line-based format intended for script consumption.
Added/removed/unchanged runs are printed in the usual unified diff format,
starting with a __+__ /__-__ /` ` character at the beginning of the line and
extending to the end of the line. Newlines in the input are represented by a
tilde __~__ on a line of its own.

none

Disable word diff again.

Note that despite the name of the first mode, color is used to highlight the
changed parts in all modes if enabled.

\--word-diff-regex=<regex>

Use <regex> to decide what a word is, instead of considering runs of non-
whitespace to be a word. Also implies __\--word-diff__ unless it was already
enabled.

Every non-overlapping match of the <regex> is considered a word. Anything
between these matches is considered whitespace and ignored(!) for the purposes
of finding differences. You may want to append __|[^[:space:]]__ to your
regular expression to make sure that it matches all non-whitespace characters.
A match that contains a newline is silently truncated(!) at the newline.

For example, __\--word-diff-regex=.__ will treat each character as a word and,
correspondingly, show differences character by character.

The regex can also be set via a diff driver or configuration option, see
__gitattributes__(5) or __git-config__(1). Giving it explicitly overrides any
diff driver or configuration setting. Diff drivers override configuration
settings.

\--color-words[=<regex>]

Equivalent to __\--word-diff=color__ plus (if a regex was specified)
__\--word-diff-regex= <regex>__.

\--no-renames

Turn off rename detection, even when the configuration file gives the default
to do so.

\--[no-]rename-empty

Whether to use empty blobs as rename source.

\--check

Warn if changes introduce conflict markers or whitespace errors. What are
considered whitespace errors is controlled by __core.whitespace__
configuration. By default, trailing whitespaces (including lines that consist
solely of whitespaces) and a space character that is immediately followed by a
tab character inside the initial indent of the line are considered whitespace
errors. Exits with non-zero status if problems are found. Not compatible with
--exit-code.

\--ws-error-highlight=<kind>

Highlight whitespace errors in the __context__ , __old__ or __new__ lines of
the diff. Multiple values are separated by comma, __none__ resets previous
values, __default__ reset the list to __new__ and __all__ is a shorthand for
__old,new,context__. When this option is not given, and the configuration
variable __diff.wsErrorHighlight__ is not set, only whitespace errors in
__new__ lines are highlighted. The whitespace errors are colored with
__color.diff.whitespace__.

\--full-index

Instead of the first handful of characters, show the full pre- and post-image
blob object names on the "index" line when generating patch format output.

\--binary

In addition to __\--full-index__ , output a binary diff that can be applied
with __git-apply__. Implies __\--patch__.

\--abbrev[=<n>]

Instead of showing the full 40-byte hexadecimal object name in diff-raw format
output and diff-tree header lines, show the shortest prefix that is at least
*< n>* hexdigits long that uniquely refers the object. In diff-patch output
format, __\--full-index__ takes higher precedence, i.e. if __\--full-index__
is specified, full blob names will be shown regardless of __\--abbrev__. Non
default number of digits can be specified with __\--abbrev= <n>__.

-B[<n>][/<m>], \--break-rewrites[=[<n>][/<m>]]
Break complete rewrite changes into pairs of delete and create. This serves
two purposes:

It affects the way a change that amounts to a total rewrite of a file not as a
series of deletion and insertion mixed together with a very few lines that
happen to match textually as the context, but as a single deletion of
everything old followed by a single insertion of everything new, and the
number __m__ controls this aspect of the -B option (defaults to 60%).
__-B/70%__ specifies that less than 30% of the original should remain in the
result for Git to consider it a total rewrite (i.e. otherwise the resulting
patch will be a series of deletion and insertion mixed together with context
lines).

When used with -M, a totally-rewritten file is also considered as the source
of a rename (usually -M only considers a file that disappeared as the source
of a rename), and the number __n__ controls this aspect of the -B option
(defaults to 50%). __-B20%__ specifies that a change with addition and
deletion compared to 20% or more of the file’s size are eligible for being
picked up as a possible source of a rename to another file.

-M[<n>], --find-renames[=<n>]
Detect renames. If __n__ is specified, it is a threshold on the similarity
index (i.e. amount of addition/deletions compared to the file’s size). For
example, __-M90%__ means Git should consider a delete/add pair to be a rename
if more than 90% of the file hasn’t changed. Without a __%__ sign, the number
is to be read as a fraction, with a decimal point before it. I.e., __-M5__
becomes 0.5, and is thus the same as __-M50%__. Similarly, __-M05__ is the
same as __-M5%__. To limit detection to exact renames, use __-M100%__. The
default similarity index is 50%.

-C[<n>], --find-copies[=<n>]
Detect copies as well as renames. See also __\--find-copies-harder__. If __n__
is specified, it has the same meaning as for __-M <n>__.

\--find-copies-harder

For performance reasons, by default, __-C__ option finds copies only if the
original file of the copy was modified in the same changeset. This flag makes
the command inspect unmodified files as candidates for the source of copy.
This is a very expensive operation for large projects, so use it with caution.
Giving more than one __-C__ option has the same effect.

-D, --irreversible-delete
Omit the preimage for deletes, i.e. print only the header but not the diff
between the preimage and __/dev/null__. The resulting patch is not meant to be
applied with __patch__ or __git apply__ ; this is solely for people who want
to just concentrate on reviewing the text after the change. In addition, the
output obviously lacks enough information to apply such a patch in reverse,
even manually, hence the name of the option.

When used together with __-B__ , omit also the preimage in the deletion part
of a delete/create pair.

-l<num>
The __-M__ and __-C__ options involve some preliminary steps that can detect
subsets of renames/copies cheaply, followed by an exhaustive fallback portion
that compares all remaining unpaired destinations to all relevant sources.
(For renames, only remaining unpaired sources are relevant; for copies, all
original sources are relevant.) For N sources and destinations, this
exhaustive check is O(N^2). This option prevents the exhaustive portion of
rename/copy detection from running if the number of source/destination files
involved exceeds the specified number. Defaults to diff.renameLimit. Note that
a value of 0 is treated as unlimited.

\--diff-filter=[(A|C|D|M|R|T|U|X|B)...[*]]

Select only files that are Added (__A__), Copied (__C__), Deleted (__D__),
Modified (__M__), Renamed (__R__), have their type (i.e. regular file,
symlink, submodule, ...) changed (__T__), are Unmerged (__U__), are Unknown
(__X__), or have had their pairing Broken (__B__). Any combination of the
filter characters (including none) can be used. When __*__ (All-or-none) is
added to the combination, all paths are selected if there is any file that
matches other criteria in the comparison; if there is no file that matches
other criteria, nothing is selected.

Also, these upper-case letters can be downcased to exclude. E.g. __\--diff-
filter=ad__ excludes added and deleted paths.

Note that not all diffs can feature all types. For instance, copied and
renamed entries cannot appear if detection for those types is disabled.

-S<string>
Look for differences that change the number of occurrences of the specified
string (i.e. addition/deletion) in a file. Intended for the scripter’s use.

It is useful when you’re looking for an exact block of code (like a struct),
and want to know the history of that block since it first came into being: use
the feature iteratively to feed the interesting block in the preimage back
into __-S__ , and keep going until you get the very first version of the
block.

Binary files are searched as well.

-G<regex>
Look for differences whose patch text contains added/removed lines that match
<regex>.

To illustrate the difference between __-S <regex> \--pickaxe-regex__ and __-G
<regex>__, consider a commit with the following diff in the same file:

[code]

    +    return frotz(nitfol, two->ptr, 1, 0);
    ...
    -    hit = frotz(nitfol, mf2.ptr, 1, 0);
[/code]

While __git log -G "frotz\\(nitfol"__ will show this commit, __git log -S
"frotz\\(nitfol" \--pickaxe-regex__ will not (because the number of
occurrences of that string did not change).

Unless __\--text__ is supplied patches of binary files without a textconv
filter will be ignored.

See the *pickaxe* entry in __gitdiffcore__(7) for more information.

\--find-object=<object-id>

Look for differences that change the number of occurrences of the specified
object. Similar to __-S__ , just the argument is different in that it doesn’t
search for a specific string but for a specific object id.

The object can be a blob or a submodule commit. It implies the __-t__ option
in __git-log__ to also find trees.

\--pickaxe-all

When __-S__ or __-G__ finds a change, show all the changes in that changeset,
not just the files that contain the change in <string>.

\--pickaxe-regex

Treat the <string> given to __-S__ as an extended POSIX regular expression to
match.

-O<orderfile>
Control the order in which files appear in the output. This overrides the
__diff.orderFile__ configuration variable (see __git-config__(1)). To cancel
__diff.orderFile__ , use __-O/dev/null__.

The output order is determined by the order of glob patterns in <orderfile>.
All files with pathnames that match the first pattern are output first, all
files with pathnames that match the second pattern (but not the first) are
output next, and so on. All files with pathnames that do not match any pattern
are output last, as if there was an implicit match-all pattern at the end of
the file. If multiple pathnames have the same rank (they match the same
pattern but no earlier patterns), their output order relative to each other is
the normal order.

<orderfile> is parsed as follows:

•Blank lines are ignored, so they can be used as separators for readability.

•Lines starting with a hash ("__#__ ") are ignored, so they can be used for
comments. Add a backslash ("__\__ ") to the beginning of the pattern if it
starts with a hash.

•Each other line contains a single pattern.

Patterns have the same syntax and semantics as patterns used for fnmatch(3)
without the FNM_PATHNAME flag, except a pathname also matches a pattern if
removing any number of the final pathname components matches the pattern. For
example, the pattern "__foo*bar__ " matches "__fooasdfbar__ " and
"__foo/bar/baz/asdf__ " but not "__foobarx__ ".

\--skip-to=<file>, --rotate-to=<file>

Discard the files before the named <file> from the output (i.e. *skip to*), or
move them to the end of the output (i.e. *rotate to*). These were invented
primarily for use of the __git difftool__ command, and may not be very useful
otherwise.

-R
Swap two inputs; that is, show differences from index or on-disk file to tree
contents.

\--relative[=<path>], --no-relative

When run from a subdirectory of the project, it can be told to exclude changes
outside the directory and show pathnames relative to it with this option. When
you are not in a subdirectory (e.g. in a bare repository), you can name which
subdirectory to make the output relative to by giving a <path> as an argument.
__\--no-relative__ can be used to countermand both __diff.relative__ config
option and previous __\--relative__.

-a, --text
Treat all files as text.

\--ignore-cr-at-eol

Ignore carriage-return at the end of line when doing a comparison.

\--ignore-space-at-eol

Ignore changes in whitespace at EOL.

-b, --ignore-space-change
Ignore changes in amount of whitespace. This ignores whitespace at line end,
and considers all other sequences of one or more whitespace characters to be
equivalent.

-w, --ignore-all-space
Ignore whitespace when comparing lines. This ignores differences even if one
line has whitespace where the other line has none.

\--ignore-blank-lines

Ignore changes whose lines are all blank.

-I<regex>, --ignore-matching-lines=<regex>
Ignore changes whose all lines match <regex>. This option may be specified
more than once.

\--inter-hunk-context=<lines>

Show the context between diff hunks, up to the specified number of lines,
thereby fusing hunks that are close to each other. Defaults to
__diff.interHunkContext__ or 0 if the config option is unset.

-W, --function-context
Show whole function as context lines for each change. The function names are
determined in the same way as __git diff__ works out patch hunk headers (see
*Defining a custom hunk-header* in __gitattributes__(5)).

\--exit-code

Make the program exit with codes similar to diff(1). That is, it exits with 1
if there were differences and 0 means no differences.

\--quiet

Disable all output of the program. Implies __\--exit-code__.

\--ext-diff

Allow an external diff helper to be executed. If you set an external diff
driver with __gitattributes__(5), you need to use this option with __git-
log__(1) and friends.

\--no-ext-diff

Disallow external diff drivers.

\--textconv, --no-textconv

Allow (or disallow) external text conversion filters to be run when comparing
binary files. See __gitattributes__(5) for details. Because textconv filters
are typically a one-way conversion, the resulting diff is suitable for human
consumption, but cannot be applied. For this reason, textconv filters are
enabled by default only for __git-diff__(1) and __git-log__(1), but not for
__git-format-patch__(1) or diff plumbing commands.

\--ignore-submodules[=<when>]

Ignore changes to submodules in the diff generation. <when> can be either
"none", "untracked", "dirty" or "all", which is the default. Using "none" will
consider the submodule modified when it either contains untracked or modified
files or its HEAD differs from the commit recorded in the superproject and can
be used to override any settings of the *ignore* option in __git-config__(1)
or __gitmodules__(5). When "untracked" is used submodules are not considered
dirty when they only contain untracked content (but they are still scanned for
modified content). Using "dirty" ignores all changes to the work tree of
submodules, only changes to the commits stored in the superproject are shown
(this was the behavior until 1.7.0). Using "all" hides all changes to
submodules.

\--src-prefix=<prefix>

Show the given source prefix instead of "a/".

\--dst-prefix=<prefix>

Show the given destination prefix instead of "b/".

\--no-prefix

Do not show any source or destination prefix.

\--line-prefix=<prefix>

Prepend an additional prefix to every line of output.

\--ita-invisible-in-index

By default entries added by "git add -N" appear as an existing empty file in
"git diff" and a new file in "git diff --cached". This option makes the entry
appear as a new file in "git diff" and non-existent in "git diff --cached".
This option could be reverted with __\--ita-visible-in-index__. Both options
are experimental and could be removed in future.

For more detailed explanation on these common options, see also
__gitdiffcore__(7).

-1 --base, -2 --ours, -3 --theirs
Compare the working tree with the "base" version (stage #1), "our branch"
(stage #2) or "their branch" (stage #3). The index contains these stages only
for unmerged entries i.e. while resolving conflicts. See __git-read-tree__(1)
section "3-Way Merge" for detailed information.

-0
Omit diff output for unmerged entries and just show "Unmerged". Can be used
only when comparing the working tree with the index.

<path>...

The <paths> parameters, when given, are used to limit the diff to the named
paths (you can give directory names and get diff for all files under them).

# RAW OUTPUT FORMAT

The raw output format from "git-diff-index", "git-diff-tree", "git-diff-files"
and "git diff \--raw" are very similar.

These commands all compare two sets of things; what is compared differs:

git-diff-index <tree-ish>

compares the <tree-ish> and the files on the filesystem.

git-diff-index --cached <tree-ish>

compares the <tree-ish> and the index.

git-diff-tree [-r] <tree-ish-1> <tree-ish-2> [<pattern>...]

compares the trees named by the two arguments.

git-diff-files [<pattern>...]

compares the index and the files on the filesystem.

The "git-diff-tree" command begins its output by printing the hash of what is
being compared. After that, all the commands print one output line per changed
file.

An output line is formatted this way:

[code]

    in-place edit  :100644 100644 bcd1234 0123456 M file0
    copy-edit      :100644 100644 abcd123 1234567 C68 file1 file2
    rename-edit    :100644 100644 abcd123 1234567 R86 file1 file3
    create         :000000 100644 0000000 1234567 A file4
    delete         :100644 000000 1234567 0000000 D file5
    unmerged       :000000 000000 0000000 0000000 U file6
[/code]

That is, from the left to the right:

1.a colon.

2.mode for "src"; 000000 if creation or unmerged.

3.a space.

4.mode for "dst"; 000000 if deletion or unmerged.

5.a space.

6.sha1 for "src"; 0{40} if creation or unmerged.

7.a space.

8.sha1 for "dst"; 0{40} if deletion, unmerged or "work tree out of sync with
the index".

9.a space.

10.status, followed by optional "score" number.

11.a tab or a NUL when __-z__ option is used.

12.path for "src"

13.a tab or a NUL when __-z__ option is used; only exists for C or R.

14.path for "dst"; only exists for C or R.

15.an LF or a NUL when __-z__ option is used, to terminate the record.

Possible status letters are:

•A: addition of a file

•C: copy of a file into a new one

•D: deletion of a file

•M: modification of the contents or mode of a file

•R: renaming of a file

•T: change in the type of the file (regular file, symbolic link or submodule)

•U: file is unmerged (you must complete the merge before it can be committed)

•X: "unknown" change type (most probably a bug, please report it)

Status letters C and R are always followed by a score (denoting the percentage
of similarity between the source and target of the move or copy). Status
letter M may be followed by a score (denoting the percentage of dissimilarity)
for file rewrites.

The sha1 for "dst" is shown as all 0’s if a file on the filesystem is out of
sync with the index.

Example:

[code]

    :100644 100644 5be4a4a 0000000 M file.c
[/code]

Without the __-z__ option, pathnames with "unusual" characters are quoted as
explained for the configuration variable __core.quotePath__ (see __git-
config__(1)). Using __-z__ the filename is output verbatim and the line is
terminated by a NUL byte.

# DIFF FORMAT FOR MERGES

"git-diff-tree", "git-diff-files" and "git-diff --raw" can take __-c__ or
__\--cc__ option to generate diff output also for merge commits. The output
differs from the format described above in the following way:

1.there is a colon for each parent

2.there are more "src" modes and "src" sha1

3.status is concatenated status characters for each parent

4.no optional "score" number

5.tab-separated pathname(s) of the file

For __-c__ and __\--cc__ , only the destination or final path is shown even if
the file was renamed on any side of history. With __\--combined-all-paths__ ,
the name of the path in each parent is shown followed by the name of the path
in the merge commit.

Examples for __-c__ and __\--cc__ without __\--combined-all-paths__ :

[code]

    ::100644 100644 100644 fabadb8 cc95eb0 4866510 MM       desc.c
    ::100755 100755 100755 52b7a2d 6d1ac04 d2ac7d7 RM       bar.sh
    ::100644 100644 100644 e07d6c5 9042e82 ee91881 RR       phooey.c
[/code]

Examples when __\--combined-all-paths__ added to either __-c__ or __\--cc__ :

[code]

    ::100644 100644 100644 fabadb8 cc95eb0 4866510 MM       desc.c  desc.c  desc.c
    ::100755 100755 100755 52b7a2d 6d1ac04 d2ac7d7 RM       foo.sh  bar.sh  bar.sh
    ::100644 100644 100644 e07d6c5 9042e82 ee91881 RR       fooey.c fuey.c  phooey.c
[/code]

Note that *combined diff* lists only files which were modified from all
parents.

# GENERATING PATCH TEXT WITH -P

Running __git-diff__(1), __git-log__(1), __git-show__(1), __git-diff-
index__(1), __git-diff-tree__(1), or __git-diff-files__(1) with the __-p__
option produces patch text. You can customize the creation of patch text via
the __GIT_EXTERNAL_DIFF__ and the __GIT_DIFF_OPTS__ environment variables (see
__git__(1)), and the __diff__ attribute (see __gitattributes__(5)).

What the -p option produces is slightly different from the traditional diff
format:

1.It is preceded with a "git diff" header that looks like this:

[code]

    diff --git a/file1 b/file2
[/code]

The __a/__ and __b/__ filenames are the same unless rename/copy is involved.
Especially, even for a creation or a deletion, __/dev/null__ is *not* used in
place of the __a/__ or __b/__ filenames.

When rename/copy is involved, __file1__ and __file2__ show the name of the
source file of the rename/copy and the name of the file that rename/copy
produces, respectively.

2.It is followed by one or more extended header lines:

[code]

    old mode <mode>
    new mode <mode>
    deleted file mode <mode>
    new file mode <mode>
    copy from <path>
    copy to <path>
    rename from <path>
    rename to <path>
    similarity index <number>
    dissimilarity index <number>
    index <hash>..<hash> <mode>
[/code]

File modes are printed as 6-digit octal numbers including the file type and
file permission bits.

Path names in extended headers do not include the __a/__ and __b/__ prefixes.

The similarity index is the percentage of unchanged lines, and the
dissimilarity index is the percentage of changed lines. It is a rounded down
integer, followed by a percent sign. The similarity index value of 100% is
thus reserved for two equal files, while 100% dissimilarity means that no line
from the old file made it into the new one.

The index line includes the blob object names before and after the change. The
<mode> is included if the file mode does not change; otherwise, separate lines
indicate the old and the new mode.

3.Pathnames with "unusual" characters are quoted as explained for the
configuration variable __core.quotePath__ (see __git-config__(1)).

4.All the __file1__ files in the output refer to files before the commit, and
all the __file2__ files refer to files after the commit. It is incorrect to
apply each change to each file sequentially. For example, this patch will swap
a and b:

[code]

    diff --git a/a b/b
    rename from a
    rename to b
    diff --git a/b b/a
    rename from b
    rename to a
[/code]

5.Hunk headers mention the name of the function to which the hunk applies. See
"Defining a custom hunk-header" in __gitattributes__(5) for details of how to
tailor to this to specific languages.

# COMBINED DIFF FORMAT

Any diff-generating command can take the __-c__ or __\--cc__ option to produce
a *combined diff* when showing a merge. This is the default format when
showing merges with __git-diff__(1) or __git-show__(1). Note also that you can
give suitable __\--diff-merges__ option to any of these commands to force
generation of diffs in specific format.

A "combined diff" format looks like this:

[code]

    diff --combined describe.c
    index fabadb8,cc95eb0..4866510
    --- a/describe.c
    +++ b/describe.c
    @@@ -98,20 -98,12 +98,20 @@@
      
    
            return (a_date > b_date) ? -1 : (a_date == b_date) ? 0 : 1;
      
    
      }
    - static void describe(char *arg)
      
    
     -static void describe(struct commit *cmit, int last_one)
    ++static void describe(char *arg, int last_one)
      
    
      {
      
    
     +      unsigned char sha1[20];
      
    
     +      struct commit *cmit;
      
    
            struct commit_list *list;
      
    
            static int initialized = 0;
      
    
            struct commit_name *n;
      
    
     +      if (get_sha1(arg, sha1) < 0)
      
    
     +              usage(describe_usage);
      
    
     +      cmit = lookup_commit_reference(sha1);
      
    
     +      if (!cmit)
      
    
     +              usage(describe_usage);
      
    
     +
      
    
            if (!initialized) {
      
    
                    initialized = 1;
      
    
                    for_each_ref(get_name);
[/code]

1.It is preceded with a "git diff" header, that looks like this (when the __-
c__ option is used):

[code]

    diff --combined file
[/code]

or like this (when the __\--cc__ option is used):

[code]

    diff --cc file
[/code]

2.It is followed by one or more extended header lines (this example shows a
merge with two parents):

[code]

    index <hash>,<hash>..<hash>
    mode <mode>,<mode>..<mode>
    new file mode <mode>
    deleted file mode <mode>,<mode>
[/code]

The __mode <mode>,<mode>..<mode>__ line appears only if at least one of the
<mode> is different from the rest. Extended headers with information about
detected contents movement (renames and copying detection) are designed to
work with diff of two <tree-ish> and are not used by combined diff format.

3.It is followed by two-line from-file/to-file header

[code]

    --- a/file
    +++ b/file
[/code]

Similar to two-line header for traditional *unified* diff format,
__/dev/null__ is used to signal created or deleted files.

However, if the --combined-all-paths option is provided, instead of a two-line
from-file/to-file you get a N+1 line from-file/to-file header, where N is the
number of parents in the merge commit

[code]

    --- a/file
    --- a/file
    --- a/file
    +++ b/file
[/code]

This extended format can be useful if rename or copy detection is active, to
allow you to see the original name of the file in different parents.

4.Chunk header format is modified to prevent people from accidentally feeding
it to __patch -p1__. Combined diff format was created for review of merge
commit changes, and was not meant to be applied. The change is similar to the
change in the extended *index* header:

[code]

    @@@ <from-file-range> <from-file-range> <to-file-range> @@@
[/code]

There are (number of parents + 1) __@__ characters in the chunk header for
combined diff format.

Unlike the traditional *unified* diff format, which shows two files A and B
with a single column that has __-__ (minus — appears in A but removed in B),
__+__ (plus — missing in A but added to B), or __" "__ (space — unchanged)
prefix, this format compares two or more files file1, file2,... with one file
X, and shows how X differs from each of fileN. One column for each of fileN is
prepended to the output line to note how X’s line is different from it.

A __-__ character in the column N means that the line appears in fileN but it
does not appear in the result. A __+__ character in the column N means that
the line appears in the result, and fileN does not have that line (in other
words, the line was added, from the point of view of that parent).

In the above example output, the function signature was changed from both
files (hence two __-__ removals from both file1 and file2, plus __++__ to mean
one line that was added does not appear in either file1 or file2). Also eight
other lines are the same from file1 but do not appear in file2 (hence prefixed
with __+__).

When shown by __git diff-tree -c__ , it compares the parents of a merge commit
with the merge result (i.e. file1..fileN are the parents). When shown by __git
diff-files -c__ , it compares the two unresolved merge parents with the
working tree file (i.e. file1 is stage 2 aka "our version", file2 is stage 3
aka "their version").

# OTHER DIFF FORMATS

The __\--summary__ option describes newly added, deleted, renamed and copied
files. The __\--stat__ option adds diffstat(1) graph to the output. These
options can be combined with other options, such as __-p__ , and are meant for
human consumption.

When showing a change that involves a rename or a copy, __\--stat__ output
formats the pathnames compactly by combining common prefix and suffix of the
pathnames. For example, a change that moves __arch/i386/Makefile__ to
__arch/x86/Makefile__ while modifying 4 lines will be shown like this:

[code]

    arch/{i386 => x86}/Makefile    |   4 +--
[/code]

The __\--numstat__ option gives the diffstat(1) information but is designed
for easier machine consumption. An entry in __\--numstat__ output looks like
this:

[code]

    1       2       README
    3       1       arch/{i386 => x86}/Makefile
[/code]

That is, from left to right:

1.the number of added lines;

2.a tab;

3.the number of deleted lines;

4.a tab;

5.pathname (possibly with rename/copy information);

6.a newline.

When __-z__ output option is in effect, the output is formatted this way:

[code]

    1       2       README NUL
    3       1       NUL arch/i386/Makefile NUL arch/x86/Makefile NUL
[/code]

That is:

1.the number of added lines;

2.a tab;

3.the number of deleted lines;

4.a tab;

5.a NUL (only exists if renamed/copied);

6.pathname in preimage;

7.a NUL (only exists if renamed/copied);

8.pathname in postimage (only exists if renamed/copied);

9.a NUL.

The extra __NUL__ before the preimage path in renamed case is to allow scripts
that read the output to tell if the current record being read is a single-path
record or a rename/copy record without reading ahead. After reading added and
deleted lines, reading up to __NUL__ would yield the pathname, but if that is
__NUL__ , the record will show two paths.

# EXAMPLES

Various ways to check your working tree

[code]

    $ git diff            __(1)__
    $ git diff --cached   __(2)__
    $ git diff HEAD       __(3)__
[/code]

__1.__ Changes in the working tree not yet staged for the next commit.  
__2.__ Changes between the index and your last commit; what you would be
committing if you run __git commit__ without __-a__ option.  
__3.__ Changes in the working tree since your last commit; what you would be
committing if you run __git commit -a__  

Comparing with arbitrary commits

[code]

    $ git diff test            __(1)__
    $ git diff HEAD -- ./test  __(2)__
    $ git diff HEAD^ HEAD      __(3)__
[/code]

__1.__ Instead of using the tip of the current branch, compare with the tip of
"test" branch.  
__2.__ Instead of comparing with the tip of "test" branch, compare with the
tip of the current branch, but limit the comparison to the file "test".  
__3.__ Compare the version before the last commit and the last commit.  

Comparing branches

[code]

    $ git diff topic master    __(1)__
    $ git diff topic..master   __(2)__
    $ git diff topic...master  __(3)__
[/code]

__1.__ Changes between the tips of the topic and the master branches.  
__2.__ Same as above.  
__3.__ Changes that occurred on the master branch since when the topic branch
was started off it.  

Limiting the diff output

[code]

    $ git diff --diff-filter=MRC            __(1)__
    $ git diff --name-status                __(2)__
    $ git diff arch/i386 include/asm-i386   __(3)__
[/code]

__1.__ Show only modification, rename, and copy, but not addition or deletion.  
__2.__ Show only names and the nature of change, but not actual diff output.  
__3.__ Limit diff output to named subtrees.  

Munging the diff output

[code]

    $ git diff --find-copies-harder -B -C  __(1)__
    $ git diff -R                          __(2)__
[/code]

__1.__ Spend extra cycles to find renames, copies and complete rewrites (very
expensive).  
__2.__ Output diff in reverse.  

# CONFIGURATION

Everything below this line in this section is selectively included from the
__git-config__(1) documentation. The content is the same as what’s found
there:

diff.autoRefreshIndex

When using *git diff* to compare with work tree files, do not consider stat-
only change as changed. Instead, silently run __git update-index --refresh__
to update the cached stat information for paths whose contents in the work
tree match the contents in the index. This option defaults to true. Note that
this affects only *git diff* Porcelain, and not lower level *diff* commands
such as *git diff-files*.

diff.dirstat

A comma separated list of __\--dirstat__ parameters specifying the default
behavior of the __\--dirstat__ option to __git-diff__(1) and friends. The
defaults can be overridden on the command line (using __\--dirstat=
<param1,param2,...>__). The fallback defaults (when not changed by
__diff.dirstat__) are __changes,noncumulative,3__. The following parameters
are available:

__changes__

Compute the dirstat numbers by counting the lines that have been removed from
the source, or added to the destination. This ignores the amount of pure code
movements within a file. In other words, rearranging lines in a file is not
counted as much as other changes. This is the default behavior when no
parameter is given.

__lines__

Compute the dirstat numbers by doing the regular line-based diff analysis, and
summing the removed/added line counts. (For binary files, count 64-byte chunks
instead, since binary files have no natural concept of lines). This is a more
expensive __\--dirstat__ behavior than the __changes__ behavior, but it does
count rearranged lines within a file as much as other changes. The resulting
output is consistent with what you get from the other __\--*stat__ options.

__files__

Compute the dirstat numbers by counting the number of files changed. Each
changed file counts equally in the dirstat analysis. This is the
computationally cheapest __\--dirstat__ behavior, since it does not have to
look at the file contents at all.

__cumulative__

Count changes in a child directory for the parent directory as well. Note that
when using __cumulative__ , the sum of the percentages reported may exceed
100%. The default (non-cumulative) behavior can be specified with the
__noncumulative__ parameter.

<limit>

An integer parameter specifies a cut-off percent (3% by default). Directories
contributing less than this percentage of the changes are not shown in the
output.

Example: The following will count changed files, while ignoring directories
with less than 10% of the total amount of changed files, and accumulating
child directory counts in the parent directories: __files,10,cumulative__.

diff.statGraphWidth

Limit the width of the graph part in --stat output. If set, applies to all
commands generating --stat output except format-patch.

diff.context

Generate diffs with <n> lines of context instead of the default of 3. This
value is overridden by the -U option.

diff.interHunkContext

Show the context between diff hunks, up to the specified number of lines,
thereby fusing the hunks that are close to each other. This value serves as
the default for the __\--inter-hunk-context__ command line option.

diff.external

If this config variable is set, diff generation is not performed using the
internal diff machinery, but using the given command. Can be overridden with
the ‘GIT_EXTERNAL_DIFF’ environment variable. The command is called with
parameters as described under "git Diffs" in __git__(1). Note: if you want to
use an external diff program only on a subset of your files, you might want to
use __gitattributes__(5) instead.

diff.ignoreSubmodules

Sets the default value of --ignore-submodules. Note that this affects only
*git diff* Porcelain, and not lower level *diff* commands such as *git diff-
files*. *git checkout* and *git switch* also honor this setting when reporting
uncommitted changes. Setting it to *all* disables the submodule summary
normally shown by *git commit* and *git status* when
__status.submoduleSummary__ is set unless it is overridden by using the
--ignore-submodules command-line option. The *git submodule* commands are not
affected by this setting. By default this is set to untracked so that any
untracked submodules are ignored.

diff.mnemonicPrefix

If set, *git diff* uses a prefix pair that is different from the standard "a/"
and "b/" depending on what is being compared. When this configuration is in
effect, reverse diff output also swaps the order of the prefixes:

__git diff__

compares the (i)ndex and the (w)ork tree;

__git diff HEAD__

compares a (c)ommit and the (w)ork tree;

__git diff --cached__

compares a (c)ommit and the (i)ndex;

__git diff HEAD:file1 file2__

compares an (o)bject and a (w)ork tree entity;

__git diff --no-index a b__

compares two non-git things (1) and (2).

diff.noprefix

If set, *git diff* does not show any source or destination prefix.

diff.relative

If set to *true* , *git diff* does not show changes outside of the directory
and show pathnames relative to the current directory.

diff.orderFile

File indicating how to order files within a diff. See the *-O* option to
__git-diff__(1) for details. If __diff.orderFile__ is a relative pathname, it
is treated as relative to the top of the working tree.

diff.renameLimit

The number of files to consider in the exhaustive portion of copy/rename
detection; equivalent to the *git diff* option __-l__. If not set, the default
value is currently 1000. This setting has no effect if rename detection is
turned off.

diff.renames

Whether and how Git detects renames. If set to "false", rename detection is
disabled. If set to "true", basic rename detection is enabled. If set to
"copies" or "copy", Git will detect copies, as well. Defaults to true. Note
that this affects only *git diff* Porcelain like __git-diff__(1) and __git-
log__(1), and not lower level commands such as __git-diff-files__(1).

diff.suppressBlankEmpty

A boolean to inhibit the standard behavior of printing a space before each
empty output line. Defaults to false.

diff.submodule

Specify the format in which differences in submodules are shown. The "short"
format just shows the names of the commits at the beginning and end of the
range. The "log" format lists the commits in the range like __git-
submodule__(1) __summary__ does. The "diff" format shows an inline diff of the
changed contents of the submodule. Defaults to "short".

diff.wordRegex

A POSIX Extended Regular Expression used to determine what is a "word" when
performing word-by-word difference calculations. Character sequences that
match the regular expression are "words", all other characters are
__ignorable__ whitespace.

diff.<driver>.command

The custom diff driver command. See __gitattributes__(5) for details.

diff.<driver>.xfuncname

The regular expression that the diff driver should use to recognize the hunk
header. A built-in pattern may also be used. See __gitattributes__(5) for
details.

diff.<driver>.binary

Set this option to true to make the diff driver treat files as binary. See
__gitattributes__(5) for details.

diff.<driver>.textconv

The command that the diff driver should call to generate the text-converted
version of a file. The result of the conversion is used to generate a human-
readable diff. See __gitattributes__(5) for details.

diff.<driver>.wordRegex

The regular expression that the diff driver should use to split words in a
line. See __gitattributes__(5) for details.

diff.<driver>.cachetextconv

Set this option to true to make the diff driver cache the text conversion
outputs. See __gitattributes__(5) for details.

__araxis__

Use Araxis Merge (requires a graphical session)

__bc__

Use Beyond Compare (requires a graphical session)

__bc3__

Use Beyond Compare (requires a graphical session)

__bc4__

Use Beyond Compare (requires a graphical session)

__codecompare__

Use Code Compare (requires a graphical session)

__deltawalker__

Use DeltaWalker (requires a graphical session)

__diffmerge__

Use DiffMerge (requires a graphical session)

__diffuse__

Use Diffuse (requires a graphical session)

__ecmerge__

Use ECMerge (requires a graphical session)

__emerge__

Use Emacs' Emerge

__examdiff__

Use ExamDiff Pro (requires a graphical session)

__guiffy__

Use Guiffy’s Diff Tool (requires a graphical session)

__gvimdiff__

Use gVim (requires a graphical session)

__kdiff3__

Use KDiff3 (requires a graphical session)

__kompare__

Use Kompare (requires a graphical session)

__meld__

Use Meld (requires a graphical session)

__nvimdiff__

Use Neovim

__opendiff__

Use FileMerge (requires a graphical session)

__p4merge__

Use HelixCore P4Merge (requires a graphical session)

__smerge__

Use Sublime Merge (requires a graphical session)

__tkdiff__

Use TkDiff (requires a graphical session)

__vimdiff__

Use Vim

__winmerge__

Use WinMerge (requires a graphical session)

__xxdiff__

Use xxdiff (requires a graphical session)

diff.indentHeuristic

Set this option to __false__ to disable the default heuristics that shift diff
hunk boundaries to make patches easier to read.

diff.algorithm

Choose a diff algorithm. The variants are as follows:

__default__ , __myers__

The basic greedy diff algorithm. Currently, this is the default.

__minimal__

Spend extra time to make sure the smallest possible diff is produced.

__patience__

Use "patience diff" algorithm when generating patches.

__histogram__

This algorithm extends the patience algorithm to "support low-occurrence
common elements".

diff.wsErrorHighlight

Highlight whitespace errors in the __context__ , __old__ or __new__ lines of
the diff. Multiple values are separated by comma, __none__ resets previous
values, __default__ reset the list to __new__ and __all__ is a shorthand for
__old,new,context__. The whitespace errors are colored with
__color.diff.whitespace__. The command line option __\--ws-error-highlight=
<kind>__ overrides this setting.

diff.colorMoved

If set to either a valid __< mode>__ or a true value, moved lines in a diff
are colored differently, for details of valid modes see *\--color-moved* in
__git-diff__(1). If simply set to true the default color mode will be used.
When set to false, moved lines are not colored.

diff.colorMovedWS

When moved lines are colored using e.g. the __diff.colorMoved__ setting, this
option controls the __< mode>__ how spaces are treated for details of valid
modes see *\--color-moved-ws* in __git-diff__(1).

# SEE ALSO

diff(1), __git-difftool__(1), __git-log__(1), __gitdiffcore__(7), __git-
format-patch__(1), __git-apply__(1), __git-show__(1)

# GIT

Part of the __git__(1) suite

12/12/2022 | Git 2.39.0  
---|---

