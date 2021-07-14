FROM continuumio/miniconda3

WORKDIR /src

COPY plotting-service /src/plotting-service

WORKDIR /src/plotting-service

#RUN conda install -n base --file env2.yml && conda clean -a
RUN conda env create -f env.yml

RUN echo "source activate plotting-service" > ~/.bashrc
ENV PATH /opt/conda/envs/plotting-service/bin:$PATH

EXPOSE 5000

#CMD ["python", "app.py"]
CMD ["gunicorn", "app:app", "--config", "/src/plotting-service/gunicorn.config.py"]
