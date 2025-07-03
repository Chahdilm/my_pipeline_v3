
""""
1. profilphenotypique entre patient et maladie  compare_rank_factors_part2.py
 

a partir de ca je peux caractériser mon patients et son maladie associé 
(chercher dans la literature en plus de ce que j'aurai fait avec gtp)

2. etude de la similarité entre maladie 


3. Argument expliquant le ranking 
A partir de la comparaison patient- maladie et des maladies tu top 10 entre elle je vais pouvoir expliquer le ranking otenue pour chaque methods

compare_rank_method.xlsx
                           step sm  rw
128	P0001068	ORPHA:610	43	43	43																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																										

et regarder pour les patients dont le rdi n'est pas dans le top 50 dans le cas des steps 
nb je fais remonter de patient ?
qualité pour chaque patient remonter pq ells sont remonter cohérence orpha patient 
pourquoi la new methode la fait remonter  
 

"""
"""

Pour évaluer le porfil on utilise cinq facteur :
1. Nombre de terme HPO communs 
combien de termes HPO du patient figurent également parmi les annotations HPO caractéristiques de la maladie correspondante​

2. Profondeur moyenne des termes HPO 
La profondeur ontologique moyenne des termes HPO communs, mesurée dans la hiérarchie de l’HPO. La profondeur d’un terme correspond à la longueur du chemin le reliant au nœud racine 

3. Variabilité sémantiqu de la profondeur des termes HPO communs entre patient et maladie 
mesure la diversité des termes HPO communs du patient. Un ensemble de termes concentrés dans le même domaine phénotypique (par ex. tous liés au système musculaire) aura une variabilité faible, tandis que des termes couvrant plusieurs systèmes anatomiques distincts (par ex. à la fois neurologiques et cardiovasculaires) auront une variabilité plus élevée. Cette variabilité peut être quantifiée par exemple via l’entropie de la distribution des termes parmi les catégories haut-niveau de l’HPO, ou par la distance ontologique moyenne entre chaque paire de termes.
La variabilité sémantique design le degre de diversité dans l'information semntique, si les termes HPO chez le patient on tous une profondeur similaire alors lephenotype est cohenre ou homogène 
Une forte variabilité (c’est-à-dire, une grande dispersion des profondeurs) indique que le phénotype est plus diversifié — certains termes sont très spécifiques tandis que d’autres sont plus généraux.
Une faible variabilité indique une présentation clair du profil potentiellement. alors qu'un ensemble hétérogene monte un phenotype plus complexe ou peu complexe ayant besoin d'un évaluation cliniqe (peut etre ?)
Un ensemble homogène de caractéristiques phénotypiques (faible variabilité) pourrait indiquer une présentation claire de la maladie.

Au contraire, un ensemble hétérogène (forte variabilité) peut signaler un phénotype plus complexe, nécessitant une évaluation clinique plus approfondie.

Lorsque l’on compare différentes méthodes de classement ou que l’on établit un profil phénotypique du patient, mesurer la variabilité sémantique aide à identifier les cas où une méthode particulière pourrait être plus performante parce que les symptômes sont concentrés à un niveau de spécificité similaire.
Donc nous ce qu'on veut est une variabilité proche de 0 pour montrer que les terme hpo en communs ont une profondeur proche du profil de orpha pas trop de dispersion.

La variabilité depend de la profondeur moyenne

4.Information content moyen (IC moyen) 
L’IC moyen des termes HPO communs, reflétant leur spécificité.
Un terme fréquent dans de nombreuses maladies aura un IC faible (peu informatif), tandis qu’un terme rare ou très spécifique à peu de maladies aura un IC élevé (beaucoup d’information). Par exemple, « déficience intellectuelle » (HP:0001249) apparaît dans 971 maladies différentes, reflétant un terme très général (IC faible)​, alors que « fistule anopérinéale » (HP:0005218) n’est présente que dans 1 maladie connue (IC très élevé)​

5.Proportion de symptômes généraux
la proportion de termes HPO communs considérés comme peu spécifiques, c’est-à-dire des termes très généraux. On peut définir un terme « général » par une profondeur ontologique faible (proche de la racine) ou un IC faible (fréquent dans de nombreuses maladies)​. Par exemple, « hypotonie musculaire » (HP:0001252) est un symptôme général présent dans plus de 1000 maladies différentes​. Cette proportion est calculée comme le nombre de termes communs du patient qui sont généraux (selon ces critères) divisé par le nombre total de termes communs.



Interprétation pour P0001068 et ORPHA:610
P0001068 a un nombre de terme hpo de 67 quant a ORPHA:610 on est sur 26 terme hpo.
(je dois aussi trouver une facon d'anyler le profil pour un patient/orpha uniquement)

Le patient a 6 termes HPO en communs avec sa maldie, et 23 qui sont dans au moins la meme branche que ceux de la maladie
donc soit plus précis ou moins précis.
Pour ces terme en communs ils sont present dans 3 branches différentes donc il y a une hétérogénitée (que dire de plus ? ... )

La profondeur moyenne est de 5.84 (quel est la profondeur max min ? je dois savoi rcb y'a de  niveau dans hpo ontology) 

La moyenne de l'IC est de 4 (encore une fois quel est le min max et la moyenne de IC global ?) 

La variabilité sémantique est  les profondeurs des termes HPO partagés (c'est-à-dire leur niveau de spécificité dans l'ontologie) varient de manière modérée autour de leur moyenne

La proportion general des terme est e 12% donc c'est des termes peu communs (revoir précisement comment cela se calcul )
donc suite a la variabilité et a la proprotion general la dispersion est donc des termes plutot precis.

Pour conclure le patient a un cheveuchement de 6 sur les 26 HPO terme present dans la maladie
Le patient exprime des manaifestations plutot (geeral/spécifique ?) de la maladie.

Je dois faire une verification manuelle de tout ca 

Je dois faire la distribution de tout  les facteurs pour pouvoir comparer cf gtp
"""


from bin.set_log import * 
 
print(f"START  3_profile_rdi_stat")
t0 = time.perf_counter()

# Chargement des données patient-HPO-maladie
df = pd.read_excel(PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER_WITH_ONTOLOGYX,index_col=0)
df_rd = pd.read_excel(PATH_OUTPUT_DF_PRODUCT4_MATCH_RSD,index_col=0)
# Installation (si nécessaire)
# !pip install hpo3 pandas odfpy

hpo_id_all = []
# iterating all HPO terms
for term in Ontology:
    hpo_id_all.append(term)


ic_map = {}
for term in hpo_id_all:
    ic_map[term.id] = term.information_content['orpha']

 
# Préparer un DataFrame vide pour les résultats
results = []

# Grouper par patient
patients = df['phenopacket'].unique()

for patient in patients:
    patient_df = df[df['phenopacket'] == patient]
    patient_hpos = set(patient_df['hpo_id'])

    disease = patient_df['Disease'].iloc[0]
    disease_hpos = set(df_rd[df_rd['ORPHAcode'] == disease]['hpo_id'])

    
 
    exact_matches = patient_hpos & disease_hpos
    branch_matches = set()

    # Trouver les correspondances de branche (ancêtres ou descendants communs)
    for phpo in patient_hpos:
        try :
            term_p = Ontology.get_hpo_object(phpo)
            for dhpo in disease_hpos:
                term_d = Ontology.get_hpo_object(dhpo)

                if phpo != dhpo and (term_p.child_of(term_d) or term_p.parent_of(term_d)):
                    branch_matches.add(phpo)
        except RuntimeError:
            pass

    nb_exact_matches = len(exact_matches)
    nb_branch_matches = len(branch_matches)

    all_matches = exact_matches | branch_matches

    if all_matches:
        categories = set()
        for hpo in all_matches:
            term = Ontology.get_hpo_object(hpo)
            for cat in term.categories:
                categories.add(cat.id)
            
        nb_cat =   len(categories)
        try:
            depths = []
            for hpo in all_matches:
                term = Ontology.get_hpo_object(hpo)
                depths.append(term.shortest_path_to_root())
            mean_depth = sum(depths) / len(depths)

        except :
            depths = []
            mean_depth = 0


        ic_values = [ic_map.get(hpo, 0) for hpo in all_matches]
        mean_ic = sum(ic_values) / len(ic_values)

        # Variabilité (ici simplifiée par écart-type des profondeurs)
        variability = pd.Series(depths).std() if len(depths) > 1 else 0

        # Termes généraux (IC < 2 considéré comme général, seuil ajustable)
        general_terms = [ic for ic in ic_values if ic < 2]
        proportion_general = len(general_terms) / len(ic_values)

    else:
        mean_depth = 0
        mean_ic = 0
        variability = 0
        proportion_general = 0

    results.append({
        'patient': patient,
        "nb_hpo_patient": len(patient_hpos),
        'disease': disease,
        "nb_hpo_disease" : len(disease_hpos),
        'nb_exact_matches': nb_exact_matches,
        'nb_branch_matches': nb_branch_matches,
        'nb_hpo_categorie': nb_cat,
        'mean_depth': mean_depth,
        'semantic_variability': variability,
        'mean_IC': mean_ic,
        'proportion_general_terms': proportion_general
    })
 



# Conversion des résultats en DataFrame
results_df = pd.DataFrame(results)
results_df_stats = results_df.describe()
results_df.to_excel(PATH_OUTPUT_COMPARE_RSLT + "patient_rdi_profil.xlsx")
results_df_stats.to_excel(PATH_OUTPUT_COMPARE_RSLT + "patient_rdi_profil_stats.xlsx")


logger.info(f"Export profile phenotypic profile for rdi\n END  3_profile_rdi_stat done in {time.perf_counter() - t0:.1f}s")
print(f"Export profile phenotypic profile for rdi \n END  3_profile_rdi_stat done in {time.perf_counter() - t0:.1f}s")







 