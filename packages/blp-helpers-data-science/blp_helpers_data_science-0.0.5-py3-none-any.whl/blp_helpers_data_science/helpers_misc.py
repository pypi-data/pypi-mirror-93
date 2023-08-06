from newsapi import NewsApiClient
import pandas as pd
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from io import StringIO
import yaml


def get_articles_from_newsapi_with_source(
        from_param='2020-01-01'
        , to_param='2020-31-12'
        , newsapi_key=''
        , article_source_ids=''
):
    """Downloads articles from newsapi using sources

    :param from_param: Format: yyyy-mm-dd
    :type from_param: str

    :param from_param: Format: yyyy-mm-dd
    :type from_param: str

    :param newsapi_key:
    :type from_param: str

    :param article_source_ids:
    :type from_param: str
    """

    all_articles_all_pages_df = pd.DataFrame()
    suchseite = 1
    anzahl_artikel_gefunden_von_api = 1

    newsapi = NewsApiClient(api_key=newsapi_key)

    while anzahl_artikel_gefunden_von_api > 0:
        all_articles_current_page_respone = newsapi.get_everything(
            from_param=from_param
            , to=to_param
            , page_size=100
            , page=suchseite
            , sources=article_source_ids
        )

        all_articles_current_page = all_articles_current_page_respone['articles']
        anzahl_artikel_gefunden_von_api = len(all_articles_current_page)
        all_articles_current_page_df = pd.DataFrame.from_dict(all_articles_current_page)
        all_articles_all_pages_df = all_articles_all_pages_df.append(all_articles_current_page_df)

        suchseite += 1
        if suchseite == 100:
            break
    return all_articles_all_pages_df


# function to get News for NewsApi
def get_articles_from_newsapi_with_qintitle(qintitle=None
                              , article_language=None
                              , from_param='2020-01-01' # yyyy-mm-dd
                              , to_param='2020-31-12'
                              , newsapi_key=''
                              ):
    all_articles_all_pages_df = pd.DataFrame()
    suchseite = 1
    anzahl_artikel_gefunden_von_api = 1
    
    newsapi = NewsApiClient(api_key=newsapi_key)



    while anzahl_artikel_gefunden_von_api > 0:
        all_articles_current_page_respone = newsapi.get_everything(
            from_param=from_param
            , to=to_param
            , language=article_language
            , page_size=100
            , page=suchseite
            , qintitle=qintitle
        )

        all_articles_current_page = all_articles_current_page_respone['articles']
        anzahl_artikel_gefunden_von_api = len(all_articles_current_page)
        all_articles_current_page_df = pd.DataFrame.from_dict(all_articles_current_page)
        all_articles_all_pages_df = all_articles_all_pages_df.append(all_articles_current_page_df)

        suchseite += 1
        if suchseite == 100:
            break
    return all_articles_all_pages_df


def get_data_using_catalog(dataset_name, config_version, azure_storage_connection_string):
    """Returns a pandas dataframe for a dataset_name stored in a catalog.yml file
    
    It either gets the data from azure or local

    Filepaths are stored in the catalog.yml according to kedro
    See: https://kedro.readthedocs.io/en/stable/02_get_started/05_example_project.html
    
    Parameters
    ----------
    dataset_name : str
        The name of the dataset to be loaded according to the catalog.yml-file
    config_version : str
        Which conf-folder to use, according to kedro it can be local or base
    azure_storage_connection_string : str
        Connection string for Azure Data Lake (see Azure Doc. for more info)

    Returns
    -------
    A pandas dataframe
    """

    with open("../conf/{}/catalog.yml".format(config_version), 'r') as stream:
        try:
            yaml_file_content = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    # the storage_provider determines if the file is on azure or local
    storage_provider = yaml_file_content.get(dataset_name).get('storage_provider')

    # depending whether it is on azure or local change loading way
    if storage_provider == 'local':
        # get the relative path
        data_file_path = '../' + yaml_file_content.get(dataset_name).get('filepath')
        df = pd.read_csv(data_file_path)
    else:  # it is azure
        data_container_name = yaml_file_content.get(dataset_name).get('container_name')
        data_blob_name = yaml_file_content.get(dataset_name).get('filepath')
        container_client = ContainerClient.from_connection_string(
            conn_str=azure_storage_connection_string
            , container_name=data_container_name
        )
        # Download blob as StorageStreamDownloader object (stored in memory)
        downloaded_blob = container_client.download_blob(data_blob_name)

        df = pd.read_csv(StringIO(downloaded_blob.content_as_text()))

    return df
