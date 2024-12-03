FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir redis==5.2.0

COPY . .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]

EXPOSE 6379