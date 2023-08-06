#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: DIYer22@github
@mail: ylxx@live.com
Created on Sat Jul 20 22:48:51 2019
"""

import os

RLAUNCH_REPLICA = int(os.environ.get("RLAUNCH_REPLICA", 0))
RLAUNCH_REPLICA_TOTAL = int(os.environ.get("RLAUNCH_REPLICA_TOTAL", 1))

replica_idx = int(os.environ.get("RJOB_REPLICA", RLAUNCH_REPLICA))
replica_total = int(os.environ.get("RJOB_REPLICA_TOTAL", RLAUNCH_REPLICA_TOTAL))

is_replica = replica_total > 1  # `bpp.isReplica`: 判断是否为 replica 模式


try:
    import torch

    gpun = torch.cuda.device_count()
    direction = ["output", "input"][gpun > 0]
    device = torch.device("cpu")
except ImportError:
    gpun = 0
    direction = "output"
    device = "cpu"

if __name__ == "__main__":
    pass
