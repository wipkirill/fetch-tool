FROM python:3.11-bullseye
WORKDIR /app
COPY src/requirements.txt ./
RUN pip install --no-cache-dir -r ./requirements.txt
COPY . .
ENV PYTHONPATH "${PYTHONPATH}:./src"
ENTRYPOINT ["python", "/app/src/main.py"]
