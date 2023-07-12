# DRS-filer

[![License][badge-license]][badge-url-license]
[![Build_status][badge-build-status]][badge-url-build-status]
[![Coverage][badge-coverage]][badge-url-coverage]

## Synopsis

Microservice implementing the [Global Alliance for Genomics and
Health][org-ga4gh] (GA4GH) [Data Repository Service][res-ga4gh-drs] (DRS)
API specification.


## Description


## Deployment

### Preliminary setup

(1) Create a Python environment (as a virtual environment, via Conda, etc) and install the server application and its dependencies. From the root of the repo, run:
```bash
pip install -r requirements.txt
pip install -e . -v
```

(2) Create a public and a private key for the server:
```bash
crypt4gh-keygen --sk server-sk.key --pk server-pk.key
```
### Via Docker

1. Build the container 
```bash
docker build . -t crypt
```

2. Run the container
```bash
docker run \
  -e MONGO_DBNAME=drsstore \
  -e MONGO_HOST=localhost \
  -e MONGO_USERNAME=admin \
  -e MONGO_PASSWORD=password123 \
  -e ACCESS_KEY=123 \
  -e SECRET_KEY=456 \
  -e STORAGE_BUCKET=mybucket \
  -e STORAGE_SECURE=false
  crypt
```

### Via Kubernetes

To deploy into an existing kubernetes cluster, the cluster will require some dependencies to already be installed such as the nginx ingress, cert-manager and mongodb community operator.

1. Ensure docker registry secret exists (you can create the token in via dockerhub):
```bash
kubectl create secret docker-registry dockerhub --docker-username=%username% --docker-password=%token%
```

2. Ensure the mongodb pass exists
```bash
kubectl create secret generic pa-drs-crypt4gh-poc-secrets \
  --from-literal=MONGOPASS=password123 \
  --from-literal=ACCESS_KEY=password123 \
  --from-literal=SECRET_KEY=password123
```

3. Install this helm chart:
```bash
cd deployment
helm 
helm upgrade -i crypt4gh-poc .
```

### Via docker-compose

Prerequisites: you should have [Docker](https://www.docker.com/) installed, as well as the [Minio client](https://min.io/docs/minio/linux/reference/minio-mc.html).

(1) Before bringing up the service for the first time, create a data directory for
MongoDB to store its configuration and local data:
```bash
mkdir -p ../data/drs/db/
```

(2) Create a file `.env` in the root of the repository containing the username and password for the Minio root account and for a Minio service account. An example such file is given below:
```bash
MINIO_ROOT_USER=miniorootuser
MINIO_ROOT_PASSWORD=miniorootpassword
ACCESS_KEY=miniolocaluser
SECRET_KEY=miniolocaluserpwd123
```

(3) Bring up the service by running, from the root of the repository,
```bash
docker compose up
```

(4) Provision Minio by setting up a bucket to hold encrypted files and a user account that can be used to upload to it:
```bash
./configure-minio.sh
```

(5) Add an entry to `/etc/hosts` so that the Minio service can be accessed using the `minio` hostname. As root, open the file `/etc/hosts`, and add the following line at the bottom:
```
127.0.0.1    minio
```

The server runs on `localhost:8080` by default. The OpenAPI interface can be
accessed at
[http://localhost:8080/ga4gh/drs/v1/ui/](http://localhost:8080/ga4gh/drs/v1/ui/). The Minio dashboad can be found at [http://localhost:9000](http://localhost:9000) and can be accessed using the root user account configured in step (2). After step (5) has been completed, the Minio service can also be accessed at [http://minio:9000](http://minio:9000).


## Local development

The source code repository is mounted as a volume inside the Docker container for the server. That means that you can edit the code in this repo, and the server will automatically restart when any changes are detected. There is no need to rebuild or even restart the Docker container.

To run the unit tests, it is necessary to activate the Python environment set up above. To run the unit test suite, run the following command:
```bash
pytest tests
```

If `pytest` cannot be found, install the testing requirements via `pip install
-r requirements-test.txt`.

The unit test suite does not require the server to be running.

## Running the integration tests

The server comes with a number of basic integration or "smoke" tests that test basic end-to-end functionality of the entire server stack. The goal is not to exhaustively test the server and make manual QA superfluous, but rather to detect simple breakage that cannot be detected at the level of the unit tests early on.

Currently the following scenarios are tested:

1. Querying the service-info endpoint and comparing the output with what is expected.

To run the integration test suite, bring up the server as described above, and then run (from within the development environment):
```bash
pytest integration
```

The integration test suite is automatically run under GitHub actions as well, for every PR.

## Configuring the server

The file `config.yaml` in the `drs_filer` can be used to set various configuration options for the server. The Crypt4GH-related options and some others can also be passed in as environment variables. Currently the following options are supported:

- `PUBKEY_PATH`: The path to the public key used by the server. This must be a file path relative to the container.
- `SECKEY_PATH`: The path to the public key used by the server. This must be a file path relative to the container.
- `STORAGE_HOST`: The FQDN of the storage host (e.g. `s3.eu-west-1.amazonaws.com` for AWS or `localhost:9000` for Minio).
- `STORAGE_BUCKET`: The name of the bucket.
- `STORAGE_SECURE`: Whether or not to check the TLS certificate of the storage host.

Note that the server must have the following environment variables set as well, as detailed above:

- `ACCESS_KEY`: Access key ID providing access to the storage bucket.
- `SECRET_KEY`: Secret access key providing access to the storage bucket.


## Contributing

This project is a community effort and lives off your contributions, be it in
the form of bug reports, feature requests, discussions, or fixes and other code
changes. Please refer to our organization's [contributing
guidelines][res-elixir-cloud-contributing] if you are interested to contribute.
Please mind the [code of conduct][res-elixir-cloud-coc] for all interactions
with the community.

## Versioning

The project adopts the [semantic versioning][res-semver] scheme for versioning.
Currently the service is in beta stage, so the API may change without further
notice.

## License

This project is covered by the [Apache License 2.0][license-apache] also
[shipped with this repository][license].

## Contact

The project is a collaborative effort under the umbrella of [ELIXIR Cloud &
AAI][org-elixir-cloud]. Follow the link to get in touch with us via chat or
email. Please mention the name of this service for any inquiry, proposal,
question etc.

[badge-build-status]:<https://travis-ci.com/elixir-cloud-aai/drs-filer.svg?branch=dev>
[badge-coverage]:<https://img.shields.io/coveralls/github/elixir-cloud-aai/drs-filer>
[badge-github-tag]:<https://img.shields.io/github/v/tag/elixir-cloud-aai/drs-filer?color=C39BD3>
[badge-license]:<https://img.shields.io/badge/license-Apache%202.0-blue.svg>
[badge-url-build-status]:<https://travis-ci.com/elixir-cloud-aai/drs-filer>
[badge-url-coverage]:<https://coveralls.io/github/elixir-cloud-aai/drs-filer>
[badge-url-github-tag]:<https://github.com/elixir-cloud-aai/drs-filer/releases>
[badge-url-license]:<http://www.apache.org/licenses/LICENSE-2.0>
[license]: LICENSE
[license-apache]: <https://www.apache.org/licenses/LICENSE-2.0>
[org-elixir-cloud]: <https://github.com/elixir-cloud-aai/elixir-cloud-aai>
[org-ga4gh]: <https://www.ga4gh.org/>
[res-elixir-cloud-coc]: <https://github.com/elixir-cloud-aai/elixir-cloud-aai/blob/dev/CODE_OF_CONDUCT.md>
[res-elixir-cloud-contributing]: <https://github.com/elixir-cloud-aai/elixir-cloud-aai/blob/dev/CONTRIBUTING.md>
[res-semver]: <https://semver.org/>
[res-ga4gh-drs]: https://github.com/ga4gh/data-repository-service-schemas
