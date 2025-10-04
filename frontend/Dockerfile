FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY frontend/ ./

# Build the application
RUN npm run build

# Production stage with nginx
FROM nginx:alpine

# Copy nginx config with proxy, WebSocket, and caching
COPY <<EOF /etc/nginx/conf.d/default.conf
server {
    listen 5000;
    server_name _;
    
    root /usr/share/nginx/html;
    index index.html;
    
    # Proxy API requests to backend
    location /api/ {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }
    
    # WebSocket support for live chat
    location /api/ws {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
    }
    
    # Cache static assets for performance
    location ~* \.(js|css|png|jpg|jpeg|gif|svg|ico|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # No cache for index.html
    location = /index.html {
        add_header Cache-Control "no-cache, no-store, must-revalidate";
    }
    
    # SPA routing
    location / {
        try_files \$uri \$uri/ /index.html;
    }
}
EOF

# Copy built files from builder
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 5000

CMD ["nginx", "-g", "daemon off;"]