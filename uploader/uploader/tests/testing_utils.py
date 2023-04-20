import contextlib
import pathlib
import shutil
import tempfile


@contextlib.contextmanager
def datafile(contents, fname="temp.txt"):
    try:
        d = pathlib.Path(tempfile.mkdtemp())
        path = d / fname
        with open(path, "wt") as fp:
            fp.write(contents)
        yield path
    finally:
        shutil.rmtree(d)
