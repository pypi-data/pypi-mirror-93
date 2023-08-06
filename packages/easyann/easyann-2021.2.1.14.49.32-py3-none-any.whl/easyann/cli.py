#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-ANN.
# @File         : cli
# @Time         : 2021/1/31 11:22 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from milvus import Milvus, DataType

class Scalar(BaseModel):
    name = 'Scalar'
    type = DataType.INT32

    def __init__(self, **data):
        super().__init__(**data)

        self.name = "xxxxxx"
        # self.indexes = [{}]



if __name__ == '__main__':
    print(Scalar().dict())