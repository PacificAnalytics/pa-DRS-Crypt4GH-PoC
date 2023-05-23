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
        cmd, check=True, shell=True, stdout=subprocess.PIPE, encoding="utf-8")
    return result.stdout


def _setup_environment():
    """Read  in the env.txt file in the integration test directory.
    """
    integration_testdir = os.path.dirname(__file__)
    with open(os.path.join(integration_testdir, "env.txt")) as fp:
        entries = [line.strip().split('=') for line in fp.readlines()]
    env = dict(entries)
    os.environ.update(env)


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

    _setup_environment()
    _touch("file.txt", "test file")

    # Upload file
    cmd = """drs-uploader --drs-url http://minio:8080 \
          --storage-url localhost:9000 \
          --bucket drs-crypt4gh --insecure file.txt"""
    id_ = _run_command(cmd).strip()[1:-1]
    _rm("file.txt")

    # Download file again
    cmd = f"drs get -d http://minio:8080 {id_}"
    _run_command(cmd)

    # Check that contents match
    assert _cat(os.path.join(id_, "file.txt")) == "test file"
