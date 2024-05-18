FROM python:3.7
COPY . /app
WORKDIR /app
EXPOSE 80
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install pytest
CMD ["python","app.py"]
