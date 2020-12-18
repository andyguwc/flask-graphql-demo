FROM node:12 as frontend-builder

WORKDIR /frontend
COPY /client /frontend

RUN npm ci --unsafe-perm --loglevel silent
RUN npm run build --loglevel silent


FROM python:3.7

ENV BASE_DIR=/backend
ENV BASE_USER=demo

WORKDIR ${BASE_DIR}

RUN useradd -ms /bin/bash -d $BASE_DIR -G sudo ${BASE_USER} && \
  apt-get install -y --fix-broken && apt-get autoremove &&\
  apt-get update && apt-get -y upgrade && apt-get install -y --no-install-recommends apt-utils \
  libssl-dev \
  libpq-dev \
  libffi-dev &&\
  apt-get install -y gcc

COPY --from=frontend-builder /frontend/build ${BASE_DIR}/client/build

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --quiet

COPY demo demo
COPY migrations migrations
COPY run.py boot.sh ./


RUN chown -R ${BASE_USER}.${BASE_USER} ${BASE_DIR}
USER ${BASE_USER}

RUN chmod +x boot.sh

EXPOSE 5000

ENTRYPOINT ["./boot.sh"]
