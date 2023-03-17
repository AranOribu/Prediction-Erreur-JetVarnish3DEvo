import pandas as pd
import numpy as np
import json

# fonction retournant un dataframe et convertissant les valeurs d'une Serie de type string en liste
def convert_str_to_list(pandas_object):
    return pd.DataFrame(pandas_object.apply(lambda x :json.loads(x)), columns=[pandas_object.name])

# fonction retournant la liste des clés d'un dictionnaire
def get_keys(dict):
    return list(k for k in dict.keys() )

# fonction retournant un dataframe, en ajoutant des colonnes
def add_key_column(df, col_name, keys, index):
    for key in keys:
        df[col_name+'_'+key+'_'+str(index)] = df[col_name].apply(lambda x: x[index].get(key))
    return df


# fonction retournant la longueur d'une liste
def check_list_length(list):
    if len(list) :
        print(len(list))


# fonction retournant une liste d'entiers, après conversion une Serie de valeur string en liste d'entiers
def convert_str_to_int_list(x):
    # on remplace les NaN par des '0' => toutes les valeurs sont maintenant des str
    x.replace(to_replace=np.nan, value='0', inplace=True)
    # on joint les str de toutes les colonnes dans une liste
    lis = ','.join(x.dropna().values.tolist()).split(',')
    # on convertit les str en int, si possible sinon valeur = 1000
    new_list = []
    for code in lis :
        try:
            new_list.append(int(code))
            it_is = True
        except ValueError:
            new_list.append(1000)
            it_is = False
    # lis = [int(i) for i in lis]
    # on supprime les valeurs 0 de chaque liste
    new_list = [x for x in new_list if x!=0]
    # if 377 in lis :
    #     print(lis)
    return new_list


# fonction supprime les valeurs 'None'
def del_none(str):
    str = str.split()
    while 'None' in str : 
        del str[str.index('None')]
    return str