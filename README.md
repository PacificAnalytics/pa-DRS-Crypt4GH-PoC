# DRS-filer

[![License][badge-license]][badge-url-license]
[![Build_status][badge-build-status]][badge-url-build-status]
[![Coverage][badge-coverage]][badge-url-coverage]

## Synopsis

Microservice implementing the [Global Alliance for Genomics and
Health][org-ga4gh] (GA4GH) [Data Repository Service][res-ga4gh-drs] (DRS)
API specification.


## Description

## Building

To build locally and push to docker hub, complete the following steps (todo automate this):

```bash
docker login
docker build . -t pacificanalytics/pa-drs-crypt4gh-poc:x.x.x
docker push pacificanalytics/pa-drs-crypt4gh-poc:x.x.x
```

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

2. Ensure the mongodb pass exists (replace with real values)
```bash
kubectl create secret generic pa-drs-crypt4gh-poc-secrets \
  --from-literal=MONGOPASS=password123 \
  --from-literal=ACCESS_KEY=access-key \
  --from-literal=SECRET_KEY=secret-key \
  --from-literal=STORAGE_BUCKET=staging-pa-drs-crypt4gh-poc \
  --from-literal=STORAGE_HOST=s3.au-southeast-1.amazonaws.com \
  --from-file=PUB_KEY=key.pub \
  --from-file=SEC_KEY=key
```

3. Install this helm chart:
```bash
helm upgrade -i crypt4gh-poc deployment
```

### Via docker-compose

1. Run the following (edit to taste):

```bash
export MONGO_URI="mongodb://admin:password@db:27017/drsStore?authSource=admin"
export SEC_KEY="-----BEGIN CRYPT4GH PRIVATE KEY-----
YzRnaC12MQAEbm9uZQAEbm9uZQAg5eYgf1QUl1cFyquP6OgMz2faF2uSc4s8OXf0L4MLRQM=
-----END CRYPT4GH PRIVATE KEY-----"
export PUB_KEY="-----BEGIN CRYPT4GH PUBLIC KEY-----
dq/9iq2WMYpYQqnxVpfd0pwRp2PToAccVWldr+kynCI=
-----END CRYPT4GH PUBLIC KEY-----"
export STORAGE_HOST=s3.ap-southeast-2.amazonaws.com
export STORAGE_BUCKET=mybucket
export STORAGE_SECURE=true
export ACCESS_KEY=key
export SECRET_KEY=secret

docker-compose up --build
```

## Troubleshooting

Logs are sent to elasticsearch via fluentd or failing that you can access the logs directly using kubectl by completing the following steps:

1. Install awscli and ensure you have it authed with `aws configure`
2. Install kubectl and run the aws command the configures your kubectl to work with eks `aws eks update-kubeconfig --region ap-southeast-2 --name staging-pa-drs-kubernetes`
3. View the current pods running in the cluster `kubectl get pods`
4. View the logs for the pod you are interested, in our case it would be `kubectl logs -f pa-drs-crypt4gh-poc-684d56f666-c6z9c` (-f being follow which is similar to tail).

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
