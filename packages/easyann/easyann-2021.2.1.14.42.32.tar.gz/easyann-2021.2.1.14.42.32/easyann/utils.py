#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-ANN.
# @File         : utils
# @Time         : 2021/2/1 12:04 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 
"""

client.list_id_in_segment
client.list_partitions

client.delete_entity_by_id
client.drop_collection
client.drop_index
client.drop_partition

集合结构化

"""

from meutils.pipe import *


class Collection(object):

    def __init__(self, name=None, client=None):
        self.name = name
        self.client = client
        self.count_entities = self.count
        self.count_documents = self.count

    def __str__(self):
        has_collection = self.client.has_collection(self.name)
        if not has_collection:
            logger.warning(f"{self.name}  doesn't exist")
        return f"Collection({self.name})"

    def __getattr__(self, name):
        return self.collection_info

    def get_entity_by_id(self, ids, fields=None):
        return self.client.get_entity_by_id(self.name, ids, fields)

    def create_collection(self):
        """
        client.create_collection
        client.create_index
        client.create_partition
        """

    @property
    def collection_info(self):
        return self.client.get_collection_info(self.name)

    @property
    def collection_stats(self):
        return self.client.get_collection_stats(self.name)

    @property
    def count(self):
        """
        count_entities
        count_documents
        :return:
        """
        return self.client.count_entities(self.name)



from milvus import Milvus, DataType


class Scalar(object):

    def __init__(self, name='Scalar', type=DataType.INT32):
        self.name = name
        self.type = type
        self.params = {}
        self.indexes = [{}]

    def dict(self):
        return self.__dict__


class Vector(Scalar):
    def __init__(self, name='Vector', type=DataType.FLOAT_VECTOR, dim=768, index_type='IVF_FLAT', metric_type='IP',
                 nlist=1024):
        super().__init__(name, type)
        self.params = {'dim': dim}
        self.indexes = [{'index_type': index_type, 'metric_type': metric_type, 'params': {'nlist': nlist}}]
