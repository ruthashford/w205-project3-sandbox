# W205 Project 3


## Navigation
The key files for this project are described below: 

| File Name   | Description |
| ----------- | ----------- |
| [Report.ipynb](Report.ipynb)        | A python notebook containing a detailed description of the pipeline along with analysis of the data that is transported through the pipline       |
| [docker-compose.yml](docker-compose.yml)     | The docker compose file outlining the services needed to run this pipeline        |  
| [game_api.py](game_api.py)     | A flask application which decribes APIs for each event type and publishes received events to Kafka        |  
| [write_horse_events.py](write_horse_events.py)     | A python file that reads horse purchase events from Kafka and writes them to HDFS        |  
| [write_sword_events.py](write_sword_events.py)     | A python file that reads sword purchase events from Kafka and writes them to HDFS        |  
| [write_guild_events.py](write_guild_events.py)     | A python file that reads guild action events from Kafka and writes them to HDFS        |  
| [generate_data.sh](generate_data.sh)     | A script for generating sample data using Apache Bench        |  