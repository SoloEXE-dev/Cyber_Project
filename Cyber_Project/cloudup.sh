#! /bin/bash
rsync -avh --relative /main/dummyfiles /backup/$(date -I)