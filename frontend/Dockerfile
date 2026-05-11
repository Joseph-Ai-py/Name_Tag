FROM node:20-alpine as builder

WORKDIR /app

# Copy logo files to public
COPY logo/ ./public/

# Copy frontend
COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ .

# Build
RUN npm run build

# Production stage
FROM node:20-alpine

WORKDIR /app

# Install serve to run the app
RUN npm install -g serve

# Copy built app from builder
COPY --from=builder /app/dist ./dist

EXPOSE 3000

CMD ["serve", "-s", "dist", "-l", "3000"]
