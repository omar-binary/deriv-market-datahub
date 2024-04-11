# Run: poetry run python3 src/importer.py --resource_name symbols

import argparse
import logging
import sys


# need to be set for root logger before importing any module that uses logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(message)s')


def parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser(description='Arguments')
    parser.add_argument(
        '--resource_name',
        required=True,
        help='Resource name for getting data',
        type=str,
        choices=['symbols', 'assets', 'stream', 'countries', 'ticks_history', 'candles_history'],
    )
    # add argument for ticks_history
    parser.add_argument('--symbol', required=False, help='Symbol for getting data', type=str, default='R_50')
    parser.add_argument('--start', required=False, help='Start time for getting data', type=int, default=0)
    parser.add_argument('--end', required=False, help='End time for getting data', type=int, default=0)

    return parser.parse_args()


def main():
    args = parse_args()
    logging.info(f'Starting importer with args: {args}')

    import deriv

    deriv.run(args)
    logging.info('Finished importer')


if __name__ == '__main__':
    main()
