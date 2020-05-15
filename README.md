# WSS
Weather Services Statistics

## Backend 
Backend app collects data from weather service providers and saves it to database.  
It is located in **wss** directory and doesn't require any external python modules.

- Command to run it once manually: `python3 -m wss`

- To schedule it to run every 30 minutes:
    - edit crontab config with command `crontab -e`
    - add line 
    `*/30 * * * * cd /path/to/WSS/ && python3 -m wss 
 python3 -m wss`

## Frontend
Fronted app is a web-service for visualizing data. 
... 