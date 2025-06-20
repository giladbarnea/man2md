#!/usr/bin/env bash
# Usage: scripts/create-test-suite.sh fsck_hfs
# Usage: scripts/create-test-suite.sh /usr/share/man/man8/fsck_hfs.8
set -euo pipefail

main() {
	[[ -d tests ]] || {
		echo "Error: tests/ dir not found. Make sure you're running this script from the root of the project."
		return 1
	}

	# Set an error trap to disable the `set -x` flag
	trap 'set +x' ERR

	local man_page_path="$1"
	if [[ ! -f "$man_page_path" ]]; then
		man_page_path="$(man -w "$man_page_path")"
	fi

	local man_page_name=${man_page_path##*/}
	man_page_name=${man_page_name%.*}
	set -x
	mkdir -p tests/"$man_page_name"
	cat "$man_page_path" >tests/"$man_page_name"/"$man_page_name"_raw.txt
	mandoc -T locale "$man_page_path" | col -b >tests/"$man_page_name"/"$man_page_name".txt
	mandoc -T tree "$man_page_path" >tests/"$man_page_name"/"$man_page_name"_tree.txt
	set +x
}

main "$@"
