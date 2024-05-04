#!/bin/bash
docker run -v `pwd`:/work:rw -v /mnt:/mnt:rw --net host -d --name work_kourituka python_work_kourituka