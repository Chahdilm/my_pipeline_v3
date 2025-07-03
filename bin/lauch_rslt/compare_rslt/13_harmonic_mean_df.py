from bin.set_log import * 


 
def hm_at_k(df, ks, methods,col_rank):

    # 1) Extraire (patient, method, rank) sans doublons
    truths = (
        df.loc[:, ['patient','method',col_rank]]
          .drop_duplicates(subset=['patient','method'])
    )

    results = []
    for k in ks:
        for method in methods:
            tr_m = truths[truths['method'] == method].copy()
            nb_rdi_tot = tr_m.shape[0] # denominator

            # filteration by k 
            tr_m = tr_m[tr_m[col_rank] <= k]

            # sum of the reciprocal rank
            sum_rr = tr_m[col_rank].apply(lambda r: 1.0/r).sum()

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






print(f"START  13_harmonic_mean_df")
t0 = time.perf_counter()
# #############################################
# Set up argument parsing
parser = argparse.ArgumentParser(description="Process inputs for the script.")

# Arguments for file paths and file names
parser.add_argument('--alpha', type=str, required=True)

# Parse the arguments
args = parser.parse_args()
 
alpha = args.alpha

#############################################
# PATH_OUTPUT_COMPARE_GLOBAL = '/home/maroua/Bureau/wip/my_pipeline_v2/output//compare_rank_1_1_1_1_1_concat_matrix_0.5//global/'
# alpha=str(0.5)
#######################*  
df_global_classif = pd.read_excel(PATH_OUTPUT_COMPARE_GLOBAL + "/global_classif.xlsx",index_col=0)

df_f =  df_global_classif[["type","method","group_id","rd_id","rank","is_rdi"]]
df_f = df_f.drop_duplicates()
list_patient = df_f['type'].unique()
list_method = df_f['method'].unique()
 

all_interaction = []
for onep in list_patient:
    mini_df = df_f[df_f['type'] == onep]
    # get the RDI
    rdi_ids = mini_df.loc[mini_df["is_rdi"] == "y", "rd_id"].unique()

    for onem in list_method:
        mini_mini_df = mini_df[mini_df['method'] == onem]
        # get the RDI group 
        list_rdi_groups = mini_mini_df[mini_mini_df["rd_id"].isin(rdi_ids)]['group_id'].unique()
        # get the RD with the same group as rdi 
        rd_match_group_rdi = mini_mini_df[mini_mini_df['group_id'].isin(list_rdi_groups)]['rd_id'].unique()

        # get the df 
        df_match_group_rdi = mini_mini_df[mini_mini_df['rd_id'].isin(rd_match_group_rdi)].drop_duplicates()
        df_match_group_rdi_without_rdi = df_match_group_rdi[df_match_group_rdi['is_rdi'] == "n"]
        df_match_group_rdi_only_rdi = df_match_group_rdi[df_match_group_rdi['is_rdi'] == "y"]

        # get the rank of each RDs
        df_for_hm = df_match_group_rdi[['rd_id','rank']].drop_duplicates()
        df_for_hm_without_rdi = df_match_group_rdi_without_rdi[['rd_id','rank']].drop_duplicates()
 
        df_for_hm_rdi = df_match_group_rdi_only_rdi[['rd_id','rank']].drop_duplicates()

        # extract ranks
        ranks_gp = df_for_hm['rank']
        try:
            ranks_gp_no_rdi = df_for_hm_without_rdi['rank']
        except IndexError:
            ranks_gp_no_rdi = []

        ranks_rdi = df_for_hm_rdi['rank'].values[0]

        try:
            # hm
            h_mean_rd_same_group_rdi = len(ranks_gp) / sum(1.0 / r for r in ranks_gp)
            h_mean_rd_same_group_no_rdi = len(ranks_gp_no_rdi) / sum(1.0 / r for r in ranks_gp_no_rdi)

            logger.info(f"{onep} - {onem}\tHarmonic mean (manual calculation): {h_mean_rd_same_group_rdi}")
        except ZeroDivisionError:
            # h_mean_rd_same_group_rdi = 0
            h_mean_rd_same_group_no_rdi = 0
            logger.info(f"{onep} - {onem}\t ZeroDivisionError")

        #for oner in ranks_gp:
        all_interaction.append((onep,onem,h_mean_rd_same_group_rdi,h_mean_rd_same_group_no_rdi,ranks_rdi))

df_hm_general = pd.DataFrame(all_interaction,columns=['patient','method','hm','hm_group_without_rdi','hm_rdi'])

df_hm_rdi  = df_hm_general[['patient','method','hm_rdi']].drop_duplicates()
df_hm_group  = df_hm_general[['patient','method','hm']]
df_hm_group_no_rdi  = df_hm_general[['patient','method','hm_group_without_rdi']]



# Compute the average HM for each method
method_hm_group = (
    df_hm_group
    .groupby('method', as_index=False)['hm']
    .mean()
    .rename(columns={'hm': 'mean_hm'})
)

# Compute the average HM for each method
method_hm_group_without_rdi= (
    df_hm_group_no_rdi
    .groupby('method', as_index=False)['hm_group_without_rdi']
    .mean()
    .rename(columns={'hm_group_without_rdi': 'mean_hm'})
)

# hm_group = hm_at_k(df_hm_general, [len(list_patient)], list_method,'hm')
# hm_rdi = hm_at_k(df_hm_general, [len(list_patient)], list_method,'hm_rdi')

method_hm_group_without_rdi.to_excel(PATH_OUTPUT_COMPARE_RSLT + "hm_group_without_rdi_rarw_" + str(alpha)+ ".xlsx")

method_hm_group.to_excel(PATH_OUTPUT_COMPARE_RSLT + "hm_group_rarw_" + str(alpha)+ ".xlsx")


logger.info(f"END  13_harmonic_mean_df done in {time.perf_counter() - t0:.1f}s")
print(f"END  13_harmonic_mean_df done in {time.perf_counter() - t0:.1f}s")
################################################

df_compare = pd.read_excel(PATH_OUTPUT_COMPARE_RSLT + "compare_rank_method.xlsx",index_col=0)
all_interecation = []
rank_rsd = df_compare['RSD'].astype(float)
harmonic_mean = len(rank_rsd) / (1.0 / rank_rsd).sum()
all_interecation.append(('RSD',harmonic_mean))
rank_rsd = df_compare['RA'].astype(float)
harmonic_mean = len(rank_rsd) / (1.0 / rank_rsd).sum()
all_interecation.append(('RA',harmonic_mean))
rank_rsd = df_compare['RARW'].astype(float)
harmonic_mean = len(rank_rsd) / (1.0 / rank_rsd).sum()
all_interecation.append(('RARW',harmonic_mean))

df_hm_general = pd.DataFrame(all_interecation,columns=['method','mean_hm'])  


df_hm_general.to_excel(PATH_OUTPUT_COMPARE_RSLT + "hm_rdi_rarw_" + str(alpha)+ ".xlsx")



