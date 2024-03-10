import argparse
import os
import pandas as pd

from utils import clean_excel, clean_club, get_UCD_top

from module_dossard import MiseEnGrille
from module_ranking import Ranking

grille = [100, 95, 90, 86, 82, 79, 76, 73, 70, 68, 66, 64, 62, 60, 59, 58, 57, 56, 55, 54, 53, 52, 51, 50,
          49, 48, 47, 46, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25,
          24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

grille += [0 for i in range(300)]

grille = [300 - i for i in range(301)] 
grille += [0 for i in range(300)]

important_col_english = ['First name', 'Last name', 'Sexe', 'Date de Naissance', 'Catégorie', 'Licence Type', 'Club Sportif']
important_col_french = ['Prénom', 'Nom', 'Sexe', 'Date de Naissance', 'Catégorie', 'Licence Type', 'Club Sportif']

important_col = important_col_french


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--inscrits_path', type=str)
    parser.add_argument('--ref_folder', type=str)
    parser.add_argument('--save_path', type=str)
    opt = vars(parser.parse_args())

    print('-' * 50)
    print('Dossard à partir du fichier ' + opt['inscrits_path'] + ' en préparation...')
    print('-' * 50)

    ref_list = [os.path.join(opt['ref_folder'], i) for i in os.listdir(opt['ref_folder']) if i.endswith('.xlsx')]

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
    name = ['Chrono - 7 8 ans', 'Chrono - 9 10 ans', 'Chrono - 11 12 ans', 'Chrono - 13 14 ans', 'Chrono - 15 16 ans', 'Chrono']
    references = {}
    for i,j in zip(name, categories):
        ranking = Ranking(grille)
        if i == 'Chrono':
            df = pd.read_excel(ref_list[0], sheet_name=i)
            df = df[df['Course'].isin(['Scratch H', 'Scratch F'])]
            df = df.reset_index()
            df['Classement'] = df.index + 1
        else:
            df = pd.read_excel(ref_list[0], sheet_name=i)

        ranking.add_first_ranking(df)

        for k in range(1, len(ref_list)):
            if i == 'Chrono':
                df = pd.read_excel(ref_list[k], sheet_name=i)
                df = df[df['Course'].isin(['Scratch H', 'Scratch F'])]
                df = df.reset_index()
                df['Classement'] = df.index + 1
            else:
                df = pd.read_excel(ref_list[k], sheet_name=i)
            
            ranking.add_ranking(df, k+1)

        ref = ranking.return_rank()
        ref['Display name'] = ref['Nom affiché'].apply(clean_club)
        references[j] = ref

    print(references['Scratch'])

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
            if i == 'Scratch':
                dossards[i] = meg.get_dossard()[important_col]
                dossards[i].to_excel(writer, sheet_name=clean_excel(i))
            else:
                dossards[i] = meg.get_dossard()
                dossards[i] = get_UCD_top(meg.get_dossard())[important_col]
                dossards[i].to_excel(writer, sheet_name=clean_excel(i))

    print('-' * 50)
    print('Dossard sauvegardés ici: ' + opt['save_path'])
    print('-' * 50)
