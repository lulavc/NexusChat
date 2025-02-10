FROM node:18-alpine

WORKDIR /app

# First copy only package files for better caching
COPY package*.json ./
RUN npm install

# Then copy the rest of the application
COPY . .

# Environment setup for development
ENV NODE_ENV=development
ENV VITE_HOST=0.0.0.0

EXPOSE 3000

# Development command
CMD ["npm", "run", "dev", "--", "--host"] 