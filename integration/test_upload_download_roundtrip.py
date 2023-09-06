import functools
import os
import shutil
import subprocess
import tempfile


# Grab storage configuration variables from the environment. Note: ACCESS_KEY
# and SECRET_KEY must also be set.
STORAGE_HOST = os.environ["STORAGE_HOST"]
STORAGE_BUCKET = os.environ["STORAGE_BUCKET"]


def _in_temp_dir(fn):
    """Run tests in a temporary directory.
    """
    @functools.wraps(fn)
    def wrapper(*args, **kwds):
        try:
            # Create temporary directory and cd into it
            tempdir = tempfile.mkdtemp()
            old_cwd = os.getcwd()
            os.chdir(tempdir)

            # Run original function
            return fn(*args, **kwds)
        finally:
            os.chdir(old_cwd)
            shutil.rmtree(tempdir)
    return wrapper


def _run_command(cmd):
    """Run command and return stdout.
    """
    result = subprocess.run(
        cmd, check=True, shell=True, capture_output=True, encoding="utf-8")
    return result.stdout


def _touch(fname, contents):
    with open(fname, "wt", encoding="utf-8") as fp:
        fp.write(contents)


def _cat(fname):
    with open(fname, encoding="utf-8") as fp:
        return fp.read()


def _rm(fname):
    os.unlink(fname)


@_in_temp_dir
def test_upload_download_roundtrip():

    _touch("file.txt", "test file")

    # Upload file
    cmd = f"""drs-uploader --drs-url http://localhost:8080 \
          --storage-url {STORAGE_HOST} \
          --bucket {STORAGE_BUCKET} file.txt"""
    id_ = _run_command(cmd).strip()[1:-1]
    _rm("file.txt")

    # Download file again
    cmd = f"drs get --suppress-ssl-verify -d http://localhost:8080 {id_}"
    _run_command(cmd)

    # Check that contents match
    assert _cat(os.path.join(id_, "file.txt")) == "test file"
