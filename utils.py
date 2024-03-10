import os
import pandas as pd
import numpy as np


def rank2point(rank, grille):
    if np.isnan(rank):return 0
    else: 
        return grille[int(rank)-1]

def clean_club(string):
    try:
        return string.lower().replace('é', 'e').replace('è', 'e').replace(' ', '').replace('-', '').replace('ç', 'c').replace('ë', "e").replace("ô", "o")
    except:
        return string

def get_UCD_top(df):
    df['Club Sportif'] = df['Club Sportif'].apply(lambda x: clean_club(x))
    df_ucd = df[df['Club Sportif'] == 'ucdarnetal']
    df_not_ucd = df[df['Club Sportif'] != 'ucdarnetal']
    df_out = pd.concat((df_ucd, df_not_ucd)).reset_index()
    df_out['index'] = df_out.index + 1
    df_out.index += 1
    return df_out

def clean_excel(string):
    return string.replace('/','_')

def cat2sheet(string):
        return 'Chrono - '+ string.replace('/', ' ')
