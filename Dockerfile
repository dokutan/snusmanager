FROM python:3.15-rc-alpine
WORKDIR /app
COPY frontend/dist/ /app/dist/
COPY backend/*.py backend/default_thumbnail.webp .
RUN apk add py3-gunicorn py3-pillow py3-z3 py3-flask py3-flask-cors
ENV SNUSMANAGER_DB=/app/db/db.sqlite
EXPOSE 8000
CMD ["gunicorn", "snusmanager:app", "--bind", "[::]:8000"]
