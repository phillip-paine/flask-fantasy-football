import pandas as pd
import structlog
from typing import Sequence
from pathlib import Path
from opal.constants import DATA_REPO_URL, DATA_LOCAL_STORE


logger = structlog.get_logger()


def retrieve_completed_seasons(filename: str, filetype: str, seasons: Sequence[str] = ()) -> pd.DataFrame:
    """Return dataframe of requested completed seasons and filename. Cannot get partial seasons"""
    df_out = pd.DataFrame()
    for s_ in seasons:
        local_path = Path(DATA_LOCAL_STORE)
        local_file = local_path.joinpath('.'.join(['_'.join([filename, s_]), filetype]))
        if not local_file.exists():
            logger.info("File does not exist locally, retrieving from URL")
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


def retrieve_current_season(filename: str, season: str) -> pd.DataFrame:
    """This is different because the season has not completed yet"""
    df_out = pd.DataFrame()
    return df_out


def get_data(filepath: [str, Path]) -> pd.DataFrame:
    return pd.read_csv(filepath)


if __name__ == '__main__':
    seasons_sequence = ["2022-23"]
    data_name = "teams"
    data_type = "csv"
    df_test = retrieve_completed_seasons(data_name, data_type, seasons_sequence)
    print(df_test.head(1))
    print(df_test.columns)

