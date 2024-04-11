import asyncio

# let socket = new WebSocket('wss://ws.derivws.com/websockets/v3?app_id=1089');
import logging

import dlt

from deriv_api import DerivAPI


APP_ID = 16929


def load_to_gcs(data, pipeline_name, dataset_name, table_name, loader_file_format, write_disposition):
    # dlt will retrieve the password from ie. DESTINATION__FILESYSTEM__CREDENTIALS__PROJECT_ID
    pipeline = dlt.pipeline(
        pipeline_name=pipeline_name,
        destination='filesystem',
        dataset_name=dataset_name,
        progress='log',
        # , full_refresh=True
    )
    load_info = pipeline.run(
        data,
        table_name=table_name,
        write_disposition=write_disposition,
        loader_file_format=loader_file_format,
    )
    # we reuse the pipeline instance below and load to the same dataset as data
    pipeline.run([load_info], table_name='_load_info', loader_file_format=loader_file_format)
    # save trace to destination, sensitive data will be removed
    pipeline.run([pipeline.last_trace], table_name='_trace', loader_file_format=loader_file_format)

    # # print human friendly extract information
    # logging.info(pipeline.last_trace.last_extract_info)
    # # print human friendly normalization information
    # logging.info(pipeline.last_trace.last_normalize_info)
    # # access row counts dictionary of normalize info
    # logging.info(pipeline.last_trace.last_normalize_info.row_counts)
    # # print human friendly load information
    # logging.info(pipeline.last_trace.last_load_info)
    return load_info


async def load_symbols_to_data_lake(**kwargs):
    api = DerivAPI(app_id=APP_ID)

    active_symbols = await api.cache.active_symbols({'active_symbols': 'full'})

    load_info = load_to_gcs(
        data=active_symbols['active_symbols'],
        pipeline_name='deriv_symbols',
        dataset_name='market_data',
        table_name='symbols',
        loader_file_format='parquet',
        write_disposition='replace',
    )

    await api.clear()
    logging.info(f'load_info: {load_info}')
    logging.info(f'details: {load_info.load_packages[0]}')


async def load_asset_to_data_lake(**kwargs):
    api = DerivAPI(app_id=APP_ID)

    asset_index = await api.cache.asset_index({'asset_index': 1})

    load_info = load_to_gcs(
        data=asset_index['asset_index'],
        pipeline_name='deriv_asset_index',
        dataset_name='market_data',
        table_name='asset_index',
        loader_file_format='parquet',
        write_disposition='replace',
    )

    await api.clear()
    logging.info(f'load_info: {load_info}')
    logging.info(f'details: {load_info.load_packages[0]}')


async def load_country_to_data_lake(**kwargs):
    api = DerivAPI(app_id=APP_ID)

    asset_index = await api.cache.residence_list({'residence_list': 1})

    load_info = load_to_gcs(
        data=asset_index['residence_list'],
        pipeline_name='deriv_residence_list',
        dataset_name='market_data',
        table_name='residence_list',
        loader_file_format='parquet',
        write_disposition='replace',
    )

    await api.clear()
    logging.info(f'load_info: {load_info}')
    logging.info(f'details: {load_info.load_packages[0]}')


async def load_ticks_history_to_data_lake(**kwargs):
    api = DerivAPI(app_id=APP_ID)

    ticks_result = await api.cache.ticks_history(
        {
            'ticks_history': kwargs['symbol'],
            'adjust_start_time': 1,
            'count': 1,
            'start': kwargs['start'],
            'end': kwargs['end'],
            'style': 'ticks',
        },
    )

    ticks_history = {
        'style': ticks_result['echo_req']['style'],
        'ticks_history': ticks_result['echo_req']['ticks_history'],
        'price': str(ticks_result['history']['prices'][0]),
        'time': ticks_result['history']['times'][0],
        'pip_size': ticks_result['pip_size'],
    }

    load_info = load_to_gcs(
        data=[ticks_history],
        pipeline_name='deriv_ticks_history',
        dataset_name='market_data',
        table_name='ticks_history',
        loader_file_format='parquet',
        write_disposition='append',
    )

    await api.clear()
    logging.info(f'load_info: {load_info}')
    logging.info(f'details: {load_info.load_packages[0]}')


async def load_candles_history_to_data_lake(**kwargs):
    api = DerivAPI(app_id=APP_ID)

    candle_result = await api.cache.ticks_history(
        {
            'ticks_history': kwargs['symbol'],
            'adjust_start_time': 1,
            'count': 1,
            'start': kwargs['start'],
            'end': kwargs['end'],
            'style': 'candles',
            'granularity': 86400,  # 1 day
        },
    )

    candle_history = {
        'style': candle_result['echo_req']['style'],
        'ticks_history': candle_result['echo_req']['ticks_history'],
        'close': candle_result['candles'][0]['close'],
        'high': candle_result['candles'][0]['high'],
        'low': candle_result['candles'][0]['low'],
        'open': candle_result['candles'][0]['open'],
        'time': candle_result['candles'][0]['epoch'],
        'pip_size': candle_result['pip_size'],
    }

    load_info = load_to_gcs(
        data=[candle_history],
        pipeline_name='deriv_candles_history',
        dataset_name='market_data',
        table_name='candles_history',
        loader_file_format='parquet',
        write_disposition='append',
    )

    await api.clear()
    logging.info(f'load_info: {load_info}')
    logging.info(f'details: {load_info.load_packages[0]}')


def run(args):
    logging.info('App Started!')

    RESOURCE_NAME_TO_FUNCTION = {
        'assets': load_asset_to_data_lake,
        'symbols': load_symbols_to_data_lake,
        'countries': load_country_to_data_lake,
        'ticks_history': load_ticks_history_to_data_lake,
        'candles_history': load_candles_history_to_data_lake,
    }

    try:
        function = RESOURCE_NAME_TO_FUNCTION[args.resource_name]
        asyncio.run(function(**vars(args)))

    except Exception as e:
        logging.error(f'Unexpected error: {e}')
        raise Exception(f'Unexpected error: {e}')
