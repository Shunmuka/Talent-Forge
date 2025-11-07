FROM python:3.11-slim
WORKDIR /app
# TODO: copy API source and install dependencies when ready
CMD ["python", "-m", "app.main"]
