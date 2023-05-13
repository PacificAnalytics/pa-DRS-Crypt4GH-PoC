# DRS-uploader

DRS-uploader is a simple command-line utility that can be used to upload file
data to a object storage server, and to register file metadata in DRS-filer.

## Example

Install the tool by running, in the same Python environment where DRS-filer was
installed,
```bash
pip install -e . -v
```

Set the following environment variables to provide access to the storage bucket:
```bash
export ACCESS_KEY=<your-bucket-access-key>
export SECRET_KEY=<your-bucket-secret-key>
```

To upload a given file `mydata.txt`, run
```bash
drs-uploader \
    --drs-url http://localhost:8080 \
    --storage-url localhost:9000 \
    --bucket mybucket \
    --insecure \
    mydata.txt
```

In the above, `--drs-url` refers to the base URL for DRS-filer, `--storage-url`
to the object storage, and `--bucket` to the name of the bucket to use. Note
that the bucket must exist.

Currently, DRS-uploader has been tested with Minio as the storage backend
only. It is expected, however, that S3 can be supported without major changes
to the code.

DRS-uploader will print a number of diagnostic messages while it runs, and it
will print the object ID on a line by itself when the upload finishes. This ID
can be used to retrieve the file and its metadata using the DRS client:
```
    drs get -d http://localhost:8080 <drs-ID>
```

## Running the tests

DRS-uploader uses Pytest as a testing framework. Before running the tests,
install the extra testing requirements:
```bash
pip install -r requirements-test.txt
```

Then, run Pytest as usual via
```bash
pytest .
```
