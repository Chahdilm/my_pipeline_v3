
"""
la je vais etudier le profil phenotypique de chaque patient associé a une maladie et le profil phenotypique de la maladie 
(apres besoins d'une correction manuelle)

Exemple : (pas le mielleur mais balec)
1. profilphenotypique entre patient et maladie 

dans ptient_confirmed_solved.xlsx j'ai acces au termes HPO
	phenopacket	status	Orphanet	OMIM	ern	gene	type_gene	variant	hpo_id	hpo_label	Gene_p	Disease																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																			
0	P0001068	SOLVED	no_info	no_info	ERN-EURO-NMD	COL6A3	CAUSATIVE	no_info	HP:0000365	Hearing impairment	COL6A3	ORPHA:610																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																			
1	P0001068	SOLVED	no_info	no_info	ERN-EURO-NMD	COL6A3	CAUSATIVE	no_info	HP:0000405	Conductive hearing impairment	COL6A3	ORPHA:610																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																			
2	P0001068	SOLVED	no_info	no_info	ERN-EURO-NMD	COL6A3	CAUSATIVE	no_info	HP:0000407	Sensorineural hearing impairment	COL6A3	ORPHA:610																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																			
3	P0001068	SOLVED	no_info	no_info	ERN-EURO-NMD	COL6A3	CAUSATIVE	no_info	HP:0000410	Mixed hearing impairment	COL6A3	ORPHA:610																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																			
4	P0001068	SOLVED	no_info	no_info	ERN-EURO-NMD	COL6A3	CAUSATIVE	no_info	HP:0000478	Abnormality of the eye	COL6A3	ORPHA:610																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																			
5	P0001068	SOLVED	no_info	no_info	ERN-EURO-NMD	COL6A3	CAUSATIVE	no_info	HP:0000501	Glaucoma	COL6A3	ORPHA:610																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																			
6	P0001068	SOLVED	no_info	no_info	ERN-EURO-NMD	COL6A3	CAUSATIVE	no_info	HP:0000508	Ptosis	COL6A3	ORPHA:610																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																			
7	P0001068	SOLVED	no_info	no_info	ERN-EURO-NMD	COL6A3	CAUSATIVE	no_info	HP:0000518	Cataract	COL6A3	ORPHA:610																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																			
ect ...


"""

## 1. evaluation du profil phenotypique de chaque patient et de sa maladie associé 

from bin.set_log import * 

def get_factor(df,name_col,name_col_hpo):
    resultats = []
    for element, group in df.groupby(name_col):
        # Récupérer les objets HPO pour tous les termes du patient

        hpo_patient = group[name_col_hpo]
        terms = []
        for onehpo in hpo_patient:  
            try : 
                terms.append(Ontology.get_hpo_object(onehpo))  
            except:
                #logger.info(f"{onehpo} Unknown HPO term")
                pass


        # 1. Nombre de termes HPO
        nb_terms = len(terms)


        # 2. Profondeurs des termes
        depths = []
        for term in terms:
            try : 
                depths.append(term.shortest_path_to_root())
            except  :
                #logger.info(f"{term.id} Unknown HPO term")
                pass


        mean_depth = float(np.mean(depths))
        semantic_var = float(np.std(depths))

        # 3. Distribution des branches
        try:
            categories = set()
            for hpo in terms:
                for cat in term.categories:
                    categories.add(cat.id) 
            nb_cat =   len(categories)
        except :
            nb_cat = 0


        # 3. Information content des termes
        ic_values = []
        for term in terms:
            ic_values.append(term.information_content['orpha'])
        mean_ic = float(np.mean(ic_values))

        # 4. Proportion de termes généraux (IC < 2)
        if nb_terms > 0:
            prop_general = sum(1 for ic in ic_values if ic < 2) / nb_terms
        else:
            prop_general = 0.0

        resultats.append([element, nb_terms, nb_cat, mean_depth, semantic_var, mean_ic, prop_general])
    
    # Construire le DataFrame agrégé
    df_profiles = pd.DataFrame(resultats, columns=[
        'element', 'nb_hpo_terms', "nb_hpo_categorie",'mean_depth', 
        'semantic_variability', 'mean_IC', 'proportion_general_terms'
    ])
    return df_profiles



print(f"START  3_profile_rd_patient_stat")
t0 = time.perf_counter()

# Chargement des données patient-HPO-maladie
df_patient = pd.read_excel(PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER_WITH_ONTOLOGYX,index_col=0)
df_rd = pd.read_excel(PATH_OUTPUT_DF_PRODUCT4_MATCH_RSD,index_col=0)

df_profiles_onep = get_factor(df_patient,"phenopacket",'hpo_id')




df_profiles_onep = get_factor(df_patient,"phenopacket",'hpo_id')
df_profiles_patient_stat = df_profiles_onep.describe()
df_profiles_onep.to_excel(PATH_OUTPUT_COMPARE_RSLT + "patient_profil.xlsx")
df_profiles_patient_stat.to_excel(PATH_OUTPUT_COMPARE_RSLT + "patient_profil_stats.xlsx")

df_profiles_rd = get_factor(df_rd,"ORPHAcode",'hpo_id')
df_profiles_rd_stat = df_profiles_rd.describe()
df_profiles_rd.to_excel(PATH_OUTPUT_COMPARE_RSLT + "rd_profil.xlsx")
df_profiles_rd_stat.to_excel(PATH_OUTPUT_COMPARE_RSLT + "rd_profil_stats.xlsx")

logger.info(f"Export profile phenotypic profile for rds/patients\nEND  3_profile_rd_patient_stat done in {time.perf_counter() - t0:.1f}s")
print(f"Export profile phenotypic profile for rds/patients\nEND  3_profile_rd_patient_stat done in {time.perf_counter() - t0:.1f}s")

############################################################################################

