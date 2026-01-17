# Node Image
FROM node:20-alpine

# work directory
WORKDIR /app

# dependency 설치
COPY package*.json .
RUN npm install

# code 
COPY . .

# port 
EXPOSE 3000

# server
CMD ["npm", "start"]