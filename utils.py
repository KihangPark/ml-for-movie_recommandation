import json
from StringIO import StringIO


import pandas as pd


def get_movie_dataframe(filter):
    """Return panda dataframe which contains movie / rating information.

    Args:
        filter (dict): dictionary information which contains field key, values.

    Returns:
        pandas.core.frame.DataFrame

    """

    # Get movie dataframe.
    movie_metadata = _load_movie_metadata()
    df_movie = _convert_metadata_to_panda_dataframe(movie_metadata)
    cleanuped_df_movie = _cleanup_df_movie_data(df_movie)
    reduced_df_movie = _filter_df_movie(cleanuped_df_movie, filter)

    # Get rating dataframe.
    df_rating = _load_and_convert_rating_to_dataframe()

    return pd.merge(reduced_df_movie, df_rating)


def get_pivot_table(df_movie):
    return df_movie.pivot_table(
        index=['userId'],
        columns=['original_title'],
        values='rating'
    )


def get_corr_table(df_pivot):
    return df_pivot.corr(min_periods=20)


def get_recommandation(my_rating, df_corr):
    candidates = pd.Series()
    for i in range(0, len(my_rating.index)):
        candidate = df_corr[my_rating.index[i]].dropna()
        candidate = candidate.map(lambda x: x * my_rating[i])
        candidates = candidates.append(candidate)
    candidates.sort_values(inplace=True, ascending=False)
    return candidates


def _load_movie_metadata():
    """Load movie metadata csv file.

    Returns:
        str: string contents which contains movie metadata information.

    """
    f = open('./the-movies-dataset/movies_metadata.csv', 'r')
    return ''.join(f.readlines())


def _convert_metadata_to_panda_dataframe(movie_metadata):
    """Convert movie metadata to panda dataframe.

    Args:
        movie_metadata (str): string contents which contains movie metadata information.

    Returns:
        pandas.core.frame.DataFrame
    """
    df_movie = pd.read_csv(
        StringIO(movie_metadata),
        # Filter out useful information.
        usecols=[
            'genres',
            'id',
            'original_title',
            'release_date',
            'vote_average',
            'vote_count'
        ]
    )
    return df_movie


def _cleanup_df_movie_data(df_movie):
    """Cleanup movie dataframe.
    (In general, raw data contains pretty funky values
    and it was same to this sample data.)
    Beside of this, this process is renaming 'id' to 'movieId',
    this modification is because we want to merge movie and rating dataframe
    based on this 'movieId'.

    Args:
        df_movie (pandas.core.frame.DataFrame): raw dataframe.

    Returns:
        pandas.core.frame.DataFrame: purified dataframe.
    """
    # Rename id.
    df_movie.rename(
        columns={'id': 'movieId'},
        inplace=True
    )

    for i in df_movie.index.values:

        # Modify genres information.
        df_movie.at[i, 'genres'] = ','.join(
            _generate_genre_list_from_string(
                df_movie.at[i, 'genres']
            )
        )

        # Convert release data.
        try:
            df_movie.at[i, 'release_date'] = df_movie.at[i, 'release_date'].replace('-', '')
        except:
            df_movie.at[i, 'release_date'] = '19000101'

        # Convert movie id data.
        try:
            df_movie.at[i, 'movieId'] = int(df_movie.at[i, 'movieId'])
        except:
            df_movie.at[i, 'movieId'] = -1

    return df_movie


def _filter_df_movie(df_movie, filter):
    """Filter out movie dataframe based on filter.

    Args:
        df_movie (pandas.core.frame.DataFrame): dataframe.

    Returns:
        pandas.core.frame.DataFrame: reduced dataframe.
    """
    for key, value in filter.iteritems():

        field_name = key

        # Rename key name if filter name contains 'anti_'.
        if 'anti_' in key:
            field_name = key.replace('anti_', '')

        if type(value) == list:
            if 'anti_' in key:
                for x in value:
                    df_movie = df_movie[
                        df_movie['genres'].str.contains(x) == False
                    ]
            else:
                for x in value:
                    df_movie = df_movie[
                        df_movie['genres'].str.contains(x) == True
                    ]

        elif type(value) == int or type(value) == float:
            if 'anti_' in key:
                df_movie = df_movie.loc[
                    df_movie[field_name] < value
                ]
            else:
                df_movie = df_movie.loc[
                    df_movie[field_name] > value
                ]

    return df_movie


def _load_and_convert_rating_to_dataframe():
    """Return rating data frame.

    Returns:
        pandas.core.frame.DataFrame: reduced dataframe.
    """
    f = open('./the-movies-dataset/ratings.csv', 'r')
    rating = StringIO(''.join(f.readlines()))
    return pd.read_csv(
        rating,
        usecols=['userId', 'movieId', 'rating']
    )


def _generate_genre_list_from_string(content):
    """Return genre list.

    Args:
        content (str): raw genre staring.

    Returns:
        (list): list of purified genre names.
    """
    try:
        result = [
            x['name'] for x in json.loads(
                content.replace('"', '#').replace('\'', '"').replace('#', '\'')
            )
        ]
    except:
        result = []
    return result

