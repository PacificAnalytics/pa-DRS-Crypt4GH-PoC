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

## Encrypting the payload

DRS-uploader can upload the payload prior to uploading it to a Crypt4GH-enabled DRS server. To do this, add the `--encrypt` flag on the command line, and pass in the secret key for the client using the `--client-sk` flag:
```bash
drs-uploader \
    --drs-url http://localhost:8080 \
    --storage-url localhost:9000 \
    --bucket mybucket \
    --insecure \
    --encrypt \
    --client-sk client-sk.key \
    mydata.txt
```
Before uploading the payload to the server, the uploader client will fetch the public key of the server, and Crypt4GH-encrypt the payload with the server public key and the client private key. The encrypted payload is then uploaded to the server and registered in DRS-filer.


To create a public/private keypair, use the `crypt4gh-keygen` utility:
```bash
crypt4gh-keygen --sk client-sk.key --pk client-pk.key
```
Make sure to leave the pass phrase for the secret key empty.

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
