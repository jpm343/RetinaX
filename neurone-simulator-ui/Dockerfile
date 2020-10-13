### STAGE 1: BUILD ###

FROM node:14.6.0-stretch-slim as builder

WORKDIR /usr/src/app
COPY package*.json ./
RUN yarn install 

ARG MODE=production

COPY . .
RUN yarn run build --mode=${MODE}

### STAGE 2: INSTALL ###

FROM nginx:1.17.8

RUN rm -rf /usr/share/nginx/html/*
COPY --from=builder /usr/src/app/dist /usr/share/nginx/html/
COPY config/nginx.conf /etc/nginx/nginx.conf
CMD ["nginx", "-g", "daemon off;"]
