import pandas as pd
import structlog
from typing import Sequence, Optional
from pathlib import Path
from opal.constants import DATA_REPO_URL, DATA_LOCAL_STORE


logger = structlog.get_logger()


def retrieve_completed_dataframes(filename: str, seasons: Sequence[str], filetype: Optional[str] = "csv") ->\
        pd.DataFrame:
    """Return dataframe of requested completed seasons and filename. Cannot get partial seasons"""
    df_out = pd.DataFrame()
    for s_ in seasons:
        local_path = Path(DATA_LOCAL_STORE)
        local_file = local_path.joinpath('.'.join(['_'.join([filename, s_]), filetype]))
        if not local_file.exists():
            logger.info(f"File does not exist locally, retrieving {'_'.join([s_, filename])} from URL")
            # if no local file then download from url first:
            url_path = '.'.join(['/'.join([DATA_REPO_URL, s_, filename]), filetype])
            df = pd.read_csv(url_path)

            df.to_csv(local_file)

        df = get_data(local_file)
        if df_out.empty:
            df_out = df
        else:
            df_out = pd.concat([df_out, df])
    return df_out


def retrieve_active_dataframe(filename: str, season: str, filetype: Optional[str] = "csv") -> pd.DataFrame:
    """This is different because the season has not completed yet, this means that we want to overwrite the dataframe
    in certain occasions"""
    local_path = Path(DATA_LOCAL_STORE)
    local_file = local_path.joinpath('.'.join(['_'.join([filename, season]), filetype]))
    logger.info(f"Retrieving {'_'.join([filename, season])} from URL")
    url_path = '.'.join(['/'.join([DATA_REPO_URL, season, filename]), filetype])
    df = pd.read_csv(url_path)
    df.to_csv(local_file)
    return df


def get_data(filepath: [str, Path]) -> pd.DataFrame:
    return pd.read_csv(filepath, index_col=0)


if __name__ == '__main__':
    """Code tested: 
    retrieve completed seasons works fine
    retrieve active season ..."""
    seasons_sequence = ["2021-22", "2022-23"]
    data_name = "teams"
    data_type = "csv"
    df_test = retrieve_completed_dataframes(data_name, seasons_sequence, data_type)
    print(df_test.sample(4))
    print(df_test.columns)


