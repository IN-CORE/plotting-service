FROM continuumio/miniconda3

WORKDIR /src

COPY plotting-service /src/plotting-service
COPY plotting-service/dummy.sqlite3 /src/plotting-service/cache.sqlite3

WORKDIR /src/plotting-service

RUN mkdir /src/plotting-service/data \
 && mkdir /src/plotting-service/copydb

#RUN conda install -n base --file env2.yml && conda clean -a
RUN conda env create -f env.yml && \
  conda clean --all


RUN echo "source activate plotting-service" > ~/.bashrc
ENV PATH /opt/conda/envs/plotting-service/bin:$PATH

EXPOSE 5000

#CMD ["python", "app.py"]
CMD ["gunicorn", "app:app", "--config", "/src/plotting-service/gunicorn.config.py"]
