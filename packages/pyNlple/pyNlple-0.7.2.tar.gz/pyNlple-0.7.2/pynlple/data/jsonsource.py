﻿# -*- coding: utf-8 -*-
import io
import json
from operator import itemgetter

import requests
from elasticsearch import Elasticsearch

from pynlple.data.source import Source, SkippingSource, TakingSource
from pynlple.exceptions import DataSourceException


class ElasticJsonDataSource(TakingSource, SkippingSource):

    def __init__(self, url_addresses, port, index, query, keys=None, fill_na_map=None, authentication=None,
                 cluster_timeout=10, max_retries=5, max_urls_pool_size=3):
        if type(url_addresses) not in (tuple, list, set):
            url_addresses = [url_addresses]
        self.urls = url_addresses
        self.PORT = port
        self.index = index
        self.__query = query
        self.keys = keys
        self.na_map = fill_na_map
        self.auth = authentication
        self.cluster_timeout = cluster_timeout
        self.max_retries = max_retries
        self.max_connection_pool_size = max_urls_pool_size
        self.es = Elasticsearch(self.__get_connection_props(), timeout=self.cluster_timeout, max_retries=max_retries,
                                retry_on_timeout=True)
        self.es.cluster.health(wait_for_status='yellow', request_timeout=self.cluster_timeout)
        super().__init__()

    def __get_connection_props(self):
        import random
        return [{'host': url, 'port': self.PORT} for url in random.sample(self.urls, self.max_connection_pool_size)]

    def set_cluster_timeout(self, cluster_timeout_secs, max_retries=5):
        self.cluster_timeout = cluster_timeout_secs
        self.max_retries = max_retries
        self.es = Elasticsearch(self.__get_connection_props(), timeout=self.cluster_timeout, max_retries=max_retries,
                                retry_on_timeout=True)
        self.es.cluster.health(wait_for_status='yellow', request_timeout=self.cluster_timeout)
        return self

    def _take(self, take):
        query = dict(self.__query)
        query['size'] = take
        self.__query = query

    def _skip(self, skip):
        query = dict(self.__query)
        query['from'] = skip
        self.__query = query

    def __prepare_final_query(self):
        final_query = dict(self.__query)
        if self.keys:
            final_query.update({'_source': self.keys})
        return final_query

    def get_data(self):
        try:
            final_query = self.__prepare_final_query()
            response = self.es.search(index=self.index, body=final_query)
        except Exception as e:
            raise DataSourceException(e.__str__())

        if self.na_map:
            results = [self.__fill_na_values(entry['_source']) for entry in response['hits']['hits']]
        else:
            results = [entry['_source'] for entry in response['hits']['hits']]
        print('Server had {0} total elements. Query yielded {1} elements.'
              .format(str(response['hits']['total']), str(len(results))))
        return results

    def count(self):
        try:
            final_query = self.__prepare_final_query()
            response = self.es.count(index=self.index, body=final_query)
        except Exception as e:
            raise DataSourceException(e.__str__())
        return response['count']

    def aggregate(self):
        try:
            final_query = self.__prepare_final_query()
            response = self.es.search(index=self.index, body=final_query)
        except Exception as e:
            raise DataSourceException(e.__str__())
        return response['aggregations']

    def __fill_na_values(self, entry):
        for key, value in self.na_map.items():
            if key not in entry:
                entry[key] = value
        return entry

    def set_data(self, json_data):
        raise NotImplementedError()


class ServerJsonDataSource(Source):
    """Class for providing json data via POST rest api calls."""

    def __init__(self, url_address, query, authentication=None):
        self.url_address = url_address
        self.query = query
        self.authentication = authentication

    def get_data(self):
        request = requests.post(url=self.url_address, data=self.query, auth=self.authentication)
        if request.status_code is not 200:
            raise DataSourceException(
                'Could not reach the data. HTTP response code: {}, response: {}'.format(str(request.status_code),
                                                                                        str(request.content)))
        else:
            return request.json()

    def set_data(self, json_data):
        raise NotImplementedError()


class FileJsonDataSource(Source):
    """Class for providing json data from json files."""

    FILE_OPEN_METHOD = 'rt'
    FILE_WRITE_METHOD = 'wt'
    DEFAULT_ENCODING = 'utf-8'

    def __init__(self, file_path, encoding_str=DEFAULT_ENCODING):
        self.file_path = file_path
        self.encoding_str = encoding_str

    def get_data(self):
        # TODO: Handle Nan/None here
        with io.open(self.file_path, FileJsonDataSource.FILE_OPEN_METHOD, encoding=self.encoding_str) as data_file:
            return json.load(data_file)

    def set_data(self, json_data):
        # TODO: Handle Nan/None here
        with io.open(self.file_path, FileJsonDataSource.FILE_WRITE_METHOD, encoding=self.encoding_str) as data_file:
            json.dump(json_data, data_file, ensure_ascii=False, indent=1)

    def __iter__(self):
        for entry in self.get_data():
            yield entry


class ESFileDumpSource(Source):
    FILE_OPEN_METHOD = 'rt'
    FILE_WRITE_METHOD = 'wt'
    DEFAULT_ENCODING = 'utf-8'

    def __init__(self, file_path, encoding_str=DEFAULT_ENCODING):
        self.file_path = file_path
        self.encoding_str = encoding_str

    def get_data(self):
        with io.open(self.file_path, FileJsonDataSource.FILE_OPEN_METHOD, encoding=self.encoding_str) as data_file:
            return list(
                map(itemgetter('_source'), filter(lambda x: x['_type'] == 'mention', map(json.loads, data_file))))

    def set_data(self, json_data):
        raise NotImplementedError()

    def __iter__(self):
        for entry in self.get_data():
            yield entry
