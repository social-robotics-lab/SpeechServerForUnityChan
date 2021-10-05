# ssfu_client
Sample programs for communicating to SpeechServerForUnitychan.


# Making a docker image 
```
cd 
docker build -t ssfu_client .
```

# Run
```
docker run --rm -it --name ssfu_client --mount type=bind,source="$(pwd)"/src,target=/tmp ssfu_client /bin/bash
python3 sample.py --host 192.168.x.x 
```
