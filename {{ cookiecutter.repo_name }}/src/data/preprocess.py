""" Preprocess data to prepare it for model training. """

import logging
from pathlib import Path
from typing import Union


def main(input_filepath: Union[str, Path],
         output_filepath: Union[str, Path]) -> None:
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')
    print(input_filepath)
    print(output_filepath)


if __name__ == '__main__':
    LOG_FMT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=LOG_FMT)

    main('data/raw', 'data/processed')
