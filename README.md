# TODO
- create a dockerfile to run the ingestor application
- create a hosted MongoDB instance on a cloud service
  - use digital ocean. Its cheap. 
  - probably ingest no more than like top 50 channels
  - in order to save on storage space we can delete data once it has been processed
  - we can have two collections. 
    - chats. For raw chats. Deleted every x time 
    - stats. For stats served to client to power visualization. Kept forever.
- get a small VM from a cloud service and deploy the container on that VM




# Developer Guide

Run the mongoDB
```

```

Run the ingestor 
```
source .venv/bin/activate
uv pip install .
cd src
python -m twitch_data_ingestor
```



