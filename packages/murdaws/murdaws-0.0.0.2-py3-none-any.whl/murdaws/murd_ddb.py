from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key
from murd import Murdi
from run_async import run_async, default_log


ddb_murd_prefix = "murd_"
__murd = None


def create_murd_table(name):
    ddb = boto3.client("dynamodb")
    ddb.create_table(
        TableName=f'{ddb_murd_prefix}{name}.{datetime.utcnow().isoformat()[:10]}',
        BillingMode="PAY_PER_REQUEST",
        AttributeDefinitions=[
            {
                'AttributeName': f'{Murdi.region_key}',
                'AttributeType': 'S'
            },
            {
                'AttributeName': f'{Murdi.sort_key}',
                'AttributeType': 'S'
            }
        ],
        KeySchema=[
            {
                'AttributeName': f'{Murdi.region_key}',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': f'{Murdi.sort_key}',
                'KeyType': 'RANGE'
            }
        ]
    )


def list_all_ddb_tablenames():
    ddb = boto3.client("dynamodb")
    resp = ddb.list_tables()
    tablenames = resp['TableNames']
    while 'LastEvaluatedTableName' in resp:
        resp = ddb.list_tables(ExclusiveStartTableName=resp['LastEvaluatedTableName'])
        tablenames.extend(resp['TableNames'])

    return tablenames


def get_murds(force_scan=False):
    if get_murds.tables is None or force_scan:
        tablenames = list_all_ddb_tablenames()
        murd_tables = [table for table in tablenames if ddb_murd_prefix == table[:len(ddb_murd_prefix)]]
        ddb = boto3.resource("dynamodb")
        get_murds.tables = {tablename: ddb.Table(tablename) for tablename in murd_tables}
    return get_murds.tables


get_murds.tables = None


def get_latest_murd():
    tables = get_murds()
    keys = list(get_murds.tables.keys())
    keys = sorted(keys, reverse=True)
    __murd = tables[keys[0]]
    return __murd


def update(murdis,
           identifier="Unidentified"):
    primed_murdis = Murdi.ze(murdis)

    if len(primed_murdis) > 0:
        latest_murd = get_latest_murd()
        print("Sending {} murdis to {} table".format(len(primed_murdis), latest_murd.table_name))

        # Store Memories in DynamoDB table
        with latest_murd.batch_writer() as writer:
            for key, murdi in primed_murdis.items():
                murdi = Murdi(**murdi)
                writer.put_item(Item=murdi)
    else:
        print("No murdis to upload")


def complete_table_query(table, kwargs):
    query_result = table.query(**kwargs)
    items = query_result['Items']

    while 'LastEvaluatedKey' in query_result:
        kwargs['ExclusiveStartKey'] = query_result['LastEvaluatedKey']
        query_result = table.query(**kwargs)
        items.extend(query_result['Items'])

        if 'Limit' in kwargs and len(items) >= kwargs['Limit']:
            break

    results = [Murdi(**item) for item in items]
    if 'Limit' in kwargs:
        results = results[:kwargs['Limit']]

    return results


def async_results_to_murdi_list(results):
    return [Murdi(**murdi) for murdis in results for murdi in murdis]


def read(region,
         sort=None,
         min_sort=None,
         max_sort=None,
         limit=None):
    if type(region) is list:
        regions = region
        arg_sets = [{
            "region": region,
            "sort": sort,
            "min_sort": min_sort,
            "max_sort": max_sort,
            "limit": limit
        } for region in regions]

        arg_sets, results = zip(*run_async(read, arg_sets, log=default_log))
        return async_results_to_murdi_list(results)
    else:
        kce = Key(Murdi.region_key).eq(region)
        if sort is not None:
            kce = kce & Key(Murdi.sort_key).begins_with(sort)

        elif max_sort is not None and min_sort is not None:
            kce = kce & Key(Murdi.sort_key).between(max_sort, min_sort)

        elif max_sort is not None:
            kce = kce & Key(Murdi.sort_key).gt(max_sort)
        elif min_sort is not None:
            kce = kce & Key(Murdi.sort_key).lt(min_sort)

        kwargs = {}
        kwargs['KeyConditionExpression'] = kce
        if limit is not None:
            kwargs['Limit'] = limit

        arg_sets = [[table, kwargs] for table in get_murds().values()]
        arg_sets, results = zip(*run_async(complete_table_query, arg_sets, log=default_log))
        return async_results_to_murdi_list(results)


def delete_from_table(table, murdis):
    stubborn_murdis = []
    with table.batch_writer() as writer:
        for murdis in murdis:
            try:
                writer.delete_item(
                    Key={
                        Murdi.region_key: murdis[Murdi.region_key],
                        Murdi.sort_key: murdis[Murdi.sort_key]
                    }
                )
            except Exception:
                stubborn_murdis.append(murdis)

    return stubborn_murdis


def delete(murdis):
    arg_sets = [[table, murdis] for table in get_murds.tables.values()]
    run_async(delete_from_table, arg_sets, log=default_log)
