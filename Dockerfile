FROM elixircloud/foca:20230301-py3.10

WORKDIR /app

COPY . .

RUN pip install -e . -v \
  && pip install -r requirements-crypt4gh.txt \
  && chmod g+w ./drs_filer/api/ \
  && pip install yq

ENTRYPOINT ["./entrypoint.sh"]

CMD ["bash", "-c", "cd /app/drs_filer; python app.py"]
