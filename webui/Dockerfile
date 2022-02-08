FROM node:latest

WORKDIR /service
ENV PATH /service/node_modules/.bin:$PATH

COPY package.json package-lock.json ./
RUN npm install --silent --production

CMD npm run build
