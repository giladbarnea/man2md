# FSCK_HFS(8)

## NAME

fsck_hfs – HFS file system consistency check

## SYNOPSIS

`fsck_hfs -q [-df] special ...`
`fsck_hfs -p [-df] special ...`
`fsck_hfs [-n | -y | -r] [-dfgxlES] [-D flags] [-b size] [-B path] [-m mode] [-c size] [-R flags] special ...`

## DESCRIPTION

The `fsck_hfs` utility verifies and repairs HFS+ file systems.

The first form of `fsck_hfs` quickly checks the specified file systems to determine whether they were cleanly unmounted.

The second form of `fsck_hfs` preens the specified file systems. It is normally started by `fsck(8)` run from `/etc/rc.boot` during automatic reboot, when a HFS file system is detected. When preening file systems, `fsck_hfs` will fix common inconsistencies for file systems that were not unmounted cleanly. If more serious problems are found, `fsck_hfs` does not try to fix them, indicates that it was not successful, and exits.

The third form of `fsck_hfs` checks the specified file systems and tries to repair all detected inconsistencies.

If no options are specified `fsck_hfs` will always check and attempt to fix the specified file systems.

The options are as follows:

**`-c size`**
Specify the size of the cache used by `fsck_hfs` internally. Bigger size can result in better performance but can result in deadlock when used with `-l` option. Size can be specified as a decimal, octal, or hexadecimal number. If the number ends with a `k`, `m`, or `g`, the number is multiplied by 1024 (1K), 1048576 (1M), or 1073741824 (1G), respectively.

**`-d`**
Display debugging information. This option may provide useful information when `fsck_hfs` cannot repair a damaged file system.

**`-D flags`**
Print extra debugging information. The flags are a bitmap that control which kind of debug information is printed. The following values are currently implemented:
    0x0001  Informational messages
    0x0002  Error messages
    0x0010  Extended attributes related messages
    0x0020  Overlapped extents related messages

**`-b size`**
Specify the size, in bytes, of the physical blocks used by the `-B` option.

**`-B path`**
Print the files containing the physical blocks listed in the file path. The file should contain one or more decimal, octal (with leading 0) or hexadecimal (with leading 0x) numbers separated by white space. The physical block numbers are relative to the start of the partition, so if you have block numbers relative to the start of the device, you will have to subtract the block number of the start of the partition. The size of a physical block is given with the `-b` option; the default is 512 bytes per block.

**`-f`**
When used with the `-p` option, force `fsck_hfs` to check `clean` file systems, otherwise it means force `fsck_hfs` to check and repair journaled HFS+ file systems.

**`-g`**
Causes `fsck_hfs` to generate its output strings in GUI format. This option is used when another application with a graphical user interface (like Mac OS X Disk Utility) is invoking the `fsck_hfs` tool.

**`-x`**
Causes `fsck_hfs` to generate its output strings in XML (plist) format. This option implies the `-g` option.

**`-l`**
Lock down the file system and perform a test-only check. This makes it possible to check a file system that is currently mounted, although no repairs can be made.

**`-m mode`**
Mode is an octal number that will be used to set the permissions for the lost+found directory when it is created. The lost+found directory is only created when a volume is repaired and orphaned files or directories are detected. `fsck_hfs` places orphaned files and directories into the lost+found directory (located at the root of the volume). The default mode is 01777.

**`-p`**
Preen the specified file systems.

**`-q`**
Causes `fsck_hfs` to quickly check whether the volume was unmounted cleanly. If the volume was unmounted cleanly, then the exit status is 0. If the volume was not unmounted cleanly, then the exit status will be non-zero. In either case, a message is printed to standard output describing whether the volume was clean or dirty.

**`-y`**
Always attempt to repair any damage that is found.

**`-n`**
Never attempt to repair any damage that is found.

**`-E`**
Cause `fsck_hfs` to exit (with a value of 47) if it encounters any major errors. A `major error` is considered one which would impact using the volume in normal usage; an inconsistency which would not impact such use is considered `minor` for this option. Only valid with the `-n` option.

**`-S`**
Cause `fsck_hfs` to scan the entire device looking for I/O errors. It will attempt to map the blocks with errors to names, similar to the `-B` option.

**`-R flags`**
Rebuilds the requested btree. The following flags are supported:
    a   Attribute btree
    c   Catalog btree
    e   Extents overflow btree
Rebuilding a btree will only work if there is enough free space on the file system for the new btree file, and if `fsck_hfs` is able to traverse each of the nodes in the requested btree successfully.

**`-r`**
Rebuild the catalog btree. This is synonymous with `-Rc`.

Because of inconsistencies between the block device and the buffer cache, the raw device should always be used.

## EXIT VALUES

`fsck_hfs` indicates some status by exit value. The current list of exit status results is:

**0**
No errors found, or successfully repaired.

**3**
A quick-check (the `-n` option) found a dirty filesystem; no repairs were made. There is a potential corruption in the filesystem, and either the journal could not be read, or a runtime corruption was present so the HFS Volume Inconsistent bit was set.

**4**
During boot, the root filesystem was found to be dirty; repairs were made, and the filesystem was remounted. The system should be rebooted.

**8**
A corrupt filesystem was found during a check, or repairs did not succeed.

**47**
A major error was found with `-E`.

## SEE ALSO

`fsck(8)`

## BUGS

`fsck_hfs` is not able to fix some inconsistencies that it detects.

## HISTORY

The `fsck_hfs` command appeared in Mac OS X Server 1.0 .