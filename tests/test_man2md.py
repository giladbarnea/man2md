import pytest
import subprocess
import sys
from pathlib import Path

def test_man2md_basic_structure():
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

def test_man2md_name_section():
    """Test NAME section conversion"""
    result = subprocess.run([
        sys.executable, 'man2md.py', 
        'tests/zshexpn/zshexpn-raw.txt'
    ], capture_output=True, text=True)
    
    assert result.returncode == 0
    output = result.stdout
    
    # Check NAME section content
    assert 'zshexpn - zsh expansion and substitution' in output

def test_man2md_description_section():
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