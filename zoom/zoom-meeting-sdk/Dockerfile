FROM node:16.17.0-bullseye-slim
# Create app directory
RUN mkdir /zoom-web
WORKDIR /zoom-web
# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY package*.json ./
RUN npm install
ENV NODE_OPTIONS=--max-old-space-size=8192
# Bundle app source
COPY . .
CMD ["npm", "start"]
Expose 3000

#docker build -t goals-react .
#docker run --name goals-app --rm -p 3000:3000 goals-react

