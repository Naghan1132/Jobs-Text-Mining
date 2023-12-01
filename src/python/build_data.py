import pandas as pd

def create_df():

    df = pd.DataFrame()

    df['title'] = None
    df['type_job'] = None
    df['location'] = None
    df['source'] = None
    df['description'] = None

    return df


def add_row(df, row_data):
    df.loc[len(df)] = row_data
    return df


def save_df(df,filename):
    # Save the df DataFrame in src/data directory
    print(df.head())
    df.to_csv('../data/'+filename+'.csv', index=False)
