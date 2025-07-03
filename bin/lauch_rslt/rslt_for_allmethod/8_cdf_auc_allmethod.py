

from bin.set_log import * 


from sklearn.metrics import auc as sk_auc
############################################################
#####            extract all cdf df file               #####
############################################################



print(f"START  8_cdf_auc_mrr.py")
rsd_type = "withdupli_noontologyX"
# withdupli_noontologyX
# nodupli_noontologyX
# nodupli_withontologyX

# # Set up argument parsing
# parser = argparse.ArgumentParser(description="Process inputs for the script.")

# # Arguments for file paths and file names
# parser.add_argument('--dropna', type=str, required=True)
# parser.add_argument('--top50', type=str, required=True)
# parser.add_argument('--logic_patient', type=str, required=True)

# # Parse the arguments
# args = parser.parse_args()

# param1 = args.dropna  
# param2 = args.top50  
# param3 = args.logic_patient  

 
# param1 = 'y' # drop_na ok 
# param2 = 'n' # top50 only

# param1 = 'y' # drop_na ok 
# param2 = 'y' # top50 only

param1 = 'n' # drop_na ok 
param2 = 'y' # top50 only

# param1 = 'n' # drop_na ok 
# param2 = 'n' # top50 only

rank_f = 15                               
                                   
                                   
                                   
folder_pd4 = "productmai2024_all_vectors_withontologyX" # _withontologyX

# print(f"\nSTART  10.10_mean_rank_mrr.py")
namefile =  PATH_OUTPUT_DF_COMPARE_RANK_DIRECT
## CAD
namefile  ="/home/maroua/Bureau/wip/my_pipeline_v2/output/compare_rank_productmai2024_all_vectors_withontologyX_withdupli_noontologyX_CAD_v2.xlsx"
 

# df_rarw= pd.read_excel('/home/maroua/Bureau/wip/my_pipeline_v2/output//rarw/' \
# 'RARW_3_2_2_2_1_rsd_resnik_n_productmai2024_all_vectors_withontologyX_0.50.xlsx', index_col=0)
# df_rarw.columns = ['patient','RD','score','rarw']
# df_rarw = df_rarw[['patient','RD','rarw']]



# benchmark_all_OBG
# benchmark_all_OBG_vector
# compare_rank_benchmark_ascendant_descendant
# compare_rank_benchmark_vector
df_compare_rank = pd.read_excel(f"benchmark_all_OBG_vector.xlsx",index_col = 0) # namefile

methods = df_compare_rank.columns.tolist()[2:]
 
df_compare_rank =df_compare_rank[["patient","RD",
 'Resnik (symmetric)',
'2_2_2_2_1_rsd_resnik_n_productmai2024_controvector_withontologyX',
'1_1_1_1_0_rsd_resnik_n_productmai2024_controvector_withontologyX',
'1_1_1_1_1_rsd_resnik_n_productmai2024_controvector_withontologyX',

'5_4_3_2_1_rsd_resnik_n_productmai2024_controvector_withontologyX',
'2_1_1_0_0_rsd_resnik_n_productmai2024_controvector_withontologyX',

'1_1_0_0_0_rsd_resnik_n_productmai2024_controvector_withontologyX',
'2_1_0_0_0_rsd_resnik_n_productmai2024_controvector_withontologyX',


]]  
                                 
                                   
df_compare_rank.columns = ["patient","RD",
'RSD',
'2,2,2,2,1',
'1,1,1,1,0',
'1,1,1,1,1',

'5,4,3,2,1',
'2,1,1,0,0',
'1,1,0,0,0',
'2,1,0,0,0'
]

# 3) create a “filtered” version where any rank >10 → NaN
methods = df_compare_rank.columns.tolist()[2:]
df_compare_rank_filtered = df_compare_rank[['patient', 'RD']].join(
    df_compare_rank[methods].where(df_compare_rank[methods] <= rank_f)
)
# grab a colormap with plenty of colors
cmap   = plt.get_cmap('nipy_spectral', len(methods))
colors = cmap(np.arange(len(methods)))

colors = ['black',"green","darkorange",'orchid',"red","gray","maroon","blue"]

spacing = 0

plt.figure(figsize=(12,6))
for i, col in enumerate(methods):
    if param1 == 'y':
        data_rank = df_compare_rank_filtered[col].dropna()
    else:
        data_rank = df_compare_rank_filtered[col]

    n_total   = len(data_rank)
    n_missing = data_rank.isna().sum()
    missing_pct = n_missing / n_total

    x = np.sort(data_rank)
    y = np.arange(1, len(x)+1) / n_total
    y_offset = y + i * spacing

    # ---- compute AUC of the empirical CDF
    auc_score = sk_auc(x, y)

    label_info = (
        f"{col}" # Nb Patients={len(x)}, missing={missing_pct:.1%}, 
        # f"AUC={auc_score:.3f}"
    )
    plt.step(
        x, y_offset, where='post',
        color=colors[i],
        label=label_info,
         alpha=0.6,         # set transparency (0 = invisible, 1 = opaque)

    )

if param2 == 'y':
    plt.xlim(0, rank_f)

plt.xlabel('r = rank')
plt.ylabel('P(rank ≤ r)')
#plt.title('Cumulative distribution of the candidate ORPHAcode rank across GSSM')
#plt.title('Cumulative distribution of the candidate ORPHAcode rank with FunSimMaxAsym Resnik GSSM')
plt.title('Cumulative distribution of the candidate ORPHAcode rank with the optimal GSSM\n (FunSimMaxAsym + Resnik)  and without removal of subsum HPO terms')
plt.legend(
    #title=f'Methods dropna={param1}, top50={param2}',
    loc='best',
    #bbox_to_anchor=(1.02, 1),
    borderaxespad=0.5,
)

plt.grid(True)
plt.tight_layout(rect=[0, 0, 0.75, 1])
### plt.savefig(f"{PATH_OUTPUT}/cdf_dropna_{param1}_top15_{param2}_{folder_pd4}_{rsd_type}_cad.png", dpi=300)
#plt.savefig(f"{PATH_OUTPUT}/benchmark_all_gssm_top8.svg", dpi=300)
plt.savefig(f"{PATH_OUTPUT}/benchmark_all_GSSM_vector_top8.svg", dpi=300)
plt.savefig(f"{PATH_OUTPUT}/benchmark_all_GSSM_vector_top8.png", dpi=300)

plt.show()

print(f"END  8_cdf_auc_mrr.py")
