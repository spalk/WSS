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
- set environment variable FLASK_APP:  
`export FLASK_APP=wss-front.py`
- to run service manually use command:  
`flask run`
- to run service constantly - *to be continued...* 