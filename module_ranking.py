from utils import clean_club, rank2point
import numpy as np


class Ranking:
    def __init__(self, grille, meg=False):
        self.grille = grille
        self.meg = meg
        self.interesting_columns = ['Nom affiché', 'Categorie', 'Sexe', 'Club']
    
    def add_first_ranking(self, df):
        self.rank = df
        self.rank.loc[:,'Classement_1'] = self.rank['Classement'].apply(lambda x: rank2point(x, self.grille))
        self.rank['tot'] = self.rank['Classement_1']
        self.rank = self.rank[self.interesting_columns + ['tot', 'Classement_1']]
        
    def add_ranking(self, df, K):
        self.rank = self.merge_ranking(self.rank, df, K)
        
    def return_rank(self):
        return self.rank
    
    def merge_ranking(self, df_1, df_2, K):
        #df_2 = df_2.dropna(subset=["1 - Ligne d'arrivée"])
        df_1['Display name'] = df_1['Nom affiché'].apply(clean_club)
        df_2 = df_2[self.interesting_columns + ['Classement']]
        df_2['Classement_' + str(K)] = df_2['Classement']
        df_2 = df_2.drop('Classement', axis=1)
        df_2['Display name'] = df_2['Nom affiché'].apply(clean_club)
        
        res = df_1.merge(df_2, on='Display name', how='outer', suffixes=('', '_' + str(K)))
        res['Classement_' + str(K)] = res['Classement_' + str(K)].apply(lambda x: rank2point(x, self.grille))

        res[['Classement_' + str(i) for i in range(1, K+1)] + ['tot']] = res[['Classement_' + str(i) for i in range(1, K+1)] + ['tot']].fillna(value=0)

        if self.meg:
            res['tot'] = np.maximum(res['Classement_' + str(K)], res['tot'])
        
        else:
            res['tot'] += res['Classement_' + str(K)]
        
        for i in self.interesting_columns:
            res[i] = res[i].combine_first(res[i + '_' + str(K)])
        
        res = res[self.interesting_columns + ['tot'] + ['Classement_' + str(i) for i in range(1, K+1)]].sort_values('tot', ascending=False)
        res = res.reset_index()
        res['Classement'] = res.index + 1
        res = res.drop('index', axis=1)
        return res
