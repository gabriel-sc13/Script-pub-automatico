FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir PyGithub

ENV GITHUB_TOKEN=""
ENV REPO_OWNER=""
ENV REPO_NAME=""

ENTRYPOINT ["python", "publish_release.py"]
