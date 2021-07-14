FROM continuumio/miniconda3

# Update C env vars so compiler can find gdal

WORKDIR /root/service

COPY . /root/service

#RUN conda install -n base --file env2.yml && conda clean -a
RUN conda env create -f env2.yml

RUN echo "source activate plotting-service" > ~/.bashrc
ENV PATH /opt/conda/envs/plotting-service/bin:$PATH

EXPOSE 5000

#CMD ["gunicorn", "-c", "gunicorn_conf.py", "wsgi:app"]
CMD ["python", "app.py"]
