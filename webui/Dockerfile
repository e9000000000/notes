FROM node:20.10.7

WORKDIR /service
ENV PATH /service/node_modules/.bin:$PATH

COPY package.json package-lock.json ./
RUN npm install --silent --production

CMD npm run build
