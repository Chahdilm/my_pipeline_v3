
import pandas as pd 
import matplotlib.pyplot as plt

from bin.set_log import * 





def mrr_at_k(df, ks, methods):
    """
    Calcule le MRR pour chaque méthode et chaque k.

    Pour chaque patient et méthode, on prend la rangée où is_rdi=='y' (rang réel),
    puis on définit
      reciprocal_rank = 1/rank  if rank <= k
                        0          otherwise

    On fait la moyenne de ces valeurs sur tous les patients de la méthode.

    Retourne un DataFrame avec colonnes :
      ['k','method','nb_rdi_tot','sum_reciprocal','MRR']
    """
    # get the rank of the rdi depending on the method
    truths = (
        df.loc[:, ['patient','method','rank']]
        .drop_duplicates(subset=['patient','method'])
    )

    results = []
    for k in ks:
        for method in methods:
            # get patients related to the method 
            tr_m = truths[truths['method'] == method].copy()
            nb_rdi_tot = tr_m.shape[0]

            results.append({
                'k':               k,
                'method':          method,
                'nb_rdi_tot':      0,
                'sum_reciprocal':  0.0,
                'MRR':             float('nan')
            })
    

            # calcul of the reciprocal rank depending on k 
            #   reciprocal_rank = 1/rank  if rank <= k
            #                      0          otherwise
            tr_m['reciprocal_rank'] = tr_m['rank'].apply(
                lambda r: 1.0/r if r <= k else 0.0
            )

            # 5) Somme et moyenne
            sum_rr = tr_m['reciprocal_rank'].sum()
            mrr    = tr_m['reciprocal_rank'].mean()

            results.append({
                'k':               k,
                'method':          method,
                'nb_rdi_tot':      nb_rdi_tot,
                'sum_reciprocal':  sum_rr,
                'MRR':             mrr
            })

    return pd.DataFrame(results)



def harmonic_mean(data):
 
    if not data:
        raise ValueError("Data list must not be empty")
    if any(x <= 0 for x in data):
        raise ValueError("All values must be positive to compute harmonic mean")
    
    n = len(data)

    reciprocals = []
    for x in data:
        reciprocals.append(1.0 / x)
    reciprocal_sum = sum(reciprocals)

    return n / reciprocal_sum


 
def hm_at_k(df, ks, methods):

    # 1) Extraire (patient, method, rank) sans doublons
    truths = (
        df.loc[:, ['patient','method','rank']]
          .drop_duplicates(subset=['patient','method'])
    )

    results = []
    for k in ks:
        for method in methods:
            tr_m = truths[truths['method'] == method].copy()
            nb_rdi_tot = tr_m.shape[0] # denominator

            # filteration by k 
            tr_m = tr_m[tr_m['rank'] <= k]

            # sum of the reciprocal rank
            sum_rr = tr_m['rank'].apply(lambda r: 1.0/r).sum()

            # 5) Harmonic mean = nombre d'items / somme des réciproques
            if sum_rr > 0:
                h_mean = nb_rdi_tot / sum_rr
            else:
                h_mean = float('nan')

            results.append({
                'k':               k,
                'method':          method,
                'nb_rdi_tot':      nb_rdi_tot,
                'sum_reciprocal':  sum_rr,
                'harmonic_mean':   h_mean
            })

    return pd.DataFrame(results)




# df_compare_rank = pd.read_excel('/home/maroua/Bureau/wip/my_pipeline_v2/output/rarw/0.3/RARW_3_2_2_2_1_concat_matrix.xlsx',index_col = 0)
# nb_rdi_tot = df_compare_rank.shape[0] # denominator

# # sum of the reciprocal rank
# sum_rr = df_compare_rank['rank'].apply(lambda r: 1.0/r).sum()

# # 5) Harmonic mean = nombre d'items / somme des réciproques
# if sum_rr > 0:
#     h_mean = nb_rdi_tot / sum_rr
# else:
#     h_mean = float('nan')

#param_2 = 'and'
                                   

rsd_type = "withdupli_noontologyX"
folder_pd4 = "productmai2024_all_vectors_withontologyX"


# df_rarw= pd.read_excel('/home/maroua/Bureau/wip/my_pipeline_v2/output//rarw/RARW_3_2_2_2_1_concat_matrix.xlsx', index_col=0)
# df_rarw.columns = ['patient','RD','score','rarw']
# df_rarw = df_rarw[['patien t','RD','rarw']]



# print(f"\nSTART  10.10_mean_rank_mrr.py")
namefile  =f"{PATH_OUTPUT}compare_rank_{folder_pd4}_{rsd_type}.xlsx"

# df_compare_rank = pd.read_excel(namefile, index_col=0)


type_bench = "benchmark_all_OBG_vector"
# benchmark_all_OBG_vector
# benchmark_all_OBG
# compare_rank_benchmark_OBG
# compare_rank_benchmark_ascendant_descendant
# compare_rank_benchmark_vector
df_compare_rank = pd.read_excel(f"{type_bench}.xlsx",index_col = 0) # namefile


methods = df_compare_rank.columns.tolist()[2:]

# df_compare_rank =df_compare_rank[["patient","RD",

#   '3_2_2_2_1_rsd_resnik_n_productmai2024_all_vectors_withontologyX',
#   '1_1_1_1_1_rsd_resnik_n_productmai2024_all_vectors_withontologyX',

#  'Resnik (symmetric)'
# ]]   
# df_compare_rank = df_compare_rank.merge(df_rarw, on=['patient','RD'],how='outer')


# df_compare_rank =df_compare_rank[["patient","RD",
#   '1_1_1_1_1_rsd_resnik_n_productmai2024_with_rsdinRA_ontologyX',
#   '1_1_1_1_0_rsd_resnik_n_productmai2024_with_rsdinRA_ontologyX',

# # faire taire les tag peu frequent
# # '2.74_5.21_9.96_12.36_3.07_funSimAvg_resnik_n_productmai2024_expo_croissante',
# # #  '0.01_0.60_0.92_1_0.15_funSimAvg_resnik_n_productmai2024_multiple_test',
# # #  '0.01_0.60_0.92_1_0.15_funSimMax_resnik_n_productmai2024_multiple_test',

# # faire taire les tag frequent
# # #  '0.36_0.19_0.11_0.08_0.32_funSimAvg_resnik_n_productmai2024_n_ontologyX',
# # #  '0.98_0.18_0.01_0_0.77_funSimAvg_resnik_n_productmai2024_avec_e',
# # '0.98_0.18_0.01_0_0.77_funSimMax_resnik_n_productmai2024_avec_e',

# # 1 - f
# #'0.99_0.77_0.65_0.63_0.94_funSimAvg_resnik_n',
# # mettre en avant les frequence intermediare
# # #  '5.16_0.90_0.46_0.39_2.54_funSimAvg_resnik_n_productmai2024_multiple_test',
# # #  '5.16_0.90_0.46_0.39_2.54_funSimMax_resnik_n_productmai2024_multiple_test',

# # mettre en avant les frequent intermediaire sans idf
# # #  '1.2_0.9_0.7_0.6_1_funSimAvg_resnik_n_productmai2024_with_rsdinRA',
# # #  '1.2_0.9_0.7_0.6_1_funSimMax_resnik_n_productmai2024_with_rsdinRA',
# # '1.2_0.9_0.7_0.6_1_rsd_resnik_n_productmai2024_with_rsdinRA',

# #  '1_1_1_1_0_funSimAvg_resnik_n_productmai2024_with_rsdinRA',
# #  '1_1_1_1_0_funSimMax_resnik_n_productmai2024_with_rsdinRA',
# #  '1_1_1_1_0_rsd_resnik_n_productmai2024_with_only_rsd',
# #  '1_1_1_1_0_rsd_resnik_y_productmai2024_with_rsdinRA',
# #  '1_1_1_1_1_funSimAvg_resnik_n_productmai2024_multiple_test',
# #  '1_1_1_1_1_funSimMax_resnik_n_productmai2024_multiple_test',
# #  '1_1_1_1_1_rsd_resnik_n_productmai2024_with_rsdinRA',

#  'Resnik (asymmetric)',
#  'Resnik (symmetric)',
#     'rarw'
# ]]      

       
methods = df_compare_rank.columns.tolist()[2:]

df_rank_melt = df_compare_rank.melt(
    id_vars=['patient', 'RD'],
    value_vars=methods,
    var_name='method',
    value_name='rank'
)

df_hm_all = hm_at_k(df_rank_melt, [145], methods)
df_hm_all.to_excel(f"hm_{type_bench}.xlsx")
 
##############################################################################
## Un autre script 

print(f"START  8_plot_mrr_rdi")

ks = list(range(0, 50, 5))

df_hm_at_k = hm_at_k(df_rank_melt, ks, methods)

df_mrr_at_k = mrr_at_k(df_rank_melt, ks, methods)
df_mrr_at_k=df_mrr_at_k.dropna()

####################################################""
cmap   = plt.get_cmap('nipy_spectral', len(methods))
colors = cmap(np.arange( len(methods)))

# Courbe MRR  per k 
plt.figure(figsize=(20,10))
for i, method in enumerate(methods):
    sub = df_hm_at_k[df_hm_at_k['method']==method]
    plt.plot(
        sub['k'], sub['harmonic_mean'],
        marker='o', linestyle='-',
        color=colors[i],
        label=method
    )

plt.title('harmonic_mean depending on k rank')
plt.xlabel('rank')
plt.ylabel('harmonic_mean')
# make sure your x‐ticks match the k values
plt.xticks(df_hm_at_k['k'].unique())

plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(
    title='Method',
    loc='upper left',
    bbox_to_anchor=(1.02, 1),
    borderaxespad=0
)
plt.tight_layout()
plt.savefig(f"{PATH_OUTPUT}/hm_{type_bench}.png", dpi=300)
# plt.savefig(f"{PATH_OUTPUT}/mrr_{rsd_type}_{folder_pd4}.png", dpi=300)

plt.show()

print(f"line plot mrr saved ")


print(f"END  8_plot_mrr_rdi")

