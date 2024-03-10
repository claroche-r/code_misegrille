from utils import clean_club


class MiseEnGrille:
    def __init__(self, tab_inscrits, tab_ref):
        self.tab_inscrits = tab_inscrits
        self.tab_ref = tab_ref
        
    def start_list(self, regist, ref):
        try:
            regist['Display name'] = regist['Display name'].apply(clean_club)
        except:
            regist['Display name'] = regist['Nom affiché'].apply(clean_club)
            
        ref['Display name'] = ref['Display name'].apply(clean_club)

        #print(ref, regist)
        final = regist.merge(ref[['Display name', 'tot']], on='Display name', how='left')

        final = final.sort_values('tot', ascending=False).reset_index().drop('index', axis=1)
        final.index += 1
        return final
    
    def get_dossard(self):
        return self.start_list(self.tab_inscrits, self.tab_ref)
