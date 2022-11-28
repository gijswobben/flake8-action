FROM python:3-slim AS builder
WORKDIR /app

# We are installing a dependency here directly into our app source dir
COPY ./requirements.txt ./requirements.txt
RUN pip install --target=/app -r requirements.txt

ADD . /app

# A distroless container image with Python and some basics like SSL certificates
# https://github.com/GoogleContainerTools/distroless
FROM gcr.io/distroless/python3-debian10
COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH /app
ENTRYPOINT [ "./entrypoint.sh" ]