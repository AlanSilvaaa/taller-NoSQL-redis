FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]

EXPOSE 6379