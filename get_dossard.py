import argparse
import os
import pandas as pd

from utils import clean_excel, clean_club, get_UCD_top

from module_dossard import MiseEnGrille
from module_ranking import Ranking

import warnings


important_col_english = ['First name', 'Last name', 'Sexe', 'Date de Naissance', 'Catégorie', 'Licence Type', 'Club Sportif']
important_col_french = ['Nom affiché', 'Sexe', 'Date de Naissance', 'Catégorie', 'Licence Type', 'Club Sportif']

important_col = important_col_french


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--inscrits_path', type=str)
    parser.add_argument('--ref_path', type=str)
    parser.add_argument('--save_path', type=str)
    opt = vars(parser.parse_args())

    print('-' * 50)
    print('Dossard à partir du fichier ' + opt['inscrits_path'] + ' en préparation...')
    print('-' * 50)

    # Open inscrits
    categories = ['7/8 ans', '9/10 ans', '11/12 ans', '13/14 ans', '15/16 ans', 'Scratch']
    inscrits = {}

    jeunes_9_16 = pd.read_excel(opt['inscrits_path'], sheet_name="JEUNES 9- 16 ans HF")

    for i in categories:
        if i == "Scratch":
            inscrits[i] = pd.read_excel(opt['inscrits_path'], sheet_name="ADULTES HF")
        elif i == "7/8 ans":
            inscrits["7/8 ans"] = pd.read_excel(opt['inscrits_path'], sheet_name="JEUNES 7-8 ans HF")
        else:
            inscrits[i] = jeunes_9_16[jeunes_9_16['Catégorie'] == i]

    # Get ranking
    name = ['Chrono - 7 8 ans', 'Chrono - 9 10 ans', 'Chrono - 11 12 ans', 'Chrono - 13 14 ans', 'Chrono - 15 16 ans', 'Chrono - Scratch']
    name_bis = ['Chrono - 78 ans', 'Chrono - 910 ans', 'Chrono - 1112 ans', 'Chrono - 1314 ans', 'Chrono - 1516 ans', 'Chrono - Scratch H']
    references = {}
    for i,j,k in zip(name, categories, name_bis):
        try:
            with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    df = pd.read_excel(opt['ref_path'], sheet_name=i)
        except:
            with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    df = pd.read_excel(opt['ref_path'], sheet_name=k)
        references[j] = df
        
    #print(references['Scratch'])

    dossards = {}
    with pd.ExcelWriter(opt['save_path']) as writer: 
        for i in categories:
            meg = MiseEnGrille(inscrits[i], references[i])
            if i == 'Scratch':
                dossards[i] = meg.get_dossard()
                dossards[i].to_excel(writer, sheet_name=clean_excel(i))
            else:
                dossards[i] = meg.get_dossard()
                dossards[i] = get_UCD_top(meg.get_dossard())
                dossards[i].to_excel(writer, sheet_name=clean_excel(i))

    with pd.ExcelWriter(opt['save_path'][:-5] + '_light.xlsx') as writer: 
        for i in categories:
            meg = MiseEnGrille(inscrits[i], references[i])
            print(i)
            if i == 'Scratch':
                dossards[i] = meg.get_dossard()[important_col]
                dossards[i].to_excel(writer, sheet_name=clean_excel(i))
            else:
                dossards[i] = meg.get_dossard()[important_col]
                #dossards[i] = get_UCD_top(meg.get_dossard())[important_col]
                dossards[i].to_excel(writer, sheet_name=clean_excel(i))

    print('-' * 50)
    print('Dossard sauvegardés ici: ' + opt['save_path'])
    print('-' * 50)
