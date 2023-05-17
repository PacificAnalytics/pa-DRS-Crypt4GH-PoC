##### BASE IMAGE #####
FROM elixircloud/foca:20230301-py3.10

##### METADATA ##### 

LABEL software="DRS-filer"
LABEL software.description="Flask Connexion implementation of Data Repository Schema"
LABEL software.website="https://github.com/elixir-cloud-aai/drs-filer"
LABEL software.license="https://spdx.org/licenses/Apache-2.0"
LABEL maintainer="sarthakgupta072@gmail.com"
LABEL maintainer.organisation="ELIXIR Cloud & AAI"


## Copy remaining app files
COPY ./ /app

## Install app
RUN cd /app \
    && pip install -e . -v \
    && pip install -e uploader -v \
    && cd / \
    && chmod g+w /app/drs_filer/api/ \
    && pip install yq

CMD ["bash", "-c", "cd /app/drs_filer; python app.py"]
