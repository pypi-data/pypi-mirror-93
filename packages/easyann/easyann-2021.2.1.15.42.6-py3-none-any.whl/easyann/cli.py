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
from easyann import ANN


class Config(BaseConfig):
    data = '/Users/yuanjie/Desktop/vec.parquet'
    reader = ''

    ips: List[str]
    collection_name = 'demo'
    ann_fields: List = Field([], alias='fields')
    auto_id: bool = True
    segment_row_limit: int = 4096
    batch_size = 10000


conf = Config.parse_zk('/mipush/easyann/user_ann')


def insert_data(ip):
    ann = ANN(ip)
    ann.create_collection(
        conf.collection_name,
        fields=conf.ann_fields,
        auto_id=conf.auto_id,
        segment_row_limit=conf.segment_row_limit
    )

    df = eval(conf.reader)(conf.data)
    collection = ann.__getattr__(conf.collection_name)
    collection.batch_insert(df, conf.batch_size)


conf.ips | xThreadPoolExecutor(insert_data, max_workers=3) | xlist

# if __name__ == '__main__':
#     insert_data(conf.ips[0])
