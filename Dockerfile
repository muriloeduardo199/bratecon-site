FROM python:3.13-alpine AS build

ENV PYTHONUTF8=1
WORKDIR /app
COPY build.py ./
COPY src/ ./src/
COPY assets/ ./assets/
RUN python build.py

FROM nginx:stable-alpine
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist/ /usr/share/nginx/html/
EXPOSE 80
