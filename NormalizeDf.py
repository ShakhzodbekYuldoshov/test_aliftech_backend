from sklearn.preprocessing import MinMaxScaler
import pandas as pd


def normalize_df(df):
    # normalize dataframe between 0 and 1
    scaler = MinMaxScaler()
    scaled_df = scaler.fit_transform(df)

    # create new dataframe with scaled values
    scaled_df = pd.DataFrame.from_dict(dict(zip(df.columns, scaled_df.T)))

    return scaled_df
