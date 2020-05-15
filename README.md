# WSS
Weather Services Statistics

## Backend 
Data collecting app is located in **wss** directory.
- To run it manually use command: `python3 -m wss`

- To schedule it to run every 30 minutes:
    - edit crontab with command `crontab -e`
    - add line 
    `*/30 * * * * cd /path/to/WSS/ && python3 -m wss 
 python3 -m wss`

## Frontend