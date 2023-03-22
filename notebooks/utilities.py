import json
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

def string_to_dict(dict_string):
    # Convert to proper json format
    dict_string = dict_string.replace("'", '"').replace('u"', '"')
    return json.loads(dict_string)


# fonction retournant un df encodé
def encode_df(df, col_to_encode):
    # creating instance of one-hot-encoder
    ohe = OneHotEncoder(handle_unknown='ignore')
    # perform one-hot encoding on 'team' column
    encoder_df = pd.DataFrame(ohe.fit_transform(df[col_to_encode]).toarray())
    print(encode_df)
    # merge one-hot encoded columns back with original DataFrame
    final_df = df.join(encoder_df)
    return final_df