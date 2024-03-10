import argparse
import os
import pandas as pd

from utils import clean_club, cat2sheet
from module_ranking import Ranking
import warnings

pd.options.mode.chained_assignment = None

grille = [100, 95, 90, 86, 82, 79, 76, 73, 70, 68, 66, 64, 62, 60, 59, 58, 57, 56, 55, 54, 53, 52, 51, 50,
          49, 48, 47, 46, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25,
          24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

cat_meg = ['Chrono - 78 ans',
        'Chrono - 1112 ans',
        'Chrono - 910 ans',
        'Chrono - 1314 ans',
        'Chrono - 1516 ans',
        'Chrono - Scratch H',
        'Chrono - Scratch F']

cat_gen = [ 'Chrono - 1719 ans H', 'Chrono - 1719 ans F',
            'Chrono - 2029 ans H', 'Chrono - 2029 ans F',
            'Chrono - 3039 ans H', 'Chrono - 3039 ans F',
            'Chrono - 4049 ans H', 'Chrono - 4049 ans F',
            'Chrono - 5059 ans H', 'Chrono - 50 ans et plus F',
            'Chrono - 60 ans et plus H',
            'Chrono - Tandem']

cat = cat_meg + cat_gen


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--ref_folder', type=str)
    parser.add_argument('--save_path', type=str)
    parser.add_argument('--meg', default=False, type=bool)
    opt = vars(parser.parse_args())

    if opt['meg']: grille += [1/i for i in range(2, 300)]

    else: grille += [0 for i in range(300)]

    print('-' * 50)
    print('Classement général à partir des classements dans ' + opt['ref_folder'] + ' en préparation...')
    print('-' * 50)

    ref_list = sorted([os.path.join(opt['ref_folder'], i) for i in os.listdir(opt['ref_folder']) if i.endswith('.xlsx')])

    references = {}
    with pd.ExcelWriter(opt['save_path']) as writer: 
        for i,j in enumerate(cat):
            ranking = Ranking(grille, opt['meg'])
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    df = pd.read_excel(ref_list[0], sheet_name=j)
                    df = df[['Classement', 'Nom affiché', 'Categorie', 'Sexe', 'Club', "1 - Ligne d'arrivée"]]
            except:
                print('No data for categorie:', j, " in", ref_list[0])
                df = pd.DataFrame(columns=['Classement', 'Nom affiché', 'Categorie', 'Sexe', 'Club', "1 - Ligne d'arrivée"])
    
            ranking.add_first_ranking(df)

            for k in range(1, len(ref_list)):
                try:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        df = pd.read_excel(ref_list[k], sheet_name=j)
                except:
                    print('No data for categorie:', j, " in", ref_list[k])
                    df = pd.DataFrame(columns=['Classement', 'Nom affiché', 'Categorie', 'Sexe', 'Club', "1 - Ligne d'arrivée"])

                ranking.add_ranking(df, k+1)

            ref = ranking.return_rank()
            ref['Display name'] = ref['Nom affiché'].apply(clean_club)
            ref.set_index("Classement", inplace=True)
            references[j] = ref

            references[j].to_excel(writer, sheet_name=j)

    print('-' * 50)
    print('Classement sauvegardés ici: ' + opt['save_path'])
    print('-' * 50)
