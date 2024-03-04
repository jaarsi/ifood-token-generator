FROM python:3.10-slim
RUN apt update && apt upgrade -y
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_PORT=8000
# ENTRYPOINT [ "scripts/docker-entrypoint.sh" ]
CMD [ "scripts/docker-entrypoint.sh" ]
