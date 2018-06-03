# ml-for-movie_recommendation
Super simple movie recommend system

This is very quick - simple material for reviewing about main algorithm of recommend system.

# Minimum Requirements

* Python v2.7.
* Pandas v0.22+.

# Reference / resources

* movie data from kaggle.com.[Kaggle sample download](https://www.kaggle.com/rounakbanik/the-movies-dataset)
* udemy machine learning course.[Udemy course](https://www.udemy.com/data-science-and-machine-learning-with-python-hands-on)

# Basic workflow

The main concept which was used in here is based on udemy course.
Main task in this project was regenerate main algorighm based on actual movie data.

## Convert movie data to dataframe.

In this process, below processes are being done.
 
1. Load movie metadata csv file.
2. Convert #1 data to panda dataframe.
3. Cleanup #2 panda dataframe.
4. Filter out / reduce data based on input filter.
5. Load rating csv file.
6. Convert #5 data to panda dataframe.
7. Merge #4, #6 and generate merged dataframe.

Actual code :

    filter = {
        'anti_genres': ['Romance', 'History'],
        'vote_average': 6,
        'vote_count': 1000
    }
    df_movie = get_movie_dataframe(filter)

## Generate pivot table.

In this process, generate pivot table which contains all movie title columns for all user ids.
 
Actual code :

    pivot_table = get_pivot_table(df_movie)

## Generate correlation matrix based on dataframe.

In this process, generate correlation matrix which is containing actual number what tells 'this movie rating and this movie rating have some relationship or not'.

Actual code :

    corr_table = get_corr_table(pivot_table)

## Generate recommandation

In this process, generate actual recommendation based on input user ratings.

Actual code :

    my_ratings = pd.Series(
        {
            'Captain America: The First Avenger': 5.0, 
            'Iron Man': 5.0, 
            'Star Wars':1.0, 
            'Toy Story': 1.0, 
            'Cars': 1.0, 
            'Shrek 2': 1.0
        }
    )
    get_recommandation(my_ratings, corr_table)

# Documentation

Actual execution result can be checked in below jupyter file..

[notebok sample](/recommandation.ipynb)

## Data preparation

This package is using actual data from kaggle.com.
For actual execution of this tool, below data must be prepared.

./the-movies-dataset/movies_metadata.csv
./the-movies-dataset/ratings.csv

Original source can be downloaded from below.

[Kaggle sample download](https://www.kaggle.com/rounakbanik/the-movies-dataset)

# Changelog
