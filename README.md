# WSS
Weather Services Statistics

## Backend 
Data collecting app is located in **wss** directory.
- To run it manually use command: `python3 -m wss`

- To schedule it to run every 30 minutes:
    - edit crontab with command: `crontab -e`
    - add line: 
    `*/30 * * * * cd /path/to/WSS/ && python3 -m wss`

## Frontend
Frontend works with Flask framework. Before install it you should create virtual environment:
- change directory to where fronted located:  
`cd /path/to/WSS/wss-front`
- create virtual environment with name **venv**:  
`python3 -m venv venv`
- activate it:  
`. venv/bin/activate`
- now you can install Flask in new virtual environment:  
`pip install Flask`  
or you can install all required modules according to requirements txt-file:
`pip install -r requirements.txt`
- to run service using development server:
    - set environment variable FLASK_APP:  
    `export FLASK_APP=wss-front.py`
    - run development web server  
    `flask run`
    
- to run service on production server:  
    - install gunicorn web-server:  
    `pip install gunicorn`    
    - to start gunicorn manually, use command:
    `gunicorn -b localhost:8000 -w 4 wss-front:app`
    - to start gunicorn with supervisor create config `/etc/supervisor/conf.d/wss-front.conf`:
    ```
    [program:wss-front]
    command=/path/to/WSS/wss-front/venv/bin/gunicorn -b localhost:8000 -w 4 $
    directory=/path/to/WSS/wss-front
    user=username
    autostart=true
    autorestart=true
    stopasgroup=true
    killasgroup=true
    ```
    - example of nginx config '/etc/nginx/sites-enabled/wss-front':
    ```
    server {
        listen 80;
        server_name _;
        location / {
            return 301 https://$host$request_uri;
        }
    }
    server {
        listen 443 ssl;
        server_name _;
    
        ssl_certificate /etc/letsencrypt/live/your.domain.name/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/your.domain.name/privkey.pem;
    
        access_log /var/log/wss_access.log;
        error_log /var/log/wss_error.log;
    
        location / {
            proxy_pass http://localhost:8000;
            proxy_redirect off;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    
        location /static {
            alias /path/to/WSS/wss-front/app/static;
            expires 30d;
        }
    }
    
    ```
     - certificates for https you can get with certbot help: https://certbot.eff.org/ 