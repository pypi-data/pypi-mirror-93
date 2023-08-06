#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-ANN.
# @File         : ANNMilvus
# @Time         : 2020/4/27 11:34 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


# https://github.com/milvus-io/docs/blob/master/site/en/guides/milvus_operation.md#createdrop-indexes-in-a-collection
# https://github.com/milvus-io/pymilvus/tree/master/examples/indexes
# https://raw.githubusercontent.com/milvus-io/pymilvus/0.7.0/examples/example.py
# TODO: 补充对应的rest api
# m.milvus.preload_table

import sys
import time
from milvus import Milvus, IndexType, MetricType


class ANNMilvus(object):

    def __init__(self, host='10.46.30.210', port='19530'):
        self.milvus = Milvus()

        print("Client Version:", self.milvus.client_version())

        status = self.milvus.connect(host, port)

        if status.OK():
            print("Server connected.")
            status, self.collections = self.milvus.show_collections()
        else:
            print("Server connect fail.")
            sys.exit(1)

        print("Server Version:", self.milvus.server_version()[-1])

    def describe_collection(self, collection_name='test'):
        print("Collections: ", self.collections)
        print(f"Describe: {self.milvus.describe_collection(collection_name)[-1]}")
        print(f"Vector number in {collection_name}: {self.milvus.count_collection(collection_name)}")

    def create_collection(self, collection_name='test', dimension=768, index_file_size=1024, metric_type=MetricType.IP,
                          **kwargs):

        status, ok = self.milvus.has_collection(collection_name)
        if ok:
            print(f"{collection_name} already exists！！！")
        else:
            params = {
                'collection_name': collection_name,
                'dimension': dimension,
                'index_file_size': index_file_size,  # optional index_file_size：文件到达这个大小的时候，milvus开始为这个文件创建索引。
                'metric_type': metric_type  # optional
            }

            self.milvus.create_collection({**params, **kwargs})

    def create_index(self, collection_name, index_type=IndexType.IVFLAT, index_param=None, timeout=-1):
        """drop_index

        :param collection_name:
        :param index_type:
        :param index_param:
            index_param = {
                'nlist': 2048
                }
        :param timeout:
        :return:
        """
        # You can search vectors without creating index. however, Creating index help to
        # search faster
        status = self.milvus.create_index(collection_name, index_type, index_param, timeout)
        print(status)

        # describe index, get information of index
        status, index = self.milvus.describe_index(collection_name)
        print(status)
        print(index)

    def insert(self, collection_name, records, ids=None, partition_tag=None, params=None, timeout=-1):
        status, self.ids = self.milvus.insert(collection_name, records, ids, partition_tag, params, timeout)
        time.sleep(3)
        status, result = self.milvus.count_collection(collection_name)
        print(status)
        print("count_collection: ", result)

    def drop_collection(self, collection_name, partition_tag=None, timeout=10):

        if partition_tag:
            status = self.milvus.drop_partition(collection_name, partition_tag, timeout)
        else:
            status = self.milvus.drop_collection(collection_name, timeout)

        print(status)
        time.sleep(1)

    def search(self, collection_name, top_k, query_records, partition_tags=None, params=None):
        """

        :param collection_name:
        :param top_k:
        :param query_records:
        :param partition_tags:
        :param params: {'nprobe': 16}
        :return:
        """
        status, results = self.milvus.search(collection_name, top_k, query_records, partition_tags, params)
        print(status)
        print(results)

    def get_vector_by_id(self):
        """
        ann.milvus.delete_by_id
        ann.milvus.get_vector_by_id
        ann.milvus.get_vector_ids
        """
        pass
