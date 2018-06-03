import json
from StringIO import StringIO


import pandas as pd


def get_movie_dataframe(filter):

    # Get movie dataframe.
    movie_metadata = _load_movie_metadata()
    df_movie = _convert_metadata_to_panda_dataframe(movie_metadata)
    cleanuped_df_movie = _cleanup_df_movie_data(df_movie)
    print cleanuped_df_movie
    reduced_df_movie = _filter_df_movie(cleanuped_df_movie, filter)

    # Get rating dataframe.
    df_rating = _convert_rating_to_dataframe()

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
    f = open('./the-movies-dataset/movies_metadata.csv', 'r')
    return ''.join(f.readlines())


def _convert_metadata_to_panda_dataframe(movie_metadata):
    df_movie = pd.read_csv(
        StringIO(movie_metadata),
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
    # Rename id.
    df_movie.rename(
        columns={'id': 'movieId'},
        inplace=True
    )

    for i in df_movie.index.values:

        # Modify genres information.
        df_movie.at[i, 'genres'] = ','.join(
            _generate_list_from_string(
                df_movie.at[i, 'genres']
            )
        )

        # Convert release data.
        try:
            df_movie.at[i, 'release_date'] = _convert_release_date(df_movie.at[i, 'release_date'])
        except:
            df_movie.at[i, 'release_date'] = '19000101'

        # Convert movie id data.
        try:
            df_movie.at[i, 'movieId'] = int(df_movie.at[i, 'movieId'])
        except:
            df_movie.at[i, 'movieId'] = -1

    return df_movie


def _convert_release_date(content):
    try:
        return content.replace('-', '')
    except:
        return '19000101'


def _filter_df_movie(df_movie, filter):
    for key, value in filter.iteritems():
        field_name = key
        if 'anti_' in key:
            field_name = key.replace('anti_', '')

        if type(value) == list:
            if 'anti_' in key:
                for x in value:
                    df_movie = df_movie[df_movie['genres'].str.contains(x) == False]
            else:
                for x in value:
                    df_movie = df_movie[df_movie['genres'].str.contains(x) == True]

        elif type(value) == int or type(value) == float:
            if 'anti_' in key:
                df_movie = df_movie.loc[df_movie[field_name] < value]
            else:
                df_movie = df_movie.loc[df_movie[field_name] > value]

    return df_movie


def _convert_rating_to_dataframe():
    rating = _load_rating()
    return pd.read_csv(
        rating,
        usecols=['userId', 'movieId', 'rating']
    )


def _load_rating():
    f = open('./the-movies-dataset/ratings.csv', 'r')
    return StringIO(''.join(f.readlines()))


def _generate_list_from_string(content):
    try:
        result = [
            x['name'] for x in json.loads(
                content.replace('"', '#').replace('\'', '"').replace('#', '\'')
            )
        ]
    except:
        result = []
    return result

