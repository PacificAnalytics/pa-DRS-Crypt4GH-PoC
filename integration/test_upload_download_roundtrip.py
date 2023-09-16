import functools
import os
import shutil
import subprocess
import tempfile


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
        cmd, check=True, capture_output=True, encoding="utf-8")
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

    # Write config file
    cmd = ["drs-client", "configure",
           "--access-key", os.environ['ACCESS_KEY'],
           "--secret-key", os.environ['SECRET_KEY'],
           "--drs-url", os.environ['DRS_HOST'],
           "--storage-url", os.environ['STORAGE_HOST'],
           "--bucket", os.environ['STORAGE_BUCKET']]
    _run_command(cmd)

    # Upload file
    cmd = ["drs-client", "upload", "--no-encrypt", "file.txt"]
    id_ = _run_command(cmd).strip()
    _rm("file.txt")

    # Download file again (note: this uses the GA4GH download client as our
    # drs-client doesn't support unencrypted downloads out of the box (yet)
    cmd = ["drs", "get",
           "--suppress-ssl-verify",
           "-d", os.environ['DRS_HOST'], id_]
    _run_command(cmd)

    # Check that contents match
    assert _cat(os.path.join(id_, "file.txt")) == "test file"
