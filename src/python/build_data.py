import pandas as pd

def create_df():

    df = pd.DataFrame()

    df['title'] = None
    df['type_job'] = None
    df['salary'] = None
    df['compagny'] = None
    df['location'] = None
    df['region'] = None
    df['departement'] = None
    df['latitude'] = None
    df['longitude'] = None
    df['language'] = None
    df['skills'] = None
    df['date'] = None
    df['description'] = None
    df['tokens'] = None
    df['source'] = None

    return df


def add_row(df, row_data):
    df.loc[len(df)] = row_data
    return df


def save_df(df,filename):
    # Save the df DataFrame in src/data directory
    print(df.head())
    df.to_csv('src/data/'+filename+'.csv', index=False)
