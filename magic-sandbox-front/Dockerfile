# Stage 1: Build the application
FROM node:20 as build-stage

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Stage 2: Serve the application from Nginx
FROM nginx:stable-alpine as production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html

# Expose port 5000
EXPOSE 5000

CMD ["nginx", "-g", "daemon off;"]
