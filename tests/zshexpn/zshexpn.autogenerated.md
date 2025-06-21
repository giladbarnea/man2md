ZSHEXPN(1) | General Commands Manual | ZSHEXPN(1)  
---|---|---  
# NAME

zshexpn - zsh expansion and substitution

# DESCRIPTION

The following types of expansions are performed in the indicated order in five
steps:

*History Expansion*
    This is performed only in interactive shells.
*Alias Expansion*
    Aliases are expanded immediately before the command line is parsed as explained under Aliasing in *zshmisc*(1).
*Process Substitution*
    
*Parameter Expansion*
    
*Command Substitution*
    
*Arithmetic Expansion*
    
*Brace Expansion*
    These five are performed in left-to-right fashion. On each argument, any of the five steps that are needed are performed one after the other. Hence, for example, all the parts of parameter expansion are completed before command substitution is started. After these expansions, all unquoted occurrences of the characters `__\__ ',`__'__ ' and `__"__ ' are removed.
*Filename Expansion*
    If the __SH_FILE_EXPANSION__ option is set, the order of expansion is modified for compatibility with __sh__ and __ksh__. In that case *filename expansion* is performed immediately after *alias expansion* , preceding the set of five expansions mentioned above.
*Filename Generation*
    This expansion, commonly referred to as __globbing__ , is always done last.
The following sections explain the types of expansion in detail.

# HISTORY EXPANSION

History expansion allows you to use words from previous command lines in the
command line you are typing. This simplifies spelling corrections and the
repetition of complicated commands or arguments.

Immediately before execution, each command is saved in the history list, the
size of which is controlled by the __HISTSIZE__ parameter. The one most recent
command is always retained in any case. Each saved command in the history list
is called a history *event* and is assigned a number, beginning with 1 (one)
when the shell starts up. The history number that you may see in your prompt
(see EXPANSION OF PROMPT SEQUENCES in *zshmisc*(1)) is the number that is to
be assigned to the *next* command.

## Overview

A history expansion begins with the first character of the __histchars__
parameter, which is `__!__ ' by default, and may occur anywhere on the command
line, including inside double quotes (but not inside single quotes __'...'__
or C-style quotes __$'...'__ nor when escaped with a backslash).

The first character is followed by an optional event designator (see the
section `Event Designators') and then an optional word designator (the section
`Word Designators'); if neither of these designators is present, no history
expansion occurs.

Input lines containing history expansions are echoed after being expanded, but
before any other expansions take place and before the command is executed. It
is this expanded form that is recorded as the history event for later
references.

History expansions do not nest.

By default, a history reference with no event designator refers to the same
event as any preceding history reference on that command line; if it is the
only history reference in a command, it refers to the previous command.
However, if the option __CSH_JUNKIE_HISTORY__ is set, then every history
reference with no event specification *always* refers to the previous command.

For example, `__!__ ' is the event designator for the previous command, so
`__!!:1__ ' always refers to the first word of the previous command, and
`__!!$__ ' always refers to the last word of the previous command. With
__CSH_JUNKIE_HISTORY__ set, then `__!:1__ ' and `__!$__ ' function in the same
manner as `__!!:1__ ' and `__!!$__ ', respectively. Conversely, if
__CSH_JUNKIE_HISTORY__ is unset, then `__!:1__ ' and `__!$__ ' refer to the
first and last words, respectively, of the same event referenced by the
nearest other history reference preceding them on the current command line, or
to the previous command if there is no preceding reference.

The character sequence `__^__*foo*__^__*bar* ' (where `__^__ ' is actually the
second character of the __histchars__ parameter) repeats the last command,
replacing the string *foo* with *bar*. More precisely, the sequence
`__^__*foo*__^__*bar*__^__ ' is synonymous with
`__!!:s____^__*foo*__^__*bar*__^__ ', hence other modifiers (see the section
`Modifiers') may follow the final `__^__ '. In particular,
`__^__*foo*__^__*bar*__^:G__ ' performs a global substitution.

If the shell encounters the character sequence `__! "__' in the input, the
history mechanism is temporarily disabled until the current list (see
*zshmisc*(1)) is fully parsed. The `__! "__' is removed from the input, and
any subsequent `__!__ ' characters have no special significance.

A less convenient but more comprehensible form of command history support is
provided by the __fc__ builtin.

## Event Designators

An event designator is a reference to a command-line entry in the history
list. In the list below, remember that the initial __`!'__ in each item may be
changed to another character by setting the __histchars__ parameter.

__!__

    Start a history expansion, except when followed by a blank, newline, `__=__ ' or `__(__ '. If followed immediately by a word designator (see the section `Word Designators'), this forms a history reference with no event designator (see the section `Overview').
__!!__

    Refer to the previous command. By itself, this expansion repeats the previous command.
__!__*n*

    Refer to command-line *n*.
__!-__*n*

    Refer to the current command-line minus *n*.
__!__*str*

    Refer to the most recent command starting with *str*.
__!?__*str*[__?__]

    Refer to the most recent command containing *str*. The trailing `__?__ ' is necessary if this reference is to be followed by a modifier or followed by any text that is not to be considered part of *str*.
__!#__

    Refer to the current command line typed in so far. The line is treated as if it were complete up to and including the word before the one with the `__!#__ ' reference.
__!{__...__}__

    Insulate a history reference from adjacent characters (if necessary).
## Word Designators

A word designator indicates which word or words of a given command line are to
be included in a history reference. A `__:__ ' usually separates the event
specification from the word designator. It may be omitted only if the word
designator begins with a `__^__ ', `__$__ ', `__*__ ', `__-__ ' or `__%__ '.
Word designators include:

__0__

    The first input word (command).
*n*
    The *n* th argument.
__^__

    The first argument. That is, __1__.
__$__

    The last argument.
__%__

    The word matched by (the most recent) __?__*str* search.
*x*__-__*y*
    A range of words; *x* defaults to __0__.
__*__

    All the arguments, or a null value if there are none.
*x*__*__
    Abbreviates `*x*__-$__ '.
*x*__-__
    Like `*x*__*__ ' but omitting word __$__.
Note that a `__%__ ' word designator works only when used in one of `__!%__ ',
`__!:%__ ' or `__!?__*str*__?:%__ ', and only when used after a __!?__
expansion (possibly in an earlier command). Anything else results in an error,
although the error may not be the most obvious one.

## Modifiers

After the optional word designator, you can add a sequence of one or more of
the following modifiers, each preceded by a `__:__ '. These modifiers also
work on the result of *filename generation* and *parameter expansion* , except
where noted.

__a__

    Turn a file name into an absolute path: prepends the current directory, if necessary; remove `__.__ ' path segments; and remove `__..__ ' path segments and the segments that immediately precede them.
This transformation is agnostic about what is in the filesystem, i.e. is on
the logical, not the physical directory. It takes place in the same manner as
when changing directories when neither of the options __CHASE_DOTS__ or
__CHASE_LINKS__ is set. For example, `__/before/here/../after__ ' is always
transformed to `__/before/after__ ', regardless of whether `__/before/here__ '
exists or what kind of object (dir, file, symlink, etc.) it is.

__A__

    Turn a file name into an absolute path as the `__a__ ' modifier does, and *then* pass the result through the __realpath(3)__ library function to resolve symbolic links.
Note: on systems that do not have a __realpath(3)__ library function, symbolic
links are not resolved, so on those systems `__a__ ' and `__A__ ' are
equivalent.

Note: __foo:A__ and __realpath(foo)__ are different on some inputs. For
__realpath(foo)__ semantics, see the `__P__ ` modifier.

__c__

    Resolve a command name into an absolute path by searching the command path given by the __PATH__ variable. This does not work for commands containing directory parts. Note also that this does not usually work as a glob qualifier unless a file of the same name is found in the current directory.
__e__

    Remove all but the part of the filename extension following the `__.__ '; see the definition of the filename extension in the description of the __r__ modifier below. Note that according to that definition the result will be empty if the string ends with a `__.__ '.
__h__ [ *digits* ]

    Remove a trailing pathname component, shortening the path by one directory level: this is the `head' of the pathname. This works like `__dirname__ '. If the __h__ is followed immediately (with no spaces or other separator) by any number of decimal digits, and the value of the resulting number is non-zero, that number of leading components is preserved instead of the final component being removed. In an absolute path the leading `__/__ ' is the first component, so, for example, if __var=/my/path/to/something__ , then __${var:h3}__ substitutes __/my/path__. Consecutive `/'s are treated the same as a single `/'. In parameter substitution, digits may only be used if the expression is in braces, so for example the short form substitution __$var:h2__ is treated as __${var:h}2__ , not as __${var:h2}__. No restriction applies to the use of digits in history substitution or globbing qualifiers. If more components are requested than are present, the entire path is substituted (so this does not trigger a `failed modifier' error in history expansion).
__l__

    Convert the words to all lowercase.
__p__

    Print the new command but do not execute it. Only works with history expansion.
__P__

    Turn a file name into an absolute path, like __realpath(3)__. The resulting path will be absolute, will refer to the same directory entry as the input filename, and none of its components will be symbolic links or equal to `__.__ ' or `__..__ '.
Unlike __realpath(3)__ , non-existent trailing components are permitted and
preserved.

__q__

    Quote the substituted words, escaping further substitutions. Works with history expansion and parameter expansion, though for parameters it is only useful if the resulting text is to be re-evaluated such as by __eval__.
__Q__

    Remove one level of quotes from the substituted words.
__r__

    Remove a filename extension leaving the root name. Strings with no filename extension are not altered. A filename extension is a `__.__ ' followed by any number of characters (including zero) that are neither `__.__ ' nor `__/__ ' and that continue to the end of the string. For example, the extension of `__foo.orig.c__ ' is `__.c__ ', and `__dir.c/foo__ ' has no extension.
__s/__*l*__/__*r*[__/__]

    Substitute *r* for *l* as described below. The substitution is done only for the first string that matches *l*. For arrays and for filename generation, this applies to each word of the expanded text. See below for further notes on substitutions.
The forms `__gs/__*l*__/__*r* ' and `__s/__*l*__/__*r*__/:G__ ' perform global
substitution, i.e. substitute every occurrence of *r* for *l*. Note that the
__g__ or __:G__ must appear in exactly the position shown.

See further notes on this form of substitution below.

__&__

    Repeat the previous __s__ substitution. Like __s__ , may be preceded immediately by a __g__. In parameter expansion the __&__ must appear inside braces, and in filename generation it must be quoted with a backslash.
__t__ [ *digits* ]

    Remove all leading pathname components, leaving the final component (tail). This works like `__basename__ '. Any trailing slashes are first removed. Decimal digits are handled as described above for (h), but in this case that number of trailing components is preserved instead of the default 1; 0 is treated the same as 1.
__u__

    Convert the words to all uppercase.
__x__

    Like __q__ , but break into words at whitespace. Does not work with parameter expansion.
The __s/__*l*__/__*r*__/__ substitution works as follows. By default the left-
hand side of substitutions are not patterns, but character strings. Any
character can be used as the delimiter in place of `__/__ '. A backslash
quotes the delimiter character. The character `__&__ ', in the right-hand-side
*r* , is replaced by the text from the left-hand-side *l*. The `__&__ ' can be
quoted with a backslash. A null *l* uses the previous string either from the
previous *l* or from the contextual scan string *s* from `__!?__*s* '. You can
omit the rightmost delimiter if a newline immediately follows *r* ; the
rightmost `__?__ ' in a context scan can similarly be omitted. Note the same
record of the last *l* and *r* is maintained across all forms of expansion.

Note that if a `__&__ ' is used within glob qualifiers an extra backslash is
needed as a __&__ is a special character in this case.

Also note that the order of expansions affects the interpretation of *l* and
*r*. When used in a history expansion, which occurs before any other
expansions, *l* and *r* are treated as literal strings (except as explained
for __HIST_SUBST_PATTERN__ below). When used in parameter expansion, the
replacement of *r* into the parameter's value is done first, and then any
additional process, parameter, command, arithmetic, or brace references are
applied, which may evaluate those substitutions and expansions more than once
if *l* appears more than once in the starting value. When used in a glob
qualifier, any substitutions or expansions are performed once at the time the
qualifier is parsed, even before the `__:s__ ' expression itself is divided
into *l* and *r* sides.

If the option __HIST_SUBST_PATTERN__ is set, *l* is treated as a pattern of
the usual form described in the section FILENAME GENERATION below. This can be
used in all the places where modifiers are available; note, however, that in
globbing qualifiers parameter substitution has already taken place, so
parameters in the replacement string should be quoted to ensure they are
replaced at the correct time. Note also that complicated patterns used in
globbing qualifiers may need the extended glob qualifier notation
__(#q:s/__*...*__/__*...*__/)__ in order for the shell to recognize the
expression as a glob qualifier. Further, note that bad patterns in the
substitution are not subject to the __NO_BAD_PATTERN__ option so will cause an
error.

When __HIST_SUBST_PATTERN__ is set, *l* may start with a __#__ to indicate
that the pattern must match at the start of the string to be substituted, and
a __%__ may appear at the start or after an __#__ to indicate that the pattern
must match at the end of the string to be substituted. The __%__ or __#__ may
be quoted with two backslashes.

For example, the following piece of filename generation code with the
__EXTENDED_GLOB__ option:

[code]

    __print -r -- *.c(#q:s/#%(#b)s(*).c/'S${match[1]}.C'/)__
[/code]

takes the expansion of __*.c__ and applies the glob qualifiers in the __(#q__
*...*__)__ expression, which consists of a substitution modifier anchored to
the start and end of each word (__#%__). This turns on backreferences
(__(#b)__), so that the parenthesised subexpression is available in the
replacement string as __${match[1]}__. The replacement string is quoted so
that the parameter is not substituted before the start of filename generation.

The following __f__ , __F__ , __w__ and __W__ modifiers work only with
parameter expansion and filename generation. They are listed here to provide a
single point of reference for all modifiers.

__f__

    Repeats the immediately (without a colon) following modifier until the resulting word doesn't change any more.
__F:__*expr*__:__

    Like __f__ , but repeats only *n* times if the expression *expr* evaluates to *n*. Any character can be used instead of the `__:__ '; if `__(__ ', `__[__ ', or `__{__ ' is used as the opening delimiter, the closing delimiter should be '__)__ ', `__]__ ', or `__}__ ', respectively.
__w__

    Makes the immediately following modifier work on each word in the string.
__W:__*sep*__:__

    Like __w__ but words are considered to be the parts of the string that are separated by *sep*. Any character can be used instead of the `__:__ '; opening parentheses are handled specially, see above.
# PROCESS SUBSTITUTION

Each part of a command argument that takes the form `__<(__*list*__)__ ',
`__>(__*list*__)__ ' or `__=(__*list*__)__ ' is subject to process
substitution. The expression may be preceded or followed by other strings
except that, to prevent clashes with commonly occurring strings and patterns,
the last form must occur at the start of a command argument, and the forms are
only expanded when first parsing command or assignment arguments. Process
substitutions may be used following redirection operators; in this case, the
substitution must appear with no trailing string.

Note that `__< <(__*list*__)__ ' is not a special syntax; it is equivalent to
`__< <(__*list*__)__ ', redirecting standard input from the result of process
substitution. Hence all the following documentation applies. The second form
(with the space) is recommended for clarity.

In the case of the __<__ or __>__ forms, the shell runs the commands in *list*
as a subprocess of the job executing the shell command line. If the system
supports the __/dev/fd__ mechanism, the command argument is the name of the
device file corresponding to a file descriptor; otherwise, if the system
supports named pipes (FIFOs), the command argument will be a named pipe. If
the form with __>__ is selected then writing on this special file will provide
input for *list*. If __<__ is used, then the file passed as an argument will
be connected to the output of the *list* process. For example,

[code]

    ______paste <(cut -f1______*file1*______) <(cut -f3______*file2*______) |__
    __tee >(______*process1*______) >(______*process2*______) >/dev/null__________
[/code]

cuts fields 1 and 3 from the files *file1* and *file2* respectively, pastes
the results together, and sends it to the processes *process1* and *process2*.

If __=(__*...*__)__ is used instead of __<(__*...*__)__ , then the file passed
as an argument will be the name of a temporary file containing the output of
the *list* process. This may be used instead of the __<__ form for a program
that expects to lseek (see *lseek*(2)) on the input file.

There is an optimisation for substitutions of the form __=( <<<__*arg*__)__ ,
where *arg* is a single-word argument to the here-string redirection __< <<__.
This form produces a file name containing the value of *arg* after any
substitutions have been performed. This is handled entirely within the current
shell. This is effectively the reverse of the special form __$( <__*arg*__)__
which treats *arg* as a file name and replaces it with the file's contents.

The __=__ form is useful as both the __/dev/fd__ and the named pipe
implementation of __<(__*...*__)__ have drawbacks. In the former case, some
programmes may automatically close the file descriptor in question before
examining the file on the command line, particularly if this is necessary for
security reasons such as when the programme is running setuid. In the second
case, if the programme does not actually open the file, the subshell
attempting to read from or write to the pipe will (in a typical
implementation, different operating systems may have different behaviour)
block for ever and have to be killed explicitly. In both cases, the shell
actually supplies the information using a pipe, so that programmes that expect
to lseek (see *lseek*(2)) on the file will not work.

Also note that the previous example can be more compactly and efficiently
written (provided the __MULTIOS__ option is set) as:

[code]

    ______paste <(cut -f1______*file1*______) <(cut -f3______*file2*______)________> >(______*process1*______) > >(______*process2*______)__________
[/code]

The shell uses pipes instead of FIFOs to implement the latter two process
substitutions in the above example.

There is an additional problem with __>(__*process*__)__ ; when this is
attached to an external command, the parent shell does not wait for *process*
to finish and hence an immediately following command cannot rely on the
results being complete. The problem and solution are the same as described in
the section *MULTIOS* in *zshmisc*(1). Hence in a simplified version of the
example above:

[code]

    ______paste <(cut -f1______*file1*______) <(cut -f3______*file2*______)________> >(______*process*______)__________
[/code]

(note that no __MULTIOS__ are involved), *process* will be run asynchronously
as far as the parent shell is concerned. The workaround is:

[code]

    ______{ paste <(cut -f1______*file1*______) <(cut -f3______*file2*______) }________> >(______*process*______)__________
[/code]

The extra processes here are spawned from the parent shell which will wait for
their completion.

Another problem arises any time a job with a substitution that requires a
temporary file is disowned by the shell, including the case where `__&!__' or
`__& |__' appears at the end of a command containing a substitution. In that
case the temporary file will not be cleaned up as the shell no longer has any
memory of the job. A workaround is to use a subshell, for example,

[code]

    __(mycmd =(myoutput)) &!__
[/code]

as the forked subshell will wait for the command to finish then remove the
temporary file.

A general workaround to ensure a process substitution endures for an
appropriate length of time is to pass it as a parameter to an anonymous shell
function (a piece of shell code that is run immediately with function scope).
For example, this code:

[code]

    __() {__
      
    
    __print File $1:__
      
    
    __cat $1__
    __} =(print This be the verse)__
[/code]

outputs something resembling the following

[code]

    __File /tmp/zsh6nU0kS:__
    __This be the verse__
[/code]

The temporary file created by the process substitution will be deleted when
the function exits.

# PARAMETER EXPANSION

The character `__$__ ' is used to introduce parameter expansions. See
*zshparam*(1) for a description of parameters, including arrays, associative
arrays, and subscript notation to access individual array elements.

Note in particular the fact that words of unquoted parameters are not
automatically split on whitespace unless the option __SH_WORD_SPLIT__ is set;
see references to this option below for more details. This is an important
difference from other shells. However, as in other shells, null words are
elided from unquoted parameters' expansions.

With default options, after the assignments:

[code]

    __array=( "first word" "" "third word")__
    __scalar= "only word"__
[/code]

then __$array__ substitutes two words, `__first word__ ' and `__third__
__word__ ', and __$scalar__ substitutes a single word `__only word__ '. Note
that second element of __array__ was elided. Scalar parameters can be elided
too if their value is null (empty). To avoid elision, use quoting as follows:
__" $scalar"__ for scalars and __" ${array[@]}"__ or __" ${(@)array}"__ for
arrays. (The last two forms are equivalent.)

Parameter expansions can involve *flags* , as in `__${(@kv)aliases}__ ', and
other operators, such as `__${PREFIX:- "/usr/local"}__'. Parameter expansions
can also be nested. These topics will be introduced below. The full rules are
complicated and are noted at the end.

In the expansions discussed below that require a pattern, the form of the
pattern is the same as that used for filename generation; see the section
`Filename Generation'. Note that these patterns, along with the replacement
text of any substitutions, are themselves subject to parameter expansion,
command substitution, and arithmetic expansion. In addition to the following
operations, the colon modifiers described in the section `Modifiers' in the
section `History Expansion' can be applied: for example, __${i:s/foo/bar/}__
performs string substitution on the expansion of parameter __$i__.

In the following descriptions, `*word* ' refers to a single word substituted
on the command line, not necessarily a space delimited word.

__${__*name*__}__

    The value, if any, of the parameter *name* is substituted. The braces are required if the expansion is to be followed by a letter, digit, or underscore that is not to be interpreted as part of *name*. In addition, more complicated forms of substitution usually require the braces to be present; exceptions, which only apply if the option __KSH_ARRAYS__ is not set, are a single subscript or any colon modifiers appearing after the name, or any of the characters `__^__ ', `__=__ ', `__~__ ', `__#__ ' or `__+__ ' appearing before the name, all of which work with or without braces.
If *name* is an array parameter, and the __KSH_ARRAYS__ option is not set,
then the value of each element of *name* is substituted, one element per word.
Otherwise, the expansion results in one word only; with __KSH_ARRAYS__ , this
is the first element of an array. No field splitting is done on the result
unless the __SH_WORD_SPLIT__ option is set. See also the flags __=__ and
__s:__*string*__:__.

__${+__*name*__}__

    If *name* is the name of a set parameter `__1__ ' is substituted, otherwise `__0__ ' is substituted.
__${__*name*__-__*word*__}__

    
__${__*name*__:-__*word*__}__

    If *name* is set, or in the second form is non-null, then substitute its value; otherwise substitute *word*. In the second form *name* may be omitted, in which case *word* is always substituted.
__${__*name*__+__*word*__}__

    
__${__*name*__:+__*word*__}__

    If *name* is set, or in the second form is non-null, then substitute *word* ; otherwise substitute nothing.
__${__*name*__=__*word*__}__

    
__${__*name*__:=__*word*__}__

    
__${__*name*__::=__*word*__}__

    In the first form, if *name* is unset then set it to *word* ; in the second form, if *name* is unset or null then set it to *word* ; and in the third form, unconditionally set *name* to *word*. In all forms, the value of the parameter is then substituted.
__${__*name*__?__*word*__}__

    
__${__*name*__:?__*word*__}__

    In the first form, if *name* is set, or in the second form if *name* is both set and non-null, then substitute its value; otherwise, print *word* and exit from the shell. Interactive shells instead return to the prompt. If *word* is omitted, then a standard message is printed.
In any of the above expressions that test a variable and substitute an
alternate *word* , note that you can use standard shell quoting in the *word*
value to selectively override the splitting done by the __SH_WORD_SPLIT__
option and the __=__ flag, but not splitting by the __s:__*string*__:__ flag.

In the following expressions, when *name* is an array and the substitution is
not quoted, or if the `__(@)__ ' flag or the *name*__[@]__ syntax is used,
matching and replacement is performed on each array element separately.

__${__*name*__#__*pattern*__}__

    
__${__*name*__##__*pattern*__}__

    If the *pattern* matches the beginning of the value of *name* , then substitute the value of *name* with the matched portion deleted; otherwise, just substitute the value of *name*. In the first form, the smallest matching pattern is preferred; in the second form, the largest matching pattern is preferred.
__${__*name*__%__*pattern*__}__

    
__${__*name*__%%__*pattern*__}__

    If the *pattern* matches the end of the value of *name* , then substitute the value of *name* with the matched portion deleted; otherwise, just substitute the value of *name*. In the first form, the smallest matching pattern is preferred; in the second form, the largest matching pattern is preferred.
__${__*name*__:#__*pattern*__}__

    If the *pattern* matches the value of *name* , then substitute the empty string; otherwise, just substitute the value of *name*. If *name* is an array the matching array elements are removed (use the `__(M)__ ' flag to remove the non-matched elements).
__${__*name*__:|__*arrayname*__}__

    If *arrayname* is the name (N.B., not contents) of an array variable, then any elements contained in *arrayname* are removed from the substitution of *name*. If the substitution is scalar, either because *name* is a scalar variable or the expression is quoted, the elements of *arrayname* are instead tested against the entire expression.
__${__*name*__:*__*arrayname*__}__

    Similar to the preceding substitution, but in the opposite sense, so that entries present in both the original substitution and as elements of *arrayname* are retained and others removed.
__${__*name*__:^__*arrayname*__}__

    
__${__*name*__:^^__*arrayname*__}__

    Zips two arrays, such that the output array is twice as long as the shortest (longest for `__:^^__ ') of __name__ and __arrayname__ , with the elements alternatingly being picked from them. For `__:^__ ', if one of the input arrays is longer, the output will stop when the end of the shorter array is reached. Thus,
[code]

    __a=(1 2 3 4); b=(a b); print ${a:^b}__
[/code]

will output `__1 a 2 b__ '. For `__:^^__ ', then the input is repeated until
all of the longer array has been used up and the above will output `__1 a 2 b
3 a 4 b__ '.

Either or both inputs may be a scalar, they will be treated as an array of
length 1 with the scalar as the only element. If either array is empty, the
other array is output with no extra elements inserted.

Currently the following code will output `__a b__ ' and `__1__ ' as two
separate elements, which can be unexpected. The second print provides a
workaround which should continue to work if this is changed.

[code]

    __a=(a b); b=(1 2); print -l "${a:^b}"; print -l "${${a:^b}}"__
[/code]

__${__*name*__:__*offset*__}__

    
__${__*name*__:__*offset*__:__*length*__}__

    This syntax gives effects similar to parameter subscripting in the form __$__*name*__[__*start*__,__*end*__]__ , but is compatible with other shells; note that both *offset* and *length* are interpreted differently from the components of a subscript.
If *offset* is non-negative, then if the variable *name* is a scalar
substitute the contents starting *offset* characters from the first character
of the string, and if *name* is an array substitute elements starting *offset*
elements from the first element. If *length* is given, substitute that many
characters or elements, otherwise the entire rest of the scalar or array.

A positive *offset* is always treated as the offset of a character or element
in *name* from the first character or element of the array (this is different
from native zsh subscript notation). Hence 0 refers to the first character or
element regardless of the setting of the option __KSH_ARRAYS__.

A negative offset counts backwards from the end of the scalar or array, so
that -1 corresponds to the last character or element, and so on.

When positive, *length* counts from the *offset* position toward the end of
the scalar or array. When negative, *length* counts back from the end. If this
results in a position smaller than *offset* , a diagnostic is printed and
nothing is substituted.

The option __MULTIBYTE__ is obeyed, i.e. the offset and length count multibyte
characters where appropriate.

*offset* and *length* undergo the same set of shell substitutions as for scalar assignment; in addition, they are then subject to arithmetic evaluation. Hence, for example
[code]

    __print ${foo:3}__
    __print ${foo: 1 + 2}__
    __print ${foo:$(( 1 + 2))}__
    __print ${foo:$(echo 1 + 2)}__
[/code]

all have the same effect, extracting the string starting at the fourth character of __$foo__ if the substitution would otherwise return a scalar, or the array starting at the fourth element if __$foo__ would return an array. Note that with the option __KSH_ARRAYS__ __$foo__ always returns a scalar (regardless of the use of the offset syntax) and a form such as __${foo[*]:3}__ is required to extract elements of an array named __foo__.
If *offset* is negative, the __-__ may not appear immediately after the __:__
as this indicates the __${__*name*__:-__*word*__}__ form of substitution.
Instead, a space may be inserted before the __-__. Furthermore, neither
*offset* nor *length* may begin with an alphabetic character or __&__ as these
are used to indicate history-style modifiers. To substitute a value from a
variable, the recommended approach is to precede it with a __$__ as this
signifies the intention (parameter substitution can easily be rendered
unreadable); however, as arithmetic substitution is performed, the expression
__${var: offs}__ does work, retrieving the offset from __$offs__.

For further compatibility with other shells there is a special case for array
offset 0. This usually accesses the first element of the array. However, if
the substitution refers to the positional parameter array, e.g. __$@__ or
__$*__ , then offset 0 instead refers to __$0__ , offset 1 refers to __$1__ ,
and so on. In other words, the positional parameter array is effectively
extended by prepending __$0__. Hence __${*:0:1}__ substitutes __$0__ and
__${*:1:1}__ substitutes __$1__.

__${__*name*__/__*pattern*__/__*repl*__}__

    
__${__*name*__//__*pattern*__/__*repl*__}__

    
__${__*name*__:/__*pattern*__/__*repl*__}__

    Replace the longest possible match of *pattern* in the expansion of parameter *name* by string *repl*. The first form replaces just the first occurrence, the second form all occurrences, and the third form replaces only if *pattern* matches the entire string. Both *pattern* and *repl* are subject to double-quoted substitution, so that expressions like __${name/$opat/$npat}__ will work, but obey the usual rule that pattern characters in __$opat__ are not treated specially unless either the option __GLOB_SUBST__ is set, or __$opat__ is instead substituted as __${~opat}__.
The *pattern* may begin with a `__#__ ', in which case the *pattern* must
match at the start of the string, or `__%__ ', in which case it must match at
the end of the string, or `__#%__ ' in which case the *pattern* must match the
entire string. The *repl* may be an empty string, in which case the final
`__/__ ' may also be omitted. To quote the final `__/__ ' in other cases it
should be preceded by a single backslash; this is not necessary if the `__/__
' occurs inside a substituted parameter. Note also that the `__#__ ', `__%__ '
and `__#%__ are not active if they occur inside a substituted parameter, even
at the start.

If, after quoting rules apply, __${__*name*__}__ expands to an array, the
replacements act on each element individually. Note also the effect of the
__I__ and __S__ parameter expansion flags below; however, the flags __M__ ,
__R__ , __B__ , __E__ and __N__ are not useful.

For example,

[code]

    __foo= "twinkle twinkle little star" sub="t*e" rep="spy"__
    __print ${foo//${~sub}/$rep}__
    __print ${(S)foo//${~sub}/$rep}__
[/code]

Here, the `__~__ ' ensures that the text of __$sub__ is treated as a pattern
rather than a plain string. In the first case, the longest match for __t*e__
is substituted and the result is `__spy star__ ', while in the second case,
the shortest matches are taken and the result is `__spy spy lispy star__ '.

__${#__*spec*__}__

    If *spec* is one of the above substitutions, substitute the length in characters of the result instead of the result itself. If *spec* is an array expression, substitute the number of elements of the result. This has the side-effect that joining is skipped even in quoted forms, which may affect other sub-expressions in *spec*. Note that `__^__ ', `__=__ ', and `__~__ ', below, must appear to the left of `__#__ ' when these forms are combined.
If the option __POSIX_IDENTIFIERS__ is not set, and *spec* is a simple name,
then the braces are optional; this is true even for special parameters so e.g.
__$#-__ and __$#*__ take the length of the string __$-__ and the array __$*__
respectively. If __POSIX_IDENTIFIERS__ is set, then braces are required for
the __#__ to be treated in this fashion.

__${^__*spec*__}__

    
__${^^__*spec*__}__

    Turn on the __RC_EXPAND_PARAM__ option for the evaluation of *spec* ; if the `__^__ ' is doubled, turn it off. When this option is set, array expansions of the form *foo*__${__*xx*__}__*bar* , where the parameter *xx* is set to __(__*a b c*__)__ , are substituted with `*fooabar foobbar foocbar* ' instead of the default `*fooa b cbar* '. Note that an empty array will therefore cause all arguments to be removed.
Internally, each such expansion is converted into the equivalent list for
brace expansion. E.g., __${^var}__ becomes __{$var[1],$var[2],__...__}__ , and
is processed as described in the section `Brace Expansion' below: note,
however, the expansion happens immediately, with any explicit brace expansion
happening later. If word splitting is also in effect the __$var[__*N*__]__ may
themselves be split into different list elements.

__${=__*spec*__}__

    
__${==__*spec*__}__

    Perform word splitting using the rules for __SH_WORD_SPLIT__ during the evaluation of *spec* , but regardless of whether the parameter appears in double quotes; if the `__=__ ' is doubled, turn it off. This forces parameter expansions to be split into separate words before substitution, using __IFS__ as a delimiter. This is done by default in most other shells.
Note that splitting is applied to *word* in the assignment forms of *spec*
*before* the assignment to *name* is performed. This affects the result of
array assignments with the __A__ flag.

__${~__*spec*__}__

    
__${~~__*spec*__}__

    Turn on the __GLOB_SUBST__ option for the evaluation of *spec* ; if the `__~__ ' is doubled, turn it off. When this option is set, the string resulting from the expansion will be interpreted as a pattern anywhere that is possible, such as in filename expansion and filename generation and pattern-matching contexts like the right hand side of the `__=__ ' and `__!=__ ' operators in conditions.
In nested substitutions, note that the effect of the __~__ applies to the
result of the current level of substitution. A surrounding pattern operation
on the result may cancel it. Hence, for example, if the parameter __foo__ is
set to __*__ , __${~foo//\\*/*.c}__ is substituted by the pattern __*.c__ ,
which may be expanded by filename generation, but __${${~foo}//\\*/*.c}__
substitutes to the string __*.c__ , which will not be further expanded.

If a __${__...__}__ type parameter expression or a __$(__...__)__ type command
substitution is used in place of *name* above, it is expanded first and the
result is used as if it were the value of *name*. Thus it is possible to
perform nested operations: __${${foo#head}%tail}__ substitutes the value of
__$foo__ with both `__head__ ' and `__tail__ ' deleted. The form with
__$(__...__)__ is often useful in combination with the flags described next;
see the examples below. Each *name* or nested __${__...__}__ in a parameter
expansion may also be followed by a subscript expression as described in
*Array Parameters* in *zshparam*(1).

Note that double quotes may appear around nested expressions, in which case
only the part inside is treated as quoted; for example, __${(f) "$(foo)"}__
quotes the result of __$(foo)__ , but the flag `__(f)__ ' (see below) is
applied using the rules for unquoted expansions. Note further that quotes are
themselves nested in this context; for example, in __" ${(@f)"$(foo)"}"__,
there are two sets of quotes, one surrounding the whole expression, the other
(redundant) surrounding the __$(foo)__ as before.

## Parameter Expansion Flags

If the opening brace is directly followed by an opening parenthesis, the
string up to the matching closing parenthesis will be taken as a list of
flags. In cases where repeating a flag is meaningful, the repetitions need not
be consecutive; for example, `(__q%q%q__)' means the same thing as the more
readable `(__%%qqq__)'. The following flags are supported:

__#__

    Evaluate the resulting words as numeric expressions and interpret these as character codes. Output the corresponding characters. Note that this form is entirely distinct from use of the __#__ without parentheses.
If the __MULTIBYTE__ option is set and the number is greater than 127 (i.e.
not an ASCII character) it is treated as a Unicode character.

__%__

    Expand all __%__ escapes in the resulting words in the same way as in prompts (see EXPANSION OF PROMPT SEQUENCES in *zshmisc*(1)). If this flag is given twice, full prompt expansion is done on the resulting words, depending on the setting of the __PROMPT_PERCENT__ , __PROMPT_SUBST__ and __PROMPT_BANG__ options.
__@__

    In double quotes, array elements are put into separate words. E.g., `__" ${(@)foo}"__' is equivalent to `__" ${foo[@]}"__' and `__" ${(@)foo[1,2]}"__' is the same as `__" $foo[1]" "$foo[2]"__'. This is distinct from *field splitting* by the __f__ , __s__ or __z__ flags, which still applies within each array element.
__A__

    Convert the substitution into an array expression, even if it otherwise would be scalar. This has lower precedence than subscripting, so one level of nested expansion is required in order that subscripts apply to array elements. Thus __${${(A____)__*name*__}[1]}__ yields the full value of *name* when *name* is scalar.
This assigns an array parameter with `__${__...__=__...__}__ ',
`__${__...__:=__...__}__ ' or `__${__...__::=__...__}__ '. If this flag is
repeated (as in `__AA__ '), assigns an associative array parameter. Assignment
is made before sorting or padding; if field splitting is active, the *word*
part is split before assignment. The *name* part may be a subscripted range
for ordinary arrays; when assigning an associative array, the *word* part
*must* be converted to an array, for example by using
`__${(AA)=__*name*__=__...__}__ ' to activate field splitting.

Surrounding context such as additional nesting or use of the value in a scalar
assignment may cause the array to be joined back into a single string again.

__a__

    Sort in array index order; when combined with `__O__ ' sort in reverse array index order. Note that `__a__ ' is therefore equivalent to the default but `__Oa__ ' is useful for obtaining an array's elements in reverse order.
__b__

    Quote with backslashes only characters that are special to pattern matching. This is useful when the contents of the variable are to be tested using __GLOB_SUBST__ , including the __${~__*...*__}__ switch.
Quoting using one of the __q__ family of flags does not work for this purpose
since quotes are not stripped from non-pattern characters by __GLOB_SUBST__.
In other words,

[code]

    __pattern=${(q)str}__
    __[[ $str = ${~pattern} ]]__
[/code]

works if __$str__ is `__a*b__ ' but not if it is `__a b__ ', whereas

[code]

    __pattern=${(b)str}__
    __[[ $str = ${~pattern} ]]__
[/code]

is always true for any possible value of __$str__.

__c__

    With __${#__*name*__}__ , count the total number of characters in an array, as if the elements were concatenated with spaces between them. This is not a true join of the array, so other expressions used with this flag may have an effect on the elements of the array before it is counted.
__C__

    Capitalize the resulting words. `Words' in this case refers to sequences of alphanumeric characters separated by non-alphanumerics, *not* to words that result from field splitting.
__D__

    Assume the string or array elements contain directories and attempt to substitute the leading part of these by names. The remainder of the path (the whole of it if the leading part was not substituted) is then quoted so that the whole string can be used as a shell argument. This is the reverse of `__~__ ' substitution: see the section FILENAME EXPANSION below.
__e__

    Perform single word shell expansions, namely *parameter expansion* , *command substitution* and *arithmetic expansion* , on the result. Such expansions can be nested but too deep recursion may have unpredictable effects.
__f__

    Split the result of the expansion at newlines. This is a shorthand for `__ps:\n:__ '.
__F__

    Join the words of arrays together using newline as a separator. This is a shorthand for `__pj:\n:__ '.
__g:__*opts*__:__

    Process escape sequences like the echo builtin when no options are given (__g::__). With the __o__ option, octal escapes don't take a leading zero. With the __c__ option, sequences like `__^X__ ' are also processed. With the __e__ option, processes `__\M-t__ ' and similar sequences like the print builtin. With both of the __o__ and __e__ options, behaves like the print builtin except that in none of these modes is `__\c__ ' interpreted.
__i__

    Sort case-insensitively. May be combined with `__n__ ' or `__O__ '.
__k__

    If *name* refers to an associative array, substitute the *keys* (element names) rather than the values of the elements. Used with subscripts (including ordinary arrays), force indices or keys to be substituted even if the subscript form refers to values. However, this flag may not be combined with subscript ranges. With the __KSH_ARRAYS__ option a subscript `__[*]__ ' or `__[@]__ ' is needed to operate on the whole array, as usual.
__L__

    Convert all letters in the result to lower case.
__n__

    Sort decimal integers numerically; if the first differing characters of two test strings are not digits, sorting is lexical. `__+__ ' and `__-__ ' are not treated specially; they are treated as any other non-digit. Integers with more initial zeroes are sorted before those with fewer or none. Hence the array `__foo+24 foo1 foo02__ __foo2 foo3 foo20 foo23__ ' is sorted into the order shown. May be combined with `__i__ ' or `__O__ '.
__-__

    As __n__ , but a leading minus sign indicates a negative decimal integer. A leading minus sign not followed by an integer does not trigger numeric sorting. Note that `__+__ ' signs are not handled specially (this may change in the future).
__o__

    Sort the resulting words in ascending order; if this appears on its own the sorting is lexical and case-sensitive (unless the locale renders it case-insensitive). Sorting in ascending order is the default for other forms of sorting, so this is ignored if combined with `__a__ ', `__i__ ', `__n__ ' or `__-__ '.
__O__

    Sort the resulting words in descending order; `__O__ ' without `__a__ ', `__i__ ', `__n__ ' or `__-__ ' sorts in reverse lexical order. May be combined with `__a__ ', `__i__ ', `__n__ ' or `__-__ ' to reverse the order of sorting.
__P__

    This forces the value of the parameter *name* to be interpreted as a further parameter name, whose value will be used where appropriate. Note that flags set with one of the __typeset__ family of commands (in particular case transformations) are not applied to the value of *name* used in this fashion.
If used with a nested parameter or command substitution, the result of that
will be taken as a parameter name in the same way. For example, if you have
`__foo=bar__ ' and `__bar=baz__ ', the strings __${(P)foo}__ ,
__${(P)${foo}}__ , and __${(P)$(echo bar)}__ will be expanded to `__baz__ '.

Likewise, if the reference is itself nested, the expression with the flag is
treated as if it were directly replaced by the parameter name. It is an error
if this nested substitution produces an array with more than one word. For
example, if `__name=assoc__ ' where the parameter __assoc__ is an associative
array, then `__${${(P)name}[elt]}__ ' refers to the element of the associative
subscripted `__elt__ '.

__q__

    Quote characters that are special to the shell in the resulting words with backslashes; unprintable or invalid characters are quoted using the __$'\__*NNN*__'__ form, with separate quotes for each octet.
If this flag is given twice, the resulting words are quoted in single quotes
and if it is given three times, the words are quoted in double quotes; in
these forms no special handling of unprintable or invalid characters is
attempted. If the flag is given four times, the words are quoted in single
quotes preceded by a __$__. Note that in all three of these forms quoting is
done unconditionally, even if this does not change the way the resulting
string would be interpreted by the shell.

If a __q-__ is given (only a single __q__ may appear), a minimal form of
single quoting is used that only quotes the string if needed to protect
special characters. Typically this form gives the most readable output.

If a __q+__ is given, an extended form of minimal quoting is used that causes
unprintable characters to be rendered using __$'__*...*__'__. This quoting is
similar to that used by the output of values by the __typeset__ family of
commands.

__Q__

    Remove one level of quotes from the resulting words.
__t__

    Use a string describing the type of the parameter where the value of the parameter would usually appear. This string consists of keywords separated by hyphens (`__-__ '). The first keyword in the string describes the main type, it can be one of `__scalar__ ', `__array__ ', `__integer__ ', `__float__ ' or `__association__ '. The other keywords describe the type in more detail:
__local__

    for local parameters
__left__

    for left justified parameters
__right_blanks__

    for right justified parameters with leading blanks
__right_zeros__

    for right justified parameters with leading zeros
__lower__

    for parameters whose value is converted to all lower case when it is expanded
__upper__

    for parameters whose value is converted to all upper case when it is expanded
__readonly__

    for readonly parameters
__tag__

    for tagged parameters
__tied__

    for parameters tied to another parameter in the manner of __PATH__ (colon-separated list) and __path__ (array), whether these are special parameters or user-defined with `__typeset -T__ '
__export__

    for exported parameters
__unique__

    for arrays which keep only the first occurrence of duplicated values
__hide__

    for parameters with the `hide' flag
__hideval__

    for parameters with the `hideval' flag
__special__

    for special parameters defined by the shell
__u__

    Expand only the first occurrence of each unique word.
__U__

    Convert all letters in the result to upper case.
__v__

    Used with __k__ , substitute (as two consecutive words) both the key and the value of each associative array element. Used with subscripts, force values to be substituted even if the subscript form refers to indices or keys.
__V__

    Make any special characters in the resulting words visible.
__w__

    With __${#__*name*__}__ , count words in arrays or strings; the __s__ flag may be used to set a word delimiter.
__W__

    Similar to __w__ with the difference that empty words between repeated delimiters are also counted.
__X__

    With this flag, parsing errors occurring with the __Q__ , __e__ and __#__ flags or the pattern matching forms such as `__${__*name*__#__*pattern*__}__ ' are reported. Without the flag, errors are silently ignored.
__z__

    Split the result of the expansion into words using shell parsing to find the words, i.e. taking into account any quoting in the value. Comments are not treated specially but as ordinary strings, similar to interactive shells with the __INTERACTIVE_COMMENTS__ option unset (however, see the __Z__ flag below for related options)
Note that this is done very late, even later than the `__(s)__ ' flag. So to
access single words in the result use nested expansions as in
`__${${(z)foo}[2]}__ '. Likewise, to remove the quotes in the resulting words
use `__${(Q)${(z)foo}}__ '.

__0__

    Split the result of the expansion on null bytes. This is a shorthand for `__ps:\0:__ '.
The following flags (except __p__) are followed by one or more arguments as
shown. Any character, or the matching pairs `__(__...__)__ ', `__{__...__}__
', `__[__...__]__ ', or `__<__...__>__ ', may be used in place of a colon as
delimiters, but note that when a flag takes more than one argument, a matched
pair of delimiters must surround each argument.

__p__

    Recognize the same escape sequences as the __print__ builtin in string arguments to any of the flags described below that follow this argument.
Alternatively, with this option string arguments may be in the form __$__*var*
in which case the value of the variable is substituted. Note this form is
strict; the string argument does not undergo general parameter expansion.

For example,

[code]

    __sep=:__
    __val=a:b:c__
    __print ${(ps.$sep.)val}__
[/code]

splits the variable on a __:__.

__~__

    Strings inserted into the expansion by any of the flags below are to be treated as patterns. This applies to the string arguments of flags that follow __~__ within the same set of parentheses. Compare with __~__ outside parentheses, which forces the entire substituted string to be treated as a pattern. Hence, for example,
[code]

    __[[ "?" = ${(~j.|.)array} ]]__
[/code]

treats `__|__ ' as a pattern and succeeds if and only if __$array__ contains
the string `__?__ ' as an element. The __~__ may be repeated to toggle the
behaviour; its effect only lasts to the end of the parenthesised group.

__j:__*string*__:__

    Join the words of arrays together using *string* as a separator. Note that this occurs before field splitting by the __s:__*string*__:__ flag or the __SH_WORD_SPLIT__ option.
__l:__*expr*__::__*string1*__::__*string2*__:__

    Pad the resulting words on the left. Each word will be truncated if required and placed in a field *expr* characters wide.
The arguments __:__*string1*__:__ and __:__*string2*__:__ are optional;
neither, the first, or both may be given. Note that the same pairs of
delimiters must be used for each of the three arguments. The space to the left
will be filled with *string1* (concatenated as often as needed) or spaces if
*string1* is not given. If both *string1* and *string2* are given, *string2*
is inserted once directly to the left of each word, truncated if necessary,
before *string1* is used to produce any remaining padding.

If either of *string1* or *string2* is present but empty, i.e. there are two
delimiters together at that point, the first character of __$IFS__ is used
instead.

If the __MULTIBYTE__ option is in effect, the flag __m__ may also be given, in
which case widths will be used for the calculation of padding; otherwise
individual multibyte characters are treated as occupying one unit of width.

If the __MULTIBYTE__ option is not in effect, each byte in the string is
treated as occupying one unit of width.

Control characters are always assumed to be one unit wide; this allows the
mechanism to be used for generating repetitions of control characters.

__m__

    Only useful together with one of the flags __l__ or __r__ or with the __#__ length operator when the __MULTIBYTE__ option is in effect. Use the character width reported by the system in calculating how much of the string it occupies or the overall length of the string. Most printable characters have a width of one unit, however certain Asian character sets and certain special effects use wider characters; combining characters have zero width. Non-printable characters are arbitrarily counted as zero width; how they would actually be displayed will vary.
If the __m__ is repeated, the character either counts zero (if it has zero
width), else one. For printable character strings this has the effect of
counting the number of glyphs (visibly separate characters), except for the
case where combining characters themselves have non-zero width (true in
certain alphabets).

__r:__*expr*__::__*string1*__::__*string2*__:__

    As __l__ , but pad the words on the right and insert *string2* immediately to the right of the string to be padded.
Left and right padding may be used together. In this case the strategy is to
apply left padding to the first half width of each of the resulting words, and
right padding to the second half. If the string to be padded has odd width the
extra padding is applied on the left.

__s:__*string*__:__

    Force field splitting at the separator *string*. Note that a *string* of two or more characters means that all of them must match in sequence; this differs from the treatment of two or more characters in the __IFS__ parameter. See also the __=__ flag and the __SH_WORD_SPLIT__ option. An empty string may also be given in which case every character will be a separate element.
For historical reasons, the usual behaviour that empty array elements are
retained inside double quotes is disabled for arrays generated by splitting;
hence the following:

[code]

    __line= "one::three"__
    __print -l "${(s.:.)line}"__
[/code]

produces two lines of output for __one__ and __three__ and elides the empty
field. To override this behaviour, supply the `__(@)__ ' flag as well, i.e.
__" ${(@s.:.)line}"__.

__Z:__*opts*__:__

    As __z__ but takes a combination of option letters between a following pair of delimiter characters. With no options the effect is identical to __z__. The following options are available:
__(Z+c+)__

    causes comments to be parsed as a string and retained; any field in the resulting array beginning with an unquoted comment character is a comment.
__(Z+C+)__

    causes comments to be parsed and removed. The rule for comments is standard: anything between a word starting with the third character of __$HISTCHARS__ , default __#__ , up to the next newline is a comment.
__(Z+n+)__

    causes unquoted newlines to be treated as ordinary whitespace, else they are treated as if they are shell code delimiters and converted to semicolons.
Options are combined within the same set of delimiters, e.g. __(Z+Cn+)__.

___:__*flags*__:__

    The underscore (_____) flag is reserved for future use. As of this revision of zsh, there are no valid *flags* ; anything following an underscore, other than an empty pair of delimiters, is treated as an error, and the flag itself has no effect.
The following flags are meaningful with the __${__...__#__...__}__ or
__${__...__%__...__}__ forms. The __S__ , __I__ , and __*__ flags may also be
used with the __${__...__/__...__}__ forms.

__S__

    With __#__ or __##__ , search for the match that starts closest to the start of the string (a `substring match'). Of all matches at a particular position, __#__ selects the shortest and __##__ the longest:
[code]

    __% str= "aXbXc"__
    __% echo ${(S)str#X*}__
    __abXc__
    __% echo ${(S)str##X*}__
    __a__
    __%__
[/code]

With __%__ or __%%__ , search for the match that starts closest to the end of
the string:

[code]

    __% str= "aXbXc"__
    __% echo ${(S)str%X*}__
    __aXbc__
    __% echo ${(S)str%%X*}__
    __aXb__
    __%__
[/code]

(Note that __%__ and __%%__ don't search for the match that ends closest to
the end of the string, as one might expect.)

With substitution via __${__...__/__...__}__ or __${__...__//__...__}__ ,
specifies non-greedy matching, i.e. that the shortest instead of the longest
match should be replaced:

[code]

    __% str= "abab"__
    __% echo ${str/*b/_}__
    _____
    __% echo ${(S)str/*b/_}__
    ___ab__
    __%__
[/code]

__I:__*expr*__:__

    Search the *expr* th match (where *expr* evaluates to a number). This only applies when searching for substrings, either with the __S__ flag, or with __${__...__/__...__}__ (only the *expr* th match is substituted) or __${__...__//__...__}__ (all matches from the *expr* th on are substituted). The default is to take the first match.
The *expr* th match is counted such that there is either one or zero matches
from each starting position in the string, although for global substitution
matches overlapping previous replacements are ignored. With the
__${__...__%__...__}__ and __${__...__%%__...__}__ forms, the starting
position for the match moves backwards from the end as the index increases,
while with the other forms it moves forward from the start.

Hence with the string

[code]

    __which switch is the right switch for Ipswich?__
[/code]

substitutions of the form __${__(__SI:__*N*__:__)__string#w*ch}__ as *N*
increases from 1 will match and remove `__which__ ', `__witch__ ', `__witch__
' and `__wich__ '; the form using `__##__ ' will match and remove `__which
switch__ __is the right switch for Ipswich__ ', `__witch is the right switch
for__ __Ipswich__ ', `__witch for Ipswich__ ' and `__wich__ '. The form using
`__%__ ' will remove the same matches as for `__#__ ', but in reverse order,
and the form using `__%%__ ' will remove the same matches as for `__##__ ' in
reverse order.

__*__

    Enable __EXTENDED_GLOB__ for substitution via __${__...__/__...__}__ or __${__...__//__...__}__. Note that `__**__ ' does not disable extendedglob.
__B__

    Include the index of the beginning of the match in the result.
__E__

    Include the index one character past the end of the match in the result (note this is inconsistent with other uses of parameter index).
__M__

    Include the matched portion in the result.
__N__

    Include the length of the match in the result.
__R__

    Include the unmatched portion in the result (the *R* est).
## Rules

Here is a summary of the rules for substitution; this assumes that braces are
present around the substitution, i.e. __${__*...*__}__. Some particular
examples are given below. Note that the Zsh Development Group accepts *no
responsibility* for any brain damage which may occur during the reading of the
following rules.

__1.__ *Nested substitution*

    If multiple nested __${__*...*__}__ forms are present, substitution is performed from the inside outwards. At each level, the substitution takes account of whether the current value is a scalar or an array, whether the whole substitution is in double quotes, and what flags are supplied to the current level of substitution, just as if the nested substitution were the outermost. The flags are not propagated up to enclosing substitutions; the nested substitution will return either a scalar or an array as determined by the flags, possibly adjusted for quoting. All the following steps take place where applicable at all levels of substitution.
Note that, unless the `__(P)__ ' flag is present, the flags and any subscripts
apply directly to the value of the nested substitution; for example, the
expansion __${${foo}}__ behaves exactly the same as __${foo}__. When the
`__(P)__ ' flag is present in a nested substitution, the other substitution
rules are applied to the value *before* it is interpreted as a name, so
__${${(P)foo}}__ may differ from __${(P)foo}__.

At each nested level of substitution, the substituted words undergo all forms
of single-word substitution (i.e. not filename generation), including command
substitution, arithmetic expansion and filename expansion (i.e. leading __~__
and __=__). Thus, for example, __${${:-=cat}:h}__ expands to the directory
where the __cat__ program resides. (Explanation: the internal substitution has
no parameter but a default value __=cat__ , which is expanded by filename
expansion to a full path; the outer substitution then applies the modifier
__:h__ and takes the directory part of the path.)

__2.__ *Internal parameter flags*

    Any parameter flags set by one of the __typeset__ family of commands, in particular the __-L__ , __-R__ , __-Z__ , __-u__ and __-l__ options for padding and capitalization, are applied directly to the parameter value. Note these flags are options to the command, e.g. `__typeset -Z__ '; they are not the same as the flags used within parameter substitutions.
At the outermost level of substitution, the `__(P)__ ' flag (rule __4.__)
ignores these transformations and uses the unmodified value of the parameter
as the name to be replaced. This is usually the desired behavior because
padding may make the value syntactically illegal as a parameter name, but if
capitalization changes are desired, use the __${${(P)foo}}__ form (rule
__25.__).

__3.__ *Parameter subscripting*

    If the value is a raw parameter reference with a subscript, such as __${__*var*__[3]}__ , the effect of subscripting is applied directly to the parameter. Subscripts are evaluated left to right; subsequent subscripts apply to the scalar or array value yielded by the previous subscript. Thus if __var__ is an array, __${var[1][2]}__ is the second character of the first word, but __${var[2,4][2]}__ is the entire third word (the second word of the range of words two through four of the original array). Any number of subscripts may appear. Flags such as `__(k)__ ' and `__(v)__ ' which alter the result of subscripting are applied.
__4.__ *Parameter name replacement*

    At the outermost level of nesting only, the `__(P)__ ' flag is applied. This treats the value so far as a parameter name (which may include a subscript expression) and replaces that with the corresponding value. This replacement occurs later if the `__(P)__ ' flag appears in a nested substitution.
If the value so far names a parameter that has internal flags (rule __2.__),
those internal flags are applied to the new value after replacement.

__5.__ *Double-quoted joining*

    If the value after this process is an array, and the substitution appears in double quotes, and neither an `__(@)__ ' flag nor a `__#__ ' length operator is present at the current level, then words of the value are joined with the first character of the parameter __$IFS__ , by default a space, between each word (single word arrays are not modified). If the `__(j)__ ' flag is present, that is used for joining instead of __$IFS__.
__6.__ *Nested subscripting*

    Any remaining subscripts (i.e. of a nested substitution) are evaluated at this point, based on whether the value is an array or a scalar. As with __3.__ , multiple subscripts can appear. Note that __${foo[2,4][2]}__ is thus equivalent to __${${foo[2,4]}[2]}__ and also to __" ${${(@)foo[2,4]}[2]}"__ (the nested substitution returns an array in both cases), but not to __" ${${foo[2,4]}[2]}"__ (the nested substitution returns a scalar because of the quotes).
__7.__ *Modifiers*

    Any modifiers, as specified by a trailing `__#__ ', `__%__ ', `__/__ ' (possibly doubled) or by a set of modifiers of the form `__:...__ ' (see the section `Modifiers' in the section `History Expansion'), are applied to the words of the value at this level.
__8.__ *Character evaluation*

    Any `__(#)__ ' flag is applied, evaluating the result so far numerically as a character.
__9.__ *Length*

    Any initial `__#__ ' modifier, i.e. in the form __${#__*var*__}__ , is used to evaluate the length of the expression so far.
__10.__ *Forced joining*

    If the `__(j)__ ' flag is present, or no `__(j)__ ' flag is present but the string is to be split as given by rule __11.__ , and joining did not take place at rule __5.__ , any words in the value are joined together using the given string or the first character of __$IFS__ if none. Note that the `__(F)__ ' flag implicitly supplies a string for joining in this manner.
__11.__ *Simple word splitting*

    If one of the `__(s)__ ' or `__(f)__ ' flags are present, or the `__=__ ' specifier was present (e.g. __${=__*var*__}__), the word is split on occurrences of the specified string, or (for __=__ with neither of the two flags present) any of the characters in __$IFS__.
If no `__(s)__ ', `__(f)__ ' or `__=__ ' was given, but the word is not quoted
and the option __SH_WORD_SPLIT__ is set, the word is split on occurrences of
any of the characters in __$IFS__. Note this step, too, takes place at all
levels of a nested substitution.

__12.__ *Case modification*

    Any case modification from one of the flags `__(L)__ ', `__(U)__ ' or `__(C)__ ' is applied.
__13.__ *Escape sequence replacement*

    First any replacements from the `__(g)__ ' flag are performed, then any prompt-style formatting from the `__(%)__ ' family of flags is applied.
__14.__ *Quote application*

    Any quoting or unquoting using `__(q)__ ' and `__(Q)__ ' and related flags is applied.
__15.__ *Directory naming*

    Any directory name substitution using `__(D)__ ' flag is applied.
__16.__ *Visibility enhancement*

    Any modifications to make characters visible using the `__(V)__ ' flag are applied.
__17.__ *Lexical word splitting*

    If the '__(z)__ ' flag or one of the forms of the '__(Z)__ ' flag is present, the word is split as if it were a shell command line, so that quotation marks and other metacharacters are used to decide what constitutes a word. Note this form of splitting is entirely distinct from that described by rule __11.__ : it does not use __$IFS__ , and does not cause forced joining.
__18.__ *Uniqueness*

    If the result is an array and the `__(u)__ ' flag was present, duplicate elements are removed from the array.
__19.__ *Ordering*

    If the result is still an array and one of the `__(o)__ ' or `__(O)__ ' flags was present, the array is reordered.
__20.__ __RC_EXPAND_PARAM__

    At this point the decision is made whether any resulting array elements are to be combined element by element with surrounding text, as given by either the __RC_EXPAND_PARAM__ option or the `__^__ ' flag.
__21.__ *Re-evaluation*

    Any `__(e)__ ' flag is applied to the value, forcing it to be re-examined for new parameter substitutions, but also for command and arithmetic substitutions.
__22.__ *Padding*

    Any padding of the value by the `__(l.__*fill*__.)__ ' or `__(r.__*fill*__.)__ ' flags is applied.
__23.__ *Semantic joining*

    In contexts where expansion semantics requires a single word to result, all words are rejoined with the first character of __IFS__ between. So in `__${(P____)${(f____)lines}}__ ' the value of __${lines}__ is split at newlines, but then must be joined again before the `__(P)__ ' flag can be applied.
If a single word is not required, this rule is skipped.

__24.__ *Empty argument removal*

    If the substitution does not appear in double quotes, any resulting zero-length argument, whether from a scalar or an element of an array, is elided from the list of arguments inserted into the command line.
Strictly speaking, the removal happens later as the same happens with other
forms of substitution; the point to note here is simply that it occurs after
any of the above parameter operations.

__25.__ *Nested parameter name replacement*

    If the `__(P)__ ' flag is present and rule __4.__ has not applied, the value so far is treated as a parameter name (which may include a subscript expression) and replaced with the corresponding value, with internal flags (rule __2.__) applied to the new value.
## Examples

The flag __f__ is useful to split a double-quoted substitution line by line.
For example, __${(f) "$(<__*file*__) "}__ substitutes the contents of *file*
divided so that each line is an element of the resulting array. Compare this
with the effect of __$____( <__*file*__)__ alone, which divides the file up by
words, or the same inside double quotes, which makes the entire content of the
file a single string.

The following illustrates the rules for nested parameter expansions. Suppose
that __$foo__ contains the array __(bar baz____)__ :

__" ${(@)${foo}[1]}"__

    This produces the result __b__. First, the inner substitution __" ${foo}"__, which has no array (__@__) flag, produces a single word result __" bar baz"__. The outer substitution __" ${(@)...[1]}"__ detects that this is a scalar, so that (despite the `__(@)__ ' flag) the subscript picks the first character.
__" ${${(@)foo}[1]}"__

    This produces the result `__bar__ '. In this case, the inner substitution __" ${(@)foo}"__ produces the array `__(bar baz____)__ '. The outer substitution __" ${...[1]}"__ detects that this is an array and picks the first word. This is similar to the simple case __" ${foo[1]}"__.
As an example of the rules for word splitting and joining, suppose __$foo__
contains the array `__(ax1 bx1____)__ '. Then

__${(s/x/)foo}__

    produces the words `__a__ ', `__1 b__ ' and `__1__ '.
__${(j/x/s/x/)foo}__

    produces `__a__ ', `__1__ ', `__b__ ' and `__1__ '.
__${(s/x/)foo%%1*}__

    produces `__a__ ' and `__b__ ' (note the extra space). As substitution occurs before either joining or splitting, the operation first generates the modified array __(ax bx____)__ , which is joined to give __" ax bx"__, and then split to give `__a__ ', `__b__ ' and `'. The final empty string will then be elided, as it is not in double quotes.
# COMMAND SUBSTITUTION

A command enclosed in parentheses preceded by a dollar sign, like
`__$(__...__)__ ', or quoted with grave accents, like `__`__...__`__ ', is
replaced with its standard output, with any trailing newlines deleted. If the
substitution is not enclosed in double quotes, the output is broken into words
using the __IFS__ parameter.

The substitution `__$(cat__ *foo*__)__ ' may be replaced by the faster `__$(
<__*foo*__)__ '. In this case *foo* undergoes single word shell expansions
(*parameter expansion* , *command substitution* and *arithmetic expansion*),
but not filename generation.

If the option __GLOB_SUBST__ is set, the result of any unquoted command
substitution, including the special form just mentioned, is eligible for
filename generation.

# ARITHMETIC EXPANSION

A string of the form `__$[__*exp*__]__ ' or `__$((__*exp*__))__ ' is
substituted with the value of the arithmetic expression *exp*. *exp* is
subjected to *parameter expansion* , *command substitution* and *arithmetic
expansion* before it is evaluated. See the section `Arithmetic Evaluation'.

# BRACE EXPANSION

A string of the form `*foo*__{__*xx*__,__*yy*__,__*zz*__}__*bar* ' is expanded
to the individual words `*fooxxbar* ', `*fooyybar* ' and `*foozzbar* '. Left-
to-right order is preserved. This construct may be nested. Commas may be
quoted in order to include them literally in a word.

An expression of the form `__{__*n1*__..__*n2*__}__ ', where *n1* and *n2* are
integers, is expanded to every number between *n1* and *n2* inclusive. If
either number begins with a zero, all the resulting numbers will be padded
with leading zeroes to that minimum width, but for negative numbers the __-__
character is also included in the width. If the numbers are in decreasing
order the resulting sequence will also be in decreasing order.

An expression of the form `__{__*n1*__..__*n2*__..__*n3*__}__ ', where *n1* ,
*n2* , and *n3* are integers, is expanded as above, but only every *n3* th
number starting from *n1* is output. If *n3* is negative the numbers are
output in reverse order, this is slightly different from simply swapping *n1*
and *n2* in the case that the step *n3* doesn't evenly divide the range. Zero
padding can be specified in any of the three numbers, specifying it in the
third can be useful to pad for example `__{-99..100..01}__ ' which is not
possible to specify by putting a 0 on either of the first two numbers (i.e.
pad to two characters).

An expression of the form `__{__*c1*__..__*c2*__}__ ', where *c1* and *c2* are
single characters (which may be multibyte characters), is expanded to every
character in the range from *c1* to *c2* in whatever character sequence is
used internally. For characters with code points below 128 this is US ASCII
(this is the only case most users will need). If any intervening character is
not printable, appropriate quotation is used to render it printable. If the
character sequence is reversed, the output is in reverse order, e.g.
`__{d..a}__ ' is substituted as `__d c b a__ '.

If a brace expression matches none of the above forms, it is left unchanged,
unless the option __BRACE_CCL__ (an abbreviation for `brace character class')
is set. In that case, it is expanded to a list of the individual characters
between the braces sorted into the order of the characters in the ASCII
character set (multibyte characters are not currently handled). The syntax is
similar to a __[__...__]__ expression in filename generation: `__-__ ' is
treated specially to denote a range of characters, but `__^__ ' or `__!__ ' as
the first character is treated normally. For example, `__{abcdef0-9}__ '
expands to 16 words __0 1 2 3 4 5 6 7 8 9 a b c d e f__.

Note that brace expansion is not part of filename generation (globbing); an
expression such as __*/{foo,bar}__ is split into two separate words __*/foo__
and __*/bar__ before filename generation takes place. In particular, note that
this is liable to produce a `no match' error if *either* of the two
expressions does not match; this is to be contrasted with __*/(foo|bar)__ ,
which is treated as a single pattern but otherwise has similar effects.

To combine brace expansion with array expansion, see the __${^__*spec*__}__
form described in the section `Parameter Expansion' above.

# FILENAME EXPANSION

Each word is checked to see if it begins with an unquoted `__~__ '. If it
does, then the word up to a `__/__ ', or the end of the word if there is no
`__/__ ', is checked to see if it can be substituted in one of the ways
described here. If so, then the `__~__ ' and the checked portion are replaced
with the appropriate substitute value.

A `__~__ ' by itself is replaced by the value of __$HOME__. A `__~__ '
followed by a `__+__ ' or a `__-__ ' is replaced by current or previous
working directory, respectively.

A `__~__ ' followed by a number is replaced by the directory at that position
in the directory stack. `__~0__ ' is equivalent to `__~+__ ', and `__~1__ ' is
the top of the stack. `__~+__ ' followed by a number is replaced by the
directory at that position in the directory stack. `__~+0__ ' is equivalent to
`__~+__ ', and `__~+1__ ' is the top of the stack. `__~-__ ' followed by a
number is replaced by the directory that many positions from the bottom of the
stack. `__~-0__ ' is the bottom of the stack. The __PUSHD_MINUS__ option
exchanges the effects of `__~+__ ' and `__~-__ ' where they are followed by a
number.

## Dynamic named directories

If the function __zsh_directory_name__ exists, or the shell variable
__zsh_directory_name_functions__ exists and contains an array of function
names, then the functions are used to implement dynamic directory naming. The
functions are tried in order until one returns status zero, so it is important
that functions test whether they can handle the case in question and return an
appropriate status.

A `__~__ ' followed by a string *namstr* in unquoted square brackets is
treated specially as a dynamic directory name. Note that the first unquoted
closing square bracket always terminates *namstr*. The shell function is
passed two arguments: the string __n__ (for name) and *namstr*. It should
either set the array __reply__ to a single element which is the directory
corresponding to the name and return status zero (executing an assignment as
the last statement is usually sufficient), or it should return status non-
zero. In the former case the element of reply is used as the directory; in the
latter case the substitution is deemed to have failed. If all functions fail
and the option __NOMATCH__ is set, an error results.

The functions defined as above are also used to see if a directory can be
turned into a name, for example when printing the directory stack or when
expanding __%~__ in prompts. In this case each function is passed two
arguments: the string __d__ (for directory) and the candidate for dynamic
naming. The function should either return non-zero status, if the directory
cannot be named by the function, or it should set the array reply to consist
of two elements: the first is the dynamic name for the directory (as would
appear within `__~[__*...*__]__ '), and the second is the prefix length of the
directory to be replaced. For example, if the trial directory is
__/home/myname/src/zsh__ and the dynamic name for __/home/myname/src__ (which
has 16 characters) is __s__ , then the function sets

[code]

    __reply=(s 16)__
[/code]

The directory name so returned is compared with possible static names for
parts of the directory path, as described below; it is used if the prefix
length matched (16 in the example) is longer than that matched by any static
name.

It is not a requirement that a function implements both __n__ and __d__ calls;
for example, it might be appropriate for certain dynamic forms of expansion
not to be contracted to names. In that case any call with the first argument
__d__ should cause a non-zero status to be returned.

The completion system calls `__zsh_directory_name c__ ' followed by equivalent
calls to elements of the array __zsh_directory_name_functions__ , if it
exists, in order to complete dynamic names for directories. The code for this
should be as for any other completion function as described in
*zshcompsys*(1).

As a working example, here is a function that expands any dynamic names
beginning with the string __p:__ to directories below __/home/pws/perforce__.
In this simple case a static name for the directory would be just as
effective.

[code]

    __zsh_directory_name() {__
      
    
    __emulate -L zsh__
      
    
    __setopt extendedglob__
      
    
    __local -a match mbegin mend__
      
    
    __if [[ $1 = d ]]; then__
      
    
    __# turn the directory into a name__
      
    
    __if [[ $2 = (#b)(/home/pws/perforce/)([^/]##)* ]]; then__
      
    
    __typeset -ga reply__
      
    
    __reply=(p:$match[2] $(( ${#match[1]} + ${#match[2]} )) )__
      
    
    __else__
      
    
    __return 1__
      
    
    __fi__
      
    
    __elif [[ $1 = n ]]; then__
      
    
    __# turn the name into a directory__
      
    
    __[[ $2 != (#b)p:(?*) ]] && return 1__
      
    
    __typeset -ga reply__
      
    
    __reply=(/home/pws/perforce/$match[1])__
      
    
    __elif [[ $1 = c ]]; then__
      
    
    __# complete names__
      
    
    __local expl__
      
    
    __local -a dirs__
      
    
    __dirs=(/home/pws/perforce/*(/:t))__
      
    
    __dirs=(p:${^dirs})__
      
    
    ___wanted dynamic-dirs expl 'dynamic directory' compadd -S\] -a dirs__
      
    
    __return__
      
    
    __else__
      
    
    __return 1__
      
    
    __fi__
      
    
    __return 0__
    __}__
[/code]

## Static named directories

A `__~__ ' followed by anything not already covered consisting of any number
of alphanumeric characters or underscore (`_____ '), hyphen (`__-__ '), or dot
(`__.__ ') is looked up as a named directory, and replaced by the value of
that named directory if found. Named directories are typically home
directories for users on the system. They may also be defined if the text
after the `__~__ ' is the name of a string shell parameter whose value begins
with a `__/__ '. Note that trailing slashes will be removed from the path to
the directory (though the original parameter is not modified).

It is also possible to define directory names using the __-d__ option to the
__hash__ builtin.

When the shell prints a path (e.g. when expanding __%~__ in prompts or when
printing the directory stack), the path is checked to see if it has a named
directory as its prefix. If so, then the prefix portion is replaced with a
`__~__ ' followed by the name of the directory. The shorter of the two ways of
referring to the directory is used, i.e. either the directory name or the full
path; the name is used if they are the same length. The parameters __$PWD__
and __$OLDPWD__ are never abbreviated in this fashion.

## `=' expansion

If a word begins with an unquoted `__=__ ' and the __EQUALS__ option is set,
the remainder of the word is taken as the name of a command. If a command
exists by that name, the word is replaced by the full pathname of the command.

## Notes

Filename expansion is performed on the right hand side of a parameter
assignment, including those appearing after commands of the __typeset__
family. In this case, the right hand side will be treated as a colon-separated
list in the manner of the __PATH__ parameter, so that a `__~__ ' or an `__=__
' following a `__:__ ' is eligible for expansion. All such behaviour can be
disabled by quoting the `__~__ ', the `__=__ ', or the whole expression (but
not simply the colon); the __EQUALS__ option is also respected.

If the option __MAGIC_EQUAL_SUBST__ is set, any unquoted shell argument in the
form `*identifier*__=__*expression* ' becomes eligible for file expansion as
described in the previous paragraph. Quoting the first `__=__ ' also inhibits
this.

# FILENAME GENERATION

If a word contains an unquoted instance of one of the characters `__*__ ',
`__(__ ', `__|__ ', `__<__ ', `__[__ ', or `__?__ ', it is regarded as a
pattern for filename generation, unless the __GLOB__ option is unset. If the
__EXTENDED_GLOB__ option is set, the `__^__ ' and `__#__ ' characters also
denote a pattern; otherwise they are not treated specially by the shell.

The word is replaced with a list of sorted filenames that match the pattern.
If no matching pattern is found, the shell gives an error message, unless the
__NULL_GLOB__ option is set, in which case the word is deleted; or unless the
__NOMATCH__ option is unset, in which case the word is left unchanged.

In filename generation, the character `__/__ ' must be matched explicitly;
also, a `__.__ ' must be matched explicitly at the beginning of a pattern or
after a `__/__ ', unless the __GLOB_DOTS__ option is set. No filename
generation pattern matches the files `__.__ ' or `__..__ '. In other instances
of pattern matching, the `__/__ ' and `__.__ ' are not treated specially.

## Glob Operators

__*__

    Matches any string, including the null string.
__?__

    Matches any character.
__[__...__]__

    Matches any of the enclosed characters. Ranges of characters can be specified by separating two characters by a `__-__ '. A `__-__ ' or `__]__ ' may be matched by including it as the first character in the list. There are also several named classes of characters, in the form `__[:__*name*__:]__ ' with the following meanings. The first set use the macros provided by the operating system to test for the given character combinations, including any modifications due to local language settings, see *ctype*(3):
__[:alnum:]__

    The character is alphanumeric
__[:alpha:]__

    The character is alphabetic
__[:ascii:]__

    The character is 7-bit, i.e. is a single-byte character without the top bit set.
__[:blank:]__

    The character is a blank character
__[:cntrl:]__

    The character is a control character
__[:digit:]__

    The character is a decimal digit
__[:graph:]__

    The character is a printable character other than whitespace
__[:lower:]__

    The character is a lowercase letter
__[:print:]__

    The character is printable
__[:punct:]__

    The character is printable but neither alphanumeric nor whitespace
__[:space:]__

    The character is whitespace
__[:upper:]__

    The character is an uppercase letter
__[:xdigit:]__

    The character is a hexadecimal digit
Another set of named classes is handled internally by the shell and is not
sensitive to the locale:

__[:IDENT:]__

    The character is allowed to form part of a shell identifier, such as a parameter name; this test respects the __POSIX_IDENTIFIERS__ option
__[:IFS:]__

    The character is used as an input field separator, i.e. is contained in the __IFS__ parameter
__[:IFSSPACE:]__

    The character is an IFS white space character; see the documentation for __IFS__ in the *zshparam*(1) manual page.
__[:INCOMPLETE:]__

    Matches a byte that starts an incomplete multibyte character. Note that there may be a sequence of more than one bytes that taken together form the prefix of a multibyte character. To test for a potentially incomplete byte sequence, use the pattern `__[[:INCOMPLETE:]]*__ '. This will never match a sequence starting with a valid multibyte character.
__[:INVALID:]__

    Matches a byte that does not start a valid multibyte character. Note this may be a continuation byte of an incomplete multibyte character as any part of a multibyte string consisting of invalid and incomplete multibyte characters is treated as single bytes.
__[:WORD:]__

    The character is treated as part of a word; this test is sensitive to the value of the __WORDCHARS__ parameter
Note that the square brackets are additional to those enclosing the whole set
of characters, so to test for a single alphanumeric character you need
`__[[:alnum:]]__ '. Named character sets can be used alongside other types,
e.g. `__[[:alpha:]0-9]__ '.

__[^__...__]__

    
__[!__...__]__

    Like __[__...__]__ , except that it matches any character which is not in the given set.
__<__[*x*]__-__[*y*]__>__

    Matches any number in the range *x* to *y* , inclusive. Either of the numbers may be omitted to make the range open-ended; hence `__< ->__' matches any number. To match individual digits, the __[__...__]__ form is more efficient.
Be careful when using other wildcards adjacent to patterns of this form; for
example, __< 0-9>*__ will actually match any number whatsoever at the start of
the string, since the `__< 0-9>__' will match the first digit, and the `__*__
' will match any others. This is a trap for the unwary, but is in fact an
inevitable consequence of the rule that the longest possible match always
succeeds. Expressions such as `__< 0-9>[^[:digit:]]*__' can be used instead.

__(__...__)__

    Matches the enclosed pattern. This is used for grouping. If the __KSH_GLOB__ option is set, then a `__@__ ', `__*__ ', `__+__ ', `__?__ ' or `__!__ ' immediately preceding the `__(__ ' is treated specially, as detailed below. The option __SH_GLOB__ prevents bare parentheses from being used in this way, though the __KSH_GLOB__ option is still available.
Note that grouping cannot extend over multiple directories: it is an error to
have a `__/__ ' within a group (this only applies for patterns used in
filename generation). There is one exception: a group of the form
__(__*pat*__/)#__ appearing as a complete path segment can match a sequence of
directories. For example, __foo/(a*/)#bar__ matches __foo/bar__ ,
__foo/any/bar__ , __foo/any/anyother/bar__ , and so on.

*x*__|__*y*
    Matches either *x* or *y*. This operator has lower precedence than any other. The `__|__ ' character must be within parentheses, to avoid interpretation as a pipeline. The alternatives are tried in order from left to right.
__^__*x*

    (Requires __EXTENDED_GLOB__ to be set.) Matches anything except the pattern *x*. This has a higher precedence than `__/__ ', so `__^foo/bar__ ' will search directories in `__.__ ' except `__./foo__ ' for a file named `__bar__ '.
*x*__~__*y*
    (Requires __EXTENDED_GLOB__ to be set.) Match anything that matches the pattern *x* but does not match *y*. This has lower precedence than any operator except `__|__ ', so `__*/*~foo/bar__ ' will search for all files in all directories in `__.__ ' and then exclude `__foo/bar__ ' if there was such a match. Multiple patterns can be excluded by `*foo*__~__*bar*__~__*baz* '. In the exclusion pattern (*y*), `__/__ ' and `__.__ ' are not treated specially the way they usually are in globbing.
*x*__#__
    (Requires __EXTENDED_GLOB__ to be set.) Matches zero or more occurrences of the pattern *x*. This operator has high precedence; `__12#__ ' is equivalent to `__1(2#)__ ', rather than `__(12)#__ '. It is an error for an unquoted `__#__ ' to follow something which cannot be repeated; this includes an empty string, a pattern already followed by `__##__ ', or parentheses when part of a __KSH_GLOB__ pattern (for example, `__!(__*foo*__)#__ ' is invalid and must be replaced by `__*(!(__*foo*__))__ ').
*x*__##__
    (Requires __EXTENDED_GLOB__ to be set.) Matches one or more occurrences of the pattern *x*. This operator has high precedence; `__12##__ ' is equivalent to `__1(2##)__ ', rather than `__(12)##__ '. No more than two active `__#__ ' characters may appear together. (Note the potential clash with glob qualifiers in the form `__1(2##)__ ' which should therefore be avoided.)
## ksh-like Glob Operators

If the __KSH_GLOB__ option is set, the effects of parentheses can be modified
by a preceding `__@__ ', `__*__ ', `__+__ ', `__?__ ' or `__!__ '. This
character need not be unquoted to have special effects, but the `__(__ ' must
be.

__@(__...__)__

    Match the pattern in the parentheses. (Like `__(__...__)__ '.)
__*(__...__)__

    Match any number of occurrences. (Like `__(__...__)#__ ', except that recursive directory searching is not supported.)
__+(__...__)__

    Match at least one occurrence. (Like `__(__...__)##__ ', except that recursive directory searching is not supported.)
__?(__...__)__

    Match zero or one occurrence. (Like `__(|__...__)__ '.)
__!(__...__)__

    Match anything but the expression in parentheses. (Like `__(^(__...__))__ '.)
## Precedence

The precedence of the operators given above is (highest) `__^__ ', `__/__ ',
`__~__ ', `__|__ ' (lowest); the remaining operators are simply treated from
left to right as part of a string, with `__#__ ' and `__##__ ' applying to the
shortest possible preceding unit (i.e. a character, `__?__ ', `__[__...__]__
', `__<__...__>__ ', or a parenthesised expression). As mentioned above, a
`__/__ ' used as a directory separator may not appear inside parentheses,
while a `__|__ ' must do so; in patterns used in other contexts than filename
generation (for example, in __case__ statements and tests within
`__[[__...__]]__ '), a `__/__ ' is not special; and `__/__ ' is also not
special after a `__~__ ' appearing outside parentheses in a filename pattern.

## Globbing Flags

There are various flags which affect any text to their right up to the end of
the enclosing group or to the end of the pattern; they require the
__EXTENDED_GLOB__ option. All take the form __(#__*X*__)__ where *X* may have
one of the following forms:

__i__

    Case insensitive: upper or lower case characters in the pattern match upper or lower case characters.
__l__

    Lower case characters in the pattern match upper or lower case characters; upper case characters in the pattern still only match upper case characters.
__I__

    Case sensitive: locally negates the effect of __i__ or __l__ from that point on.
__b__

    Activate backreferences for parenthesised groups in the pattern; this does not work in filename generation. When a pattern with a set of active parentheses is matched, the strings matched by the groups are stored in the array __$match__ , the indices of the beginning of the matched parentheses in the array __$mbegin__ , and the indices of the end in the array __$mend__ , with the first element of each array corresponding to the first parenthesised group, and so on. These arrays are not otherwise special to the shell. The indices use the same convention as does parameter substitution, so that elements of __$mend__ and __$mbegin__ may be used in subscripts; the __KSH_ARRAYS__ option is respected. Sets of globbing flags are not considered parenthesised groups; only the first nine active parentheses can be referenced.
For example,

[code]

    __foo= "a_string_with_a_message"__
    __if [[ $foo = (a|an)_(#b)(*) ]]; then__
      
    
    __print ${foo[$mbegin[1],$mend[1]]}__
    __fi__
[/code]

prints `__string_with_a_message__ '. Note that the first set of parentheses is
before the __(#b)__ and does not create a backreference.

Backreferences work with all forms of pattern matching other than filename
generation, but note that when performing matches on an entire array, such as
__${__*array*__#__*pattern*__}__ , or a global substitution, such as
__${__*param*__//__*pat*__/__*repl*__}__ , only the data for the last match
remains available. In the case of global replacements this may still be
useful. See the example for the __m__ flag below.

The numbering of backreferences strictly follows the order of the opening
parentheses from left to right in the pattern string, although sets of
parentheses may be nested. There are special rules for parentheses followed by
`__#__ ' or `__##__ '. Only the last match of the parenthesis is remembered:
for example, in `__[[ abab = (#b)([ab])# ]]__ ', only the final `__b__ ' is
stored in __match[1]__. Thus extra parentheses may be necessary to match the
complete segment: for example, use `__X((ab|cd)#)Y__ ' to match a whole string
of either `__ab__ ' or `__cd__ ' between `__X__ ' and `__Y__ ', using the
value of __$match[1]__ rather than __$match[2]__.

If the match fails none of the parameters is altered, so in some cases it may
be necessary to initialise them beforehand. If some of the backreferences fail
to match -- which happens if they are in an alternate branch which fails to
match, or if they are followed by __#__ and matched zero times -- then the
matched string is set to the empty string, and the start and end indices are
set to -1.

Pattern matching with backreferences is slightly slower than without.

__B__

    Deactivate backreferences, negating the effect of the __b__ flag from that point on.
__c__ *N*__,__*M*

    The flag __(#c__ *N*__,__*M*__)__ can be used anywhere that the __#__ or __##__ operators can be used except in the expressions `__(*/)#__ ' and `__(*/)##__ ' in filename generation, where `__/__ ' has special meaning; it cannot be combined with other globbing flags and a bad pattern error occurs if it is misplaced. It is equivalent to the form __{__*N*__,__*M*__}__ in regular expressions. The previous character or group is required to match between *N* and *M* times, inclusive. The form __(#c__ *N*__)__ requires exactly __N__ matches; __(#c,__*M*__)__ is equivalent to specifying *N* as 0; __(#c__ *N*__,)__ specifies that there is no maximum limit on the number of matches.
__m__

    Set references to the match data for the entire string matched; this is similar to backreferencing and does not work in filename generation. The flag must be in effect at the end of the pattern, i.e. not local to a group. The parameters __$MATCH__ , __$MBEGIN__ and __$MEND__ will be set to the string matched and to the indices of the beginning and end of the string, respectively. This is most useful in parameter substitutions, as otherwise the string matched is obvious.
For example,

[code]

    __arr=(veldt jynx grimps waqf zho buck)__
    __print ${arr//(#m)[aeiou]/${(U)MATCH}}__
[/code]

forces all the matches (i.e. all vowels) into uppercase, printing `__vEldt
jynx grImps wAqf zhO bUck__ '.

Unlike backreferences, there is no speed penalty for using match references,
other than the extra substitutions required for the replacement strings in
cases such as the example shown.

__M__

    Deactivate the __m__ flag, hence no references to match data will be created.
__a__ *num*

    Approximate matching: *num* errors are allowed in the string matched by the pattern. The rules for this are described in the next subsection.
__s__ , __e__

    Unlike the other flags, these have only a local effect, and each must appear on its own: `__(#s)__ ' and `__(#e)__ ' are the only valid forms. The `__(#s)__ ' flag succeeds only at the start of the test string, and the `__(#e)__ ' flag succeeds only at the end of the test string; they correspond to `__^__ ' and `__$__ ' in standard regular expressions. They are useful for matching path segments in patterns other than those in filename generation (where path segments are in any case treated separately). For example, `__*((#s)|/)test((#e)|/)*__ ' matches a path segment `__test__ ' in any of the following strings: __test__ , __test/at/start__ , __at/end/test__ , __in/test/middle__.
Another use is in parameter substitution; for example
`__${array/(#s)A*Z(#e)}__ ' will remove only elements of an array which match
the complete pattern `__A*Z__ '. There are other ways of performing many
operations of this type, however the combination of the substitution
operations `__/__ ' and `__//__ ' with the `__(#s)__ ' and `__(#e)__ ' flags
provides a single simple and memorable method.

Note that assertions of the form `__(^(#s))__ ' also work, i.e. match anywhere
except at the start of the string, although this actually means `anything
except a zero-length portion at the start of the string'; you need to use `__(
""~(#s))__' to match a zero-length portion of the string not at the start.

__q__

    A `__q__ ' and everything up to the closing parenthesis of the globbing flags are ignored by the pattern matching code. This is intended to support the use of glob qualifiers, see below. The result is that the pattern `__(#b)(*).c(#q.)__ ' can be used both for globbing and for matching against a string. In the former case, the `__(#q.)__ ' will be treated as a glob qualifier and the `__(#b)__ ' will not be useful, while in the latter case the `__(#b)__ ' is useful for backreferences and the `__(#q.)__ ' will be ignored. Note that colon modifiers in the glob qualifiers are also not applied in ordinary pattern matching.
__u__

    Respect the current locale in determining the presence of multibyte characters in a pattern, provided the shell was compiled with __MULTIBYTE_SUPPORT__. This overrides the __MULTIBYTE__ option; the default behaviour is taken from the option. Compare __U__. (Mnemonic: typically multibyte characters are from Unicode in the UTF-8 encoding, although any extension of ASCII supported by the system library may be used.)
__U__

    All characters are considered to be a single byte long. The opposite of __u__. This overrides the __MULTIBYTE__ option.
For example, the test string __fooxx__ can be matched by the pattern
__(#i____)FOOXX__ , but not by __(#l____)FOOXX__ ,
__(#i____)FOO____(#I____)XX__ or __((#i____)FOOX____)X__. The string
__(#ia2____)readme__ specifies case-insensitive matching of __readme__ with up
to two errors.

When using the ksh syntax for grouping both __KSH_GLOB__ and __EXTENDED_GLOB__
must be set and the left parenthesis should be preceded by __@__. Note also
that the flags do not affect letters inside __[__...__]__ groups, in other
words __(#i____)[a-z]__ still matches only lowercase letters. Finally, note
that when examining whole paths case-insensitively every directory must be
searched for all files which match, so that a pattern of the form
__(#i____)/foo/bar/...__ is potentially slow.

## Approximate Matching

When matching approximately, the shell keeps a count of the errors found,
which cannot exceed the number specified in the __(#a__ *num*__)__ flags. Four
types of error are recognised:

1.

    Different characters, as in __fooxbar__ and __fooybar__.
2.

    Transposition of characters, as in __banana__ and __abnana__.
3.

    A character missing in the target string, as with the pattern __road__ and target string __rod__.
4.

    An extra character appearing in the target string, as with __stove__ and __strove__.
Thus, the pattern __(#a3____)abcd__ matches __dcba__ , with the errors
occurring by using the first rule twice and the second once, grouping the
string as __[d][cb][a]__ and __[a][bc][d]__.

Non-literal parts of the pattern must match exactly, including characters in
character ranges: hence __(#a1____)???__ matches strings of length four, by
applying rule 4 to an empty part of the pattern, but not strings of length
two, since all the __?__ must match. Other characters which must match exactly
are initial dots in filenames (unless the __GLOB_DOTS__ option is set), and
all slashes in filenames, so that __a/bc__ is two errors from __ab/c__ (the
slash cannot be transposed with another character). Similarly, errors are
counted separately for non-contiguous strings in the pattern, so that
__(ab|cd____)ef__ is two errors from __aebf__.

When using exclusion via the __~__ operator, approximate matching is treated
entirely separately for the excluded part and must be activated separately.
Thus, __(#a1____)README~READ_ME__ matches __READ.ME__ but not __READ_ME__ , as
the trailing __READ_ME__ is matched without approximation. However,
__(#a1____)README~(#a1____)READ_ME__ does not match any pattern of the form
__READ__ *?*__ME__ as all such forms are now excluded.

Apart from exclusions, there is only one overall error count; however, the
maximum errors allowed may be altered locally, and this can be delimited by
grouping. For example, __(#a1____)cat____((#a0____)dog____)fox__ allows one
error in total, which may not occur in the __dog__ section, and the pattern
__(#a1____)cat____(#a0____)dog____(#a1____)fox__ is equivalent. Note that the
point at which an error is first found is the crucial one for establishing
whether to use approximation; for example, __(#a1)abc(#a0)xyz__ will not match
__abcdxyz__ , because the error occurs at the `__x__ ', where approximation is
turned off.

Entire path segments may be matched approximately, so that
`__(#a1)/foo/d/is/available/at/the/bar__ ' allows one error in any path
segment. This is much less efficient than without the __(#a1)__ , however,
since every directory in the path must be scanned for a possible approximate
match. It is best to place the __(#a1)__ after any path segments which are
known to be correct.

## Recursive Globbing

A pathname component of the form `__(__*foo*__/)#__ ' matches a path
consisting of zero or more directories matching the pattern *foo*.

As a shorthand, `__**/__ ' is equivalent to `__(*/)#__ '; note that this
therefore matches files in the current directory as well as subdirectories.
Thus:

[code]

    __ls -ld -- (*/)#bar__
[/code]

or

[code]

    __ls -ld -- **/bar__
[/code]

does a recursive directory search for files named `__bar__ ' (potentially
including the file `__bar__ ' in the current directory). This form does not
follow symbolic links; the alternative form `__***/__ ' does, but is otherwise
identical. Neither of these can be combined with other forms of globbing
within the same path segment; in that case, the `__*__ ' operators revert to
their usual effect.

Even shorter forms are available when the option __GLOB_STAR_SHORT__ is set.
In that case if no __/__ immediately follows a __**__ or __***__ they are
treated as if both a __/__ plus a further __*__ are present. Hence:

[code]

    __setopt GLOBSTARSHORT__
    __ls -ld -- **.c__
[/code]

is equivalent to

[code]

    __ls -ld -- **/*.c__
[/code]

## Glob Qualifiers

Patterns used for filename generation may end in a list of qualifiers enclosed
in parentheses. The qualifiers specify which filenames that otherwise match
the given pattern will be inserted in the argument list.

If the option __BARE_GLOB_QUAL__ is set, then a trailing set of parentheses
containing no `__|__ ' or `__(__ ' characters (or `__~__ ' if it is special)
is taken as a set of glob qualifiers. A glob subexpression that would normally
be taken as glob qualifiers, for example `__(^x)__ ', can be forced to be
treated as part of the glob pattern by doubling the parentheses, in this case
producing `__((^x))__ '.

If the option __EXTENDED_GLOB__ is set, a different syntax for glob qualifiers
is available, namely `__(#q__ *x*__)__ ' where *x* is any of the same glob
qualifiers used in the other format. The qualifiers must still appear at the
end of the pattern. However, with this syntax multiple glob qualifiers may be
chained together. They are treated as a logical AND of the individual sets of
flags. Also, as the syntax is unambiguous, the expression will be treated as
glob qualifiers just as long any parentheses contained within it are balanced;
appearance of `__|__ ', `__(__ ' or `__~__ ' does not negate the effect. Note
that qualifiers will be recognised in this form even if a bare glob qualifier
exists at the end of the pattern, for example `__*(#q*)(.)__ ' will recognise
executable regular files if both options are set; however, mixed syntax should
probably be avoided for the sake of clarity. Note that within conditions using
the `__[[__ ' form the presence of a parenthesised expression __(#q__
*...*__)__ at the end of a string indicates that globbing should be performed;
the expression may include glob qualifiers, but it is also valid if it is
simply __(#q)__. This does not apply to the right hand side of pattern match
operators as the syntax already has special significance.

A qualifier may be any one of the following:

__/__

    directories
__F__

    `full' (i.e. non-empty) directories. Note that the opposite sense __(^F____)__ expands to empty directories and all non-directories. Use __(/^F____)__ for empty directories.
__.__

    plain files
__@__

    symbolic links
__=__

    sockets
__p__

    named pipes (FIFOs)
__*__

    executable plain files (0100 or 0010 or 0001)
__%__

    device files (character or block special)
__%b__

    block special files
__%c__

    character special files
__r__

    owner-readable files (0400)
__w__

    owner-writable files (0200)
__x__

    owner-executable files (0100)
__A__

    group-readable files (0040)
__I__

    group-writable files (0020)
__E__

    group-executable files (0010)
__R__

    world-readable files (0004)
__W__

    world-writable files (0002)
__X__

    world-executable files (0001)
__s__

    setuid files (04000)
__S__

    setgid files (02000)
__t__

    files with the sticky bit (01000)
__f__ *spec*

    files with access rights matching *spec*. This *spec* may be a octal number optionally preceded by a `__=__ ', a `__+__ ', or a `__-__ '. If none of these characters is given, the behavior is the same as for `__=__ '. The octal number describes the mode bits to be expected, if combined with a `__=__ ', the value given must match the file-modes exactly, with a `__+__ ', at least the bits in the given number must be set in the file-modes, and with a `__-__ ', the bits in the number must not be set. Giving a `__?__ ' instead of a octal digit anywhere in the number ensures that the corresponding bits in the file-modes are not checked, this is only useful in combination with `__=__ '.
If the qualifier `__f__ ' is followed by any other character anything up to
the next matching character (`__[__ ', `__{__ ', and `__<__ ' match `__]__ ',
`__}__ ', and `__>__ ' respectively, any other character matches itself) is
taken as a list of comma-separated *sub-spec* s. Each *sub-spec* may be either
an octal number as described above or a list of any of the characters `__u__
', `__g__ ', `__o__ ', and `__a__ ', followed by a `__=__ ', a `__+__ ', or a
`__-__ ', followed by a list of any of the characters `__r__ ', `__w__ ',
`__x__ ', `__s__ ', and `__t__ ', or an octal digit. The first list of
characters specify which access rights are to be checked. If a `__u__ ' is
given, those for the owner of the file are used, if a `__g__ ' is given, those
of the group are checked, a `__o__ ' means to test those of other users, and
the `__a__ ' says to test all three groups. The `__=__ ', `__+__ ', and `__-__
' again says how the modes are to be checked and have the same meaning as
described for the first form above. The second list of characters finally says
which access rights are to be expected: `__r__ ' for read access, `__w__ ' for
write access, `__x__ ' for the right to execute the file (or to search a
directory), `__s__ ' for the setuid and setgid bits, and `__t__ ' for the
sticky bit.

Thus, `__*(f70?)__ ' gives the files for which the owner has read, write, and
execute permission, and for which other group members have no rights,
independent of the permissions for other users. The pattern `__*(f-100)__ '
gives all files for which the owner does not have execute permission, and
`__*(f:gu+w,o-rx:)__ ' gives the files for which the owner and the other
members of the group have at least write permission, and for which other users
don't have read or execute permission.

__e__ *string*

    
__+__*cmd*

    The *string* will be executed as shell code. The filename will be included in the list if and only if the code returns a zero status (usually the status of the last command).
In the first form, the first character after the `__e__ ' will be used as a
separator and anything up to the next matching separator will be taken as the
*string* ; `__[__ ', `__{__ ', and `__<__ ' match `__]__ ', `__}__ ', and
`__>__ ', respectively, while any other character matches itself. Note that
expansions must be quoted in the *string* to prevent them from being expanded
before globbing is done. *string* is then executed as shell code. The string
__globqual__ is appended to the array __zsh_eval_context__ the duration of
execution.

During the execution of *string* the filename currently being tested is
available in the parameter __REPLY__ ; the parameter may be altered to a
string to be inserted into the list instead of the original filename. In
addition, the parameter __reply__ may be set to an array or a string, which
overrides the value of __REPLY__. If set to an array, the latter is inserted
into the command line word by word.

For example, suppose a directory contains a single file `__lonely__ '. Then
the expression `__*(e:'reply=(${REPLY}{1,2})':)__ ' will cause the words
`__lonely1__ ' and `__lonely2__ ' to be inserted into the command line. Note
the quoting of *string*.

The form __+__*cmd* has the same effect, but no delimiters appear around
*cmd*. Instead, *cmd* is taken as the longest sequence of characters following
the __+__ that are alphanumeric or underscore. Typically *cmd* will be the
name of a shell function that contains the appropriate test. For example,

[code]

    __nt() { [[ $REPLY -nt $NTREF ]] }__
    __NTREF=reffile__
    __ls -ld -- *(+nt)__
[/code]

lists all files in the directory that have been modified more recently than
__reffile__.

__d__ *dev*

    files on the device *dev*
__l__[__-__ |__+__]*ct*

    files having a link count less than *ct* (__-__), greater than *ct* (__+__), or equal to *ct*
__U__

    files owned by the effective user ID
__G__

    files owned by the effective group ID
__u__ *id*

    files owned by user ID *id* if that is a number. Otherwise, *id* specifies a user name: the character after the `__u__ ' will be taken as a separator and the string between it and the next matching separator will be taken as a user name. The starting separators `__[__ ', `__{__ ', and `__<__ ' match the final separators `__]__ ', `__}__ ', and `__>__ ', respectively; any other character matches itself. The selected files are those owned by this user. For example, `__u:foo:__ ' or `__u[foo]__ ' selects files owned by user `__foo__ '.
__g__ *id*

    like __u__ *id* but with group IDs or names
__a__[__Mwhms__][__-__ |__+__]*n*

    files accessed exactly *n* days ago. Files accessed within the last *n* days are selected using a negative value for *n* (__-__*n*). Files accessed more than *n* days ago are selected by a positive *n* value (__+__*n*). Optional unit specifiers `__M__ ', `__w__ ', `__h__ ', `__m__ ' or `__s__ ' (e.g. `__ah5__ ') cause the check to be performed with months (of 30 days), weeks, hours, minutes or seconds instead of days, respectively. An explicit `__d__ ' for days is also allowed.
Any fractional part of the difference between the access time and the current
part in the appropriate units is ignored in the comparison. For instance,
`__echo *(ah-5)__ ' would echo files accessed within the last five hours,
while `__echo *(ah+5)__ ' would echo files accessed at least six hours ago, as
times strictly between five and six hours are treated as five hours.

__m__[__Mwhms__][__-__ |__+__]*n*

    like the file access qualifier, except that it uses the file modification time.
__c__[__Mwhms__][__-__ |__+__]*n*

    like the file access qualifier, except that it uses the file inode change time.
__L__[__+__ |__-__]*n*

    files less than *n* bytes (__-__), more than *n* bytes (__+__), or exactly *n* bytes in length.
If this flag is directly followed by a *size specifier* `__k__ ' (`__K__ '),
`__m__ ' (`__M__ '), or `__p__ ' (`__P__ ') (e.g. `__Lk-50__ ') the check is
performed with kilobytes, megabytes, or blocks (of 512 bytes) instead. (On
some systems additional specifiers are available for gigabytes, `__g__ ' or
`__G__ ', and terabytes, `__t__ ' or `__T__ '.) If a size specifier is used a
file is regarded as "exactly" the size if the file size rounded up to the next
unit is equal to the test size. Hence `__*(Lm1)__ ' matches files from 1 byte
up to 1 Megabyte inclusive. Note also that the set of files "less than" the
test size only includes files that would not match the equality test; hence
`__*(Lm-1)__ ' only matches files of zero size.

__^__

    negates all qualifiers following it
__-__

    toggles between making the qualifiers work on symbolic links (the default) and the files they point to, if any; any symbolic link for whose target the `__stat__ ' system call fails (whatever the cause of the failure) is treated as a file in its own right
__M__

    sets the __MARK_DIRS__ option for the current pattern
__T__

    appends a trailing qualifier mark to the filenames, analogous to the __LIST_TYPES__ option, for the current pattern (overrides __M__)
__N__

    sets the __NULL_GLOB__ option for the current pattern
__D__

    sets the __GLOB_DOTS__ option for the current pattern
__n__

    sets the __NUMERIC_GLOB_SORT__ option for the current pattern
__Y__ *n*

    enables short-circuit mode: the pattern will expand to at most *n* filenames. If more than *n* matches exist, only the first *n* matches in directory traversal order will be considered.
Implies __oN__ when no __o__ *c* qualifier is used.

__o__ *c*

    specifies how the names of the files should be sorted. The following values of *c* sort in the following ways:
__n__

    By name.
__L__

    By the size (length) of the files.
__l__

    By number of links.
__a__

    By time of last access, youngest first.
__m__

    By time of last modification, youngest first.
__c__

    By time of last inode change, youngest first.
__d__

    By directories: files in subdirectories appear before those in the current directory at each level of the search -- this is best combined with other criteria, for example `__odon__ ' to sort on names for files within the same directory.
__N__

    No sorting is performed.
__e__ *string*

    
__+__*cmd*

    Sort by shell code (see below).
Note that the modifiers __^__ and __-__ are used, so `__*(^-oL)__ ' gives a
list of all files sorted by file size in descending order, following any
symbolic links. Unless __oN__ is used, multiple order specifiers may occur to
resolve ties.

The default sorting is __n__ (by name) unless the __Y__ glob qualifier is
used, in which case it is __N__ (unsorted).

__oe__ and __o+__ are special cases; they are each followed by shell code,
delimited as for the __e__ glob qualifier and the __+__ glob qualifier
respectively (see above). The code is executed for each matched file with the
parameter __REPLY__ set to the name of the file on entry and __globsort__
appended to __zsh_eval_context__. The code should modify the parameter
__REPLY__ in some fashion. On return, the value of the parameter is used
instead of the file name as the string on which to sort. Unlike other sort
operators, __oe__ and __o+__ may be repeated, but note that the maximum number
of sort operators of any kind that may appear in any glob expression is 12.

__O__ *c*

    like `__o__ ', but sorts in descending order; i.e. `__*(^o__ *c*__)__ ' is the same as `__*(O__ *c*__)__ ' and `__*(^O__ *c*__)__ ' is the same as `__*(o__ *c*__)__ '; `__Od__ ' puts files in the current directory before those in subdirectories at each level of the search.
__[__*beg*[__,__*end*]__]__

    specifies which of the matched filenames should be included in the returned list. The syntax is the same as for array subscripts. *beg* and the optional *end* may be mathematical expressions. As in parameter subscripting they may be negative to make them count from the last match backward. E.g.: `__*(-OL[1,3])__ ' gives a list of the names of the three largest files.
__P__ *string*

    The *string* will be prepended to each glob match as a separate word. *string* is delimited in the same way as arguments to the __e__ glob qualifier described above. The qualifier can be repeated; the words are prepended separately so that the resulting command line contains the words in the same order they were given in the list of glob qualifiers.
A typical use for this is to prepend an option before all occurrences of a
file name; for example, the pattern `__*(P:-f:)__ ' produces the command line
arguments `__-f__ *file1* __-f__ *file2* ...'

If the modifier __^__ is active, then *string* will be appended instead of
prepended. Prepending and appending is done independently so both can be used
on the same glob expression; for example by writing
`__*(P:foo:^P:bar:^P:baz:)__ ' which produces the command line arguments
`__foo__ __baz__ *file1* __bar__ ...'

More than one of these lists can be combined, separated by commas. The whole
list matches if at least one of the sublists matches (they are `or'ed, the
qualifiers in the sublists are `and'ed). Some qualifiers, however, affect all
matches generated, independent of the sublist in which they are given. These
are the qualifiers `__M__ ', `__T__ ', `__N__ ', `__D__ ', `__n__ ', `__o__ ',
`__O__ ' and the subscripts given in brackets (`__[__*...*__]__ ').

If a `__:__ ' appears in a qualifier list, the remainder of the expression in
parenthesis is interpreted as a modifier (see the section `Modifiers' in the
section `History Expansion'). Each modifier must be introduced by a separate
`__:__ '. Note also that the result after modification does not have to be an
existing file. The name of any existing file can be followed by a modifier of
the form `__(:__*...*__)__ ' even if no actual filename generation is
performed, although note that the presence of the parentheses causes the
entire expression to be subjected to any global pattern matching options such
as __NULL_GLOB__. Thus:

[code]

    __ls -ld -- *(-/)__
[/code]

lists all directories and symbolic links that point to directories, and

[code]

    __ls -ld -- *(-@)__
[/code]

lists all broken symbolic links, and

[code]

    __ls -ld -- *(%W)__
[/code]

lists all world-writable device files in the current directory, and

[code]

    __ls -ld -- *(W,X)__
[/code]

lists all files in the current directory that are world-writable or world-
executable, and

[code]

    __print -rC1 /tmp/foo*(u0^@:t)__
[/code]

outputs the basename of all root-owned files beginning with the string
`__foo__ ' in __/tmp__ , ignoring symlinks, and

[code]

    __ls -ld -- *.*~(lex|parse).[ch](^D^l1)__
[/code]

lists all files having a link count of one whose names contain a dot (but not
those starting with a dot, since __GLOB_DOTS__ is explicitly switched off)
except for __lex.c__ , __lex.h__ , __parse.c__ and __parse.h__.

[code]

    __print -rC1 b*.pro(#q:s/pro/shmo/)(#q.:s/builtin/shmiltin/)__
[/code]

demonstrates how colon modifiers and other qualifiers may be chained together.
The ordinary qualifier `__.__ ' is applied first, then the colon modifiers in
order from left to right. So if __EXTENDED_GLOB__ is set and the base pattern
matches the regular file __builtin.pro__ , the shell will print
`__shmiltin.shmo__ '.

May 14, 2022 | zsh 5.9  
---|---

