import subprocess
import sys

def test_zshexpn_basic_structure():
    """Test that man2md produces basic markdown structure"""
    result = subprocess.run([
        sys.executable, 'man2md.py', 
        'tests/zshexpn/zshexpn-raw.txt'
    ], capture_output=True, text=True)
    
    assert result.returncode == 0
    output = result.stdout
    
    # Check for basic markdown headers
    assert '# ZSHEXPN(1)' in output
    assert '## NAME' in output
    assert '## DESCRIPTION' in output
    assert '## HISTORY EXPANSION' in output

def test_zshexpn_name_section():
    """Test NAME section conversion"""
    result = subprocess.run([
        sys.executable, 'man2md.py', 
        'tests/zshexpn/zshexpn-raw.txt'
    ], capture_output=True, text=True)
    
    assert result.returncode == 0
    output = result.stdout
    
    # Check NAME section content
    assert 'zshexpn - zsh expansion and substitution' in output

def test_zshexpn_description_section():
    """Test DESCRIPTION section conversion"""
    result = subprocess.run([
        sys.executable, 'man2md.py', 
        'tests/zshexpn/zshexpn-raw.txt'
    ], capture_output=True, text=True)
    
    assert result.returncode == 0
    output = result.stdout
    
    # Check for key content in DESCRIPTION
    assert 'The following types of expansions are performed' in output
    assert '**History Expansion**' in output
    assert '**Alias Expansion**' in output

# BSD-style man page tests (fsck_hfs)
def test_fsck_hfs_basic_structure():
    """Test that man2md produces basic markdown structure for BSD-style man pages"""
    result = subprocess.run([
        sys.executable, 'man2md.py', 
        'tests/fsck_hfs/fsck_hfs_raw.txt'
    ], capture_output=True, text=True)
    
    assert result.returncode == 0
    output = result.stdout
    
    # Check for basic markdown headers
    assert '# FSCK_HFS(8)' in output
    assert '## NAME' in output
    assert '## SYNOPSIS' in output
    assert '## DESCRIPTION' in output

def test_fsck_hfs_name_section():
    """Test NAME section conversion for BSD-style man pages"""
    result = subprocess.run([
        sys.executable, 'man2md.py', 
        'tests/fsck_hfs/fsck_hfs_raw.txt'
    ], capture_output=True, text=True)
    
    assert result.returncode == 0
    output = result.stdout
    
    # Check NAME section content
    assert 'fsck_hfs – HFS file system consistency check' in output

def test_fsck_hfs_description_section():
    """Test DESCRIPTION section conversion for BSD-style man pages"""
    result = subprocess.run([
        sys.executable, 'man2md.py', 
        'tests/fsck_hfs/fsck_hfs_raw.txt'
    ], capture_output=True, text=True)
    
    assert result.returncode == 0
    output = result.stdout
    
    # Check for key content in DESCRIPTION
    assert 'utility verifies and repairs HFS+ file systems' in output
    assert '`fsck_hfs`' in output

def test_fsck_hfs_synopsis_section():
    """Test SYNOPSIS section conversion for BSD-style man pages"""
    result = subprocess.run([
        sys.executable, 'man2md.py', 
        'tests/fsck_hfs/fsck_hfs_raw.txt'
    ], capture_output=True, text=True)
    
    assert result.returncode == 0
    output = result.stdout
    
    # Check for synopsis content (should have command syntax)
    assert '## SYNOPSIS' in output
    # Should contain some form of fsck_hfs command syntax
    synopsis_section = output.split('## SYNOPSIS')[1].split('## DESCRIPTION')[0]
    assert 'fsck_hfs' in synopsis_section or '`' in synopsis_section

# Regression tests to ensure both formats work
def test_both_formats_work():
    """Regression test to ensure both traditional and BSD man page formats work"""
    # Test zshexpn (traditional format)
    result_zsh = subprocess.run([
        sys.executable, 'man2md.py', 
        'tests/zshexpn/zshexpn-raw.txt'
    ], capture_output=True, text=True)
    
    # Test fsck_hfs (BSD format)  
    result_fsck = subprocess.run([
        sys.executable, 'man2md.py', 
        'tests/fsck_hfs/fsck_hfs_raw.txt'
    ], capture_output=True, text=True)
    
    # Both should succeed
    assert result_zsh.returncode == 0
    assert result_fsck.returncode == 0
    
    # Both should produce valid markdown with titles
    assert '# ZSHEXPN(1)' in result_zsh.stdout
    assert '# FSCK_HFS(8)' in result_fsck.stdout