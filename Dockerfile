FROM python:3.9
#FROM sonoisa/deep-learning-coding:pytorch1.6.0_tensorflow2.3.0


# mecabの導入
RUN apt-get -y update && \
  apt-get -y upgrade && \
  apt-get install -y mecab && \
  apt-get install -y libmecab-dev && \
  apt-get install -y mecab-ipadic-utf8 && \
  apt-get install -y git && \
  apt-get install -y make && \
  apt-get install -y curl && \
  apt-get install -y xz-utils && \
  apt-get install -y file && \
  apt-get install -y sudo

ADD . /app
WORKDIR /app



RUN apt-get install -y vim less
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile default --component rls rust-analysis
ENV PATH="/root/.cargo/bin:$PATH"
RUN pip install -r requirements.txt
RUN pip install gunicorn
RUN sudo cp /etc/mecabrc /usr/local/etc/

WORKDIR /app/opt
VOLUME ./opt:/app
#EXPOSE 8080:8080
#CMD flask run --host 0.0.0.0 --port 8080
CMD exec gunicorn --bind :$PORT --workers 4 --threads 8 app:app
CMD python app.py


#ENV APP_HOME /app
#WORKDIR $APP_HOME
#COPY . ./
#RUN export CRYPTOGRAPHY_DONT_BUILD_RUST=1
#RUN pip install setuptools_rust
# RUN curl -y curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
#RUN pip install Flask gunicorn
#RUN export CRYPTOGRAPHY_DONT_BUILD_RUST=1
#RUN pip install setuptools_rust
# RUN curl -y curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
#CMD sudo cp ./etc/mecabrc /usr/local/etc/