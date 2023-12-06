# Stage 1: Build the application
#FROM node:20-alpine as build-stage

#WORKDIR /app

#COPY package*.json ./
#RUN npm install

#COPY . .
#RUN npm run build

#this first part does not work because of vite plugin for vue wheareas it works locally I don't know why, so I build the project first and then run the dockerfile

# Stage 2: Serve the application from Nginx
FROM nginx:stable-alpine as production-stage

#COPY --from=build-stage /app/dist /usr/share/nginx/html
# Copy the local dist folder to the Nginx serve directory
COPY ./dist /usr/share/nginx/html

# Expose port 5000
EXPOSE 5000

CMD ["nginx", "-g", "daemon off;"]

