FROM node:20 as build

WORKDIR /app
COPY . .
RUN yarn install
RUN yarn build

FROM nginx:1.24.0
WORKDIR /usr/share/nginx/html
RUN rm -rf ./*
COPY --from=build /app/build .
ENTRYPOINT ["nginx", "-g", "daemon off;"]
