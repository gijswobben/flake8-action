FROM python:3-slim AS builder
WORKDIR /app

# We are installing a dependency here directly into our app source dir
COPY ./requirements.txt ./requirements.txt
RUN pip install --target=/app -r requirements.txt
COPY ./ ./

# A distroless container image with Python and some basics like SSL certificates
# https://github.com/GoogleContainerTools/distroless
FROM gcr.io/distroless/python3-debian10
WORKDIR /app
COPY --from=builder /app /app
COPY ./entrypoint.sh ./entrypoint.sh
ENV PYTHONPATH /app
ENTRYPOINT [ "/app/entrypoint.sh" ]
