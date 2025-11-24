# Deployment Guide

This guide covers deploying Eduak Backend to production environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Docker Deployment](#docker-deployment)
4. [Manual Deployment](#manual-deployment)
5. [Database Setup](#database-setup)
6. [Web Server Configuration](#web-server-configuration)
7. [SSL/HTTPS Setup](#sslhttps-setup)
8. [Monitoring](#monitoring)
9. [Backup Strategy](#backup-strategy)
10. [Troubleshooting](#troubleshooting)

## Prerequisites

- Ubuntu 20.04+ or similar Linux distribution
- Python 3.11+
- PostgreSQL 15+
- Nginx
- Domain name with DNS configured
- SSL certificate (Let's Encrypt recommended)

## Environment Setup

### 1. Update System

```bash
sudo apt update
sudo apt upgrade -y
```

### 2. Install Dependencies

```bash
# Python and pip
sudo apt install python3.11 python3.11-venv python3-pip -y

# PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Nginx
sudo apt install nginx -y

# Other tools
sudo apt install git curl -y
```

### 3. Create Application User

```bash
sudo useradd -m -s /bin/bash eduak
sudo su - eduak
```

## Docker Deployment (Recommended)

### 1. Install Docker

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group
sudo usermod -aG docker $USER
```

### 2. Clone Repository

```bash
cd /home/eduak
git clone https://github.com/akfaqih3/eduak-backend.git
cd eduak-backend
```

### 3. Configure Environment

```bash
cp .env.example .env
nano .env
```

Update with production values:
```env
SECRET_KEY=your-very-secure-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DB_ENGINE=django.db.backends.postgresql
DB_NAME=eduak_db
DB_USER=eduak_user
DB_PASSWORD=secure-db-password
DB_HOST=db
DB_PORT=5432

EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=https://yourdomain.com/api/v1/accounts/google/login/

CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### 4. Build and Run

```bash
# Build containers
docker-compose build

# Start services
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

### 5. Verify Deployment

```bash
docker-compose ps
docker-compose logs web
```

## Manual Deployment

### 1. Clone Repository

```bash
cd /home/eduak
git clone https://github.com/akfaqih3/eduak-backend.git
cd eduak-backend
```

### 2. Create Virtual Environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
```

### 4. Configure Environment

```bash
cp .env.example .env
nano .env
```

### 5. Run Migrations

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 6. Create Systemd Service

```bash
sudo nano /etc/systemd/system/eduak.service
```

Add:
```ini
[Unit]
Description=Eduak Backend
After=network.target

[Service]
Type=notify
User=eduak
Group=eduak
WorkingDirectory=/home/eduak/eduak-backend
Environment="PATH=/home/eduak/eduak-backend/.venv/bin"
ExecStart=/home/eduak/eduak-backend/.venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/home/eduak/eduak-backend/eduak.sock \
    --timeout 60 \
    --access-logfile /home/eduak/eduak-backend/logs/access.log \
    --error-logfile /home/eduak/eduak-backend/logs/error.log \
    config.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 7. Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl start eduak
sudo systemctl enable eduak
sudo systemctl status eduak
```

## Database Setup

### 1. Create PostgreSQL Database

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE eduak_db;
CREATE USER eduak_user WITH PASSWORD 'secure-password';
ALTER ROLE eduak_user SET client_encoding TO 'utf8';
ALTER ROLE eduak_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE eduak_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE eduak_db TO eduak_user;
\q
```

### 2. Configure PostgreSQL for Remote Access (if needed)

```bash
sudo nano /etc/postgresql/15/main/postgresql.conf
```

Change:
```
listen_addresses = 'localhost'
```

```bash
sudo nano /etc/postgresql/15/main/pg_hba.conf
```

Add:
```
host    eduak_db    eduak_user    127.0.0.1/32    md5
```

Restart:
```bash
sudo systemctl restart postgresql
```

## Web Server Configuration

### Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/eduak
```

Add:
```nginx
upstream eduak_backend {
    server unix:/home/eduak/eduak-backend/eduak.sock fail_timeout=0;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Logging
    access_log /var/log/nginx/eduak_access.log;
    error_log /var/log/nginx/eduak_error.log;
    
    # Client body size
    client_max_body_size 10M;
    
    # Static files
    location /static/ {
        alias /home/eduak/eduak-backend/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Media files
    location /media/ {
        alias /home/eduak/eduak-backend/media/;
        expires 7d;
        add_header Cache-Control "public";
    }
    
    # Application
    location / {
        proxy_pass http://eduak_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/eduak /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## SSL/HTTPS Setup

### Using Let's Encrypt (Certbot)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal (already configured)
sudo certbot renew --dry-run
```

## Monitoring

### 1. Application Logs

```bash
# View logs
tail -f /home/eduak/eduak-backend/logs/django.log
tail -f /home/eduak/eduak-backend/logs/access.log
tail -f /home/eduak/eduak-backend/logs/error.log

# Nginx logs
tail -f /var/log/nginx/eduak_access.log
tail -f /var/log/nginx/eduak_error.log
```

### 2. System Monitoring

```bash
# Install monitoring tools
sudo apt install htop iotop -y

# Check system resources
htop

# Check disk usage
df -h

# Check memory
free -h
```

### 3. Application Health Check

Create a simple health check endpoint and monitor it:

```bash
curl https://yourdomain.com/api/v1/health/
```

## Backup Strategy

### 1. Database Backup

Create backup script:
```bash
nano /home/eduak/backup_db.sh
```

Add:
```bash
#!/bin/bash
BACKUP_DIR="/home/eduak/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# Backup database
PGPASSWORD="secure-password" pg_dump -h localhost -U eduak_user eduak_db > $BACKUP_DIR/db_$DATE.sql

# Compress
gzip $BACKUP_DIR/db_$DATE.sql

# Keep only last 7 days
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +7 -delete

echo "Backup completed: db_$DATE.sql.gz"
```

Make executable:
```bash
chmod +x /home/eduak/backup_db.sh
```

### 2. Media Files Backup

```bash
nano /home/eduak/backup_media.sh
```

Add:
```bash
#!/bin/bash
BACKUP_DIR="/home/eduak/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# Backup media files
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /home/eduak/eduak-backend/media/

# Keep only last 7 days
find $BACKUP_DIR -name "media_*.tar.gz" -mtime +7 -delete

echo "Backup completed: media_$DATE.tar.gz"
```

### 3. Automate Backups

```bash
crontab -e
```

Add:
```
# Daily database backup at 2 AM
0 2 * * * /home/eduak/backup_db.sh

# Weekly media backup on Sunday at 3 AM
0 3 * * 0 /home/eduak/backup_media.sh
```

## Troubleshooting

### Application Won't Start

```bash
# Check service status
sudo systemctl status eduak

# Check logs
journalctl -u eduak -n 50

# Check permissions
ls -la /home/eduak/eduak-backend/
```

### Database Connection Issues

```bash
# Test connection
psql -h localhost -U eduak_user -d eduak_db

# Check PostgreSQL status
sudo systemctl status postgresql

# Check PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-15-main.log
```

### Nginx Issues

```bash
# Test configuration
sudo nginx -t

# Check status
sudo systemctl status nginx

# Check logs
sudo tail -f /var/log/nginx/error.log
```

### Static Files Not Loading

```bash
# Collect static files again
cd /home/eduak/eduak-backend
source .venv/bin/activate
python manage.py collectstatic --noinput

# Check permissions
sudo chown -R eduak:eduak /home/eduak/eduak-backend/static/
```

### High Memory Usage

```bash
# Check processes
ps aux | grep gunicorn

# Restart service
sudo systemctl restart eduak

# Adjust worker count in systemd service
sudo nano /etc/systemd/system/eduak.service
# Change --workers value
sudo systemctl daemon-reload
sudo systemctl restart eduak
```

## Performance Optimization

### 1. Database Optimization

```sql
-- Create indexes (already in models)
-- Analyze tables
ANALYZE;

-- Vacuum database
VACUUM ANALYZE;
```

### 2. Gunicorn Workers

Rule of thumb: `(2 x CPU cores) + 1`

```bash
# For 2 CPU cores
--workers 5
```

### 3. Caching

Consider adding Redis for caching:

```bash
sudo apt install redis-server -y
pip install django-redis
```

Update settings:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

## Updating the Application

```bash
cd /home/eduak/eduak-backend
git pull origin main
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart eduak
```

## Rollback Procedure

```bash
# Restore database
gunzip < /home/eduak/backups/db_YYYYMMDD_HHMMSS.sql.gz | psql -U eduak_user eduak_db

# Restore code
cd /home/eduak/eduak-backend
git checkout <previous-commit-hash>
sudo systemctl restart eduak
```

## Support

For deployment issues:
- GitHub Issues: https://github.com/akfaqih3/eduak-backend/issues
- Email: support@eduak.com

## Checklist

- [ ] Server configured and secured
- [ ] Database created and configured
- [ ] Application deployed
- [ ] Environment variables set
- [ ] Migrations run
- [ ] Static files collected
- [ ] Nginx configured
- [ ] SSL certificate installed
- [ ] Firewall configured
- [ ] Backups automated
- [ ] Monitoring set up
- [ ] Health checks working
- [ ] Documentation updated

Congratulations! Your Eduak Backend is now deployed! 🚀
