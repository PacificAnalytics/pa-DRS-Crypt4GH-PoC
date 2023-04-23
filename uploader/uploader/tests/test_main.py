from ..main import main

from .testing_utils import datafile, patch_drs_filer, patch_minio


def test_main(cli_runner):

    with (patch_minio() as minio_client,
          patch_drs_filer("http://drs.url") as drs_client,
          datafile("foo") as path):

        # WHEN
        result = cli_runner.invoke(
            main, [
                "--drs-url", "http://drs.url",
                "--storage-url", "http://storage.url",
                "--bucket", "some-bucket",
                "--insecure",
                "--desc", "integration test object",
                str(path)
            ])

        # THEN, (a) check that command exited normally
        assert result.exit_code == 0

        # THEN, (b) check that bytes were uploaded
        minio_client.put_object.assert_called_once()
        call_args = minio_client.put_object.call_args
        assert call_args[0][0] == "some-bucket"
        assert call_args[0][1] == "temp.txt"

        # THEN, (c) check that metadata was registered
        assert drs_client.call_count == 1
        payload = drs_client.request_history[-1].json()
        assert payload["name"] == "temp.txt"
        assert payload["description"] == "integration test object"
