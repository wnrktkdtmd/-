FROM pytorch/pytorch:1.6.0-cuda10.1-cudnn7-runtime

RUN conda install numpy
RUN conda install pandas
RUN pip install konlpy
RUN conda install gensim
RUN conda install smart_open==2.0.0
RUN conda install Flask gunicorn
RUN conda install -c conda-forge pickle5
RUN apt-get update
RUN conda install -c conda-forge jpype1
RUN apt-get install -y openjdk-8-jdk
RUN export PATH="/usr/lib/jvm/java-8-openjdk-amd64:$PATH"

ENV APP_HOME /app
WORKDIR $APP_HOME

COPY ./model.doc2vec ./
COPY ./loadmodel.py ./
COPY ./app.py ./
COPY ./groups.pickle ./

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
