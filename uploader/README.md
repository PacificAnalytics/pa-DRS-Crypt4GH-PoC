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

## Setting up a Minio instance for local development/testing

Minio is an S3-compatible object storage system that can be easily set up via
Docker for isolated testing and development. To follow the instructions below,
it is assumed that you have installed the [Minio
client](https://min.io/docs/minio/linux/reference/minio-mc.html) (`mc`), and
that you have created a directory where objects will be stored. In what
follows, this directory will be referred to as `$DATADIR`. This must be an
absolute directory path.

(1) Start the Minio server via
```bash
export MINIO_ROOT_PASSWORD=myminiorootpwd
export MINIO_ROOT_USER=myminiorootuser

docker run \
   --rm \
   -p 9000:9000 \
   -p 9090:9090 \
   --name minio \
   -v $DATADIR:/data \
   -e "MINIO_ROOT_USER=$MINIO_ROOT_USER" \
   -e "MINIO_ROOT_PASSWORD=$MINIO_ROOT_PASSWORD" \
   quay.io/minio/minio server /data --console-address ":9090"
```
You can adjust the Minio root user and password as desired.

(2) Create a local alias for the deployment:
```bash
mc alias set local http://127.0.0.1:9000 $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD
```

(3) Create a bucket and configure it to allow anonymous downloads:
```bash
mc mb local/mybucket
mc anonymous set download local/mybucket
```

(4) Create a local user with upload privileges
```bash
mc admin user add local $ACCESS_KEY $SECRET_KEY
mc admin policy attach local readwrite --user $ACCESS_KEY

```

In the above, `$ACCESS_KEY` and `$SECRET_KEY` specify an access key (like a
username) and a secret key for the new user. If you have the `pwgen` utility
installed, you can generate appropriate values for these variables via
```bash
export SECRET_KEY=$(pwgen --secure --capitalize --numerals --ambiguous 30 -N 1)
export ACCESS_KEY=$(pwgen --secure --capitalize --numerals --ambiguous 30 -N 1)
```
