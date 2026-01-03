FROM node:20-alpine
WORKDIR /app
COPY package.json tsconfig.json vite.config.ts ./
COPY src ./src
RUN npm install
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "dev", "--", "--host"]
