#####
##### Docker multi-stage build : Node.js build image
#####
FROM node:lts-alpine as build-stage

# make the 'app' folder the current working directory
WORKDIR /app

# Copy project files and restore as distinct layers
COPY package.json ./
COPY package-lock.json ./

# install project dependencies
RUN npm install

# Copy everything else for build
COPY src/ ./src
COPY vite.config.js ./
COPY index.html ./

# build app for production with minification
RUN npm run build

# Data 
COPY static/ /backend/templates/dist/static

# production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /backend/templates/dist /usr/share/nginx/html


EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]