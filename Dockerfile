FROM python:3-slim
WORKDIR /app

# We are installing a dependency here directly into our app source dir
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY ./ ./
ENTRYPOINT [ "/app/entrypoint.sh" ]
