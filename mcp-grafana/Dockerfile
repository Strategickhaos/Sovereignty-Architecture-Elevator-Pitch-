FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install production dependencies only
RUN npm install --production

# Copy pre-built application files
COPY dist ./dist

# Set environment
ENV NODE_ENV=production

# Run the server
CMD ["node", "dist/index.js"]
