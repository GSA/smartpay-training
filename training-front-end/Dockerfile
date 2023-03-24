FROM node:18
WORKDIR /usr/src/app
ENV HOME /home/node
RUN chown node:node /usr/src/app
USER node
COPY package*.json .
RUN npm ci
CMD ["npm", "run", "dev", "--", "--host"]
