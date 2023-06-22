from pathlib import Path

from drs_filer.crypt4gh_support.utils import (
    create_unique_filename, temp_folder
)


def test_temp_folder():
    old_cwd = Path.cwd()
    with temp_folder() as d:
        assert Path.cwd() == old_cwd
        assert d.exists()
    assert not d.exists()


def test_create_unique_filename():
    p = Path("/a/b/c")
    f1 = create_unique_filename(p)
    assert f1.parent == p

    f2 = create_unique_filename(p)
    assert f2 != f1
