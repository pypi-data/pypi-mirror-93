#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# Alan Viars

import argparse
import json
from collections import OrderedDict
from pymongo import MongoClient
import ndjson


def ndjson2mongo(ndjsonfile, database_name,
                 collection_name,
                 delete_collection_before_import,
                 host,
                 port):
    """Return a response_dict with a summary of ndjson2mongo transaction."""
    print("Import file", ndjsonfile,
          "into the MongoDB collection", collection_name, ".")
    # collection_name, "within the database", database_name, "."

    response_dict = OrderedDict()
    fileindex = 0
    mongoindex = 0
    error_list = []

    mc = MongoClient(host=host, port=port)
    db = mc[database_name]
    collection = db[collection_name]

    if delete_collection_before_import:
        db.drop_collection(collection)

    with open(ndjsonfile) as f:
        data = ndjson.load(f, object_pairs_hook=OrderedDict)
        for item in data:
            # print("item",item)
            try:
                if not isinstance(item, type(OrderedDict())):
                    error_message = "File " + \
                        str(ndjsonfile) + \
                        " did not contain a JSON object, i.e. {}."
                    error_list.append(error_message)
                # insert the item/document
                myobjectid = collection.insert(item)
                mongoindex += 1

            except:
                # print(sys.exc_info())
                error_message = "File " + \
                    str(item) + " did not contain valid JSON."
                error_list.append(error_message)

        if error_list:
            response_dict['file'] = ndjsonfile
            response_dict['database'] = database_name
            response_dict['collection'] = collection_name
            response_dict['num_files_imported'] = mongoindex
            response_dict['num_file_errors'] = len(error_list)
            response_dict['errors'] = error_list
            response_dict['code'] = 400
            response_dict['message'] = "Completed with errors."

        else:
            response_dict['file'] = ndjsonfile
            response_dict['database'] = database_name
            response_dict['collection'] = collection_name
            response_dict['num_rows_imported'] = mongoindex
            response_dict['num_file_errors'] = len(error_list)
            response_dict['code'] = 200
            response_dict['message'] = "Completed without errors."

    return response_dict

if __name__ == "__main__":

    # Parse args
    parser = argparse.ArgumentParser(
        description='Load in the NDJSON doc into MongoDB')
    parser.add_argument(
        dest='input_ndjson_file',
        action='store',
        help='Input the NDJSON file to load here')
    parser.add_argument(
        dest='db_name',
        action='store',
        help="Enter the Database name you want to import the JSON to")
    parser.add_argument(
        dest='collection_name',
        action='store',
        help="Enter the Collection name within the Database specified that you want the JSON to be imported to")
    parser.add_argument('-d', '--delete', dest='delete', action='store_true',
                        help='Delete previous collection upon import')
    parser.add_argument(
        '--host',
        dest='host',
        action='store',
        default='127.0.0.1',
        help='Specify host. Default is 127.0.0.1 ')
    parser.add_argument(
        '-p',
        '--port',
        dest='port',
        action='store',
        default=27017,
        help='Specify port. Default is 27017')
    args = parser.parse_args()
    ndjson_file = args.input_ndjson_file
    database = args.db_name
    collection = args.collection_name
    delete_collection_before_import = args.delete
    host = args.host
    port = args.port

    result = ndjson2mongo(
        ndjson_file,
        database,
        collection,
        delete_collection_before_import,
        host,
        port)

    # output the JSON transaction summary
    print(json.dumps(result, indent=4))
