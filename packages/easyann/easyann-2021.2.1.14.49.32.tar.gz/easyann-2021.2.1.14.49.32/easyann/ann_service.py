#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-ANN.
# @File         : ann_service
# @Time         : 2021/1/31 11:25 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :


"""
1. 建表建索引
2. id mapping: cache/mongodb; 自动生成索引还是自行映射索引
3. 插入数据：根据相应的数据格式指定相应的加载规则
    1> cache:
    1> csv: index scalar vector，大致流程是 加载数据到内存，然后执行cache相应的操作

"""
from meutils.pipe import *


class Config(BaseConfig):
    data_dir = ''
    glob = '*'
    reader = 'pd.read_parquet'
    vector_index: List[int] = [1]  # 规定id为第一列
    scalar_index: List[int] = []

    # milvus server
    ips = ''  # 逗号分割
    collection_name = ''
    write_type = 'overwrite'  # DelData: 优先级不高
    ann_fields: Any = Field('', alias='fields')


conf = Config.parse_zk("/mipush/easyann/user_ann")

# {'fileds': conf.ann_fields}


if not Path(conf.data).exists():
    logger.error(f"{conf.data} does not exist")

df = pd.concat(map(eval(conf.reader), Path(conf.data).glob(conf.glob)), ignore_index=True)
