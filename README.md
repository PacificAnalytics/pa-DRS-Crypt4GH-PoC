# DRS-filer

[![License][badge-license]][badge-url-license]
[![Build_status][badge-build-status]][badge-url-build-status]
[![Coverage][badge-coverage]][badge-url-coverage]

## Synopsis

Microservice implementing the [Global Alliance for Genomics and
Health][org-ga4gh] (GA4GH) [Data Repository Service][res-ga4gh-drs] (DRS)
API specification.


## Description


## Local development

For development, it is recommend to run the service outside of Docker. This
provides an easier debugging and editing experience. Steps 1 through 3 below
need to be done only once.

(1) Create a Python environment and install both the dependencies and the
service itself:
```bash
pip install -r requirements.txt
pip install -e . -v
```

(2) Bring up a MongoDB instance, for example by running
```bash
docker run -it --rm -p 27017:27017 --name mongo -d mongo
```
Initialize the database by running
```bash
python tools/initialize-mongodb.py
```

(3) Open the configuration file `drs_filer/config.yaml` and edit the `host` key
in the `db` section to refer to the correct location of the MongoDB
instance. For a local MonogDB instance, as installed in step (3), the host is
`localhost`.

(4) Bring up the server:
```bash
cd drs_filer && python app.py
```

Once the server is up and running, it can be queried, e.g. by running
```bash
curl localhost:8080/ga4gh/drs/v1/service-info
```

## Testing the server

To run the unit test suite, activate the development environment (as set up
in the previous section), and run the following command from the root of the
repository:
```bash
pytest tests
```

If `pytest` cannot be found, install the testing requirements via `pip install
-r requirements-test.txt`.

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
