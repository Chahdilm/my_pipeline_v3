from bin.set_log import * 

from sklearn.metrics import auc as sk_auc

def set_auc(nodrop,col_df):
    if nodrop == 'n' : 
        data_rank = col_df.dropna()
    else:
            
        data_rank = col_df

    # show the missing data (useful for RSD)
    n_total   = len(data_rank)
    n_missing = data_rank.isna().sum()
    missing_pct = n_missing / n_total

    data_col = data_rank.fillna(0)

    auc_val= np.sort(data_col)



    # AUC value
    if len(auc_val) >= 2:
        auc_var = sk_auc(np.sort(auc_val),  np.arange(1, len(np.sort(auc_val))+1) / n_total)
    else:
        # 0.0 no area when <2 points
        auc_var = 0.0
    print(f"\t\t Nb Patients={n_total}, missing={missing_pct:.1%}, AUC={auc_var}")

    return auc_var


param_2 = "ra_only"
vector_list=[ '1_1_0_1_0', '1_0_0_0_0', '1_1_0_0_0', '1_1_1_0_0', '1_1_1_1_0', '1_1_1_1_1', '2_1_1_1_1', '2_2_1_1_1', '2_2_2_1_1', '2_2_2_2_1', '3_2_2_2_1', '3_3_2_2_1', '3_3_3_2_1','4_3_3_2_1', '4_4_3_2_1', '5_4_3_2_1',]


scoring = []
for one_vector in vector_list:
    motif = 'resnik_n_all_product4_avril_2025_' + one_vector
    PATH_OUTPUT_COMPARE_RSLT = "/home/maroua/Bureau/wip/my_pipeline_v2/compare_rank_v1/" + "/compare_rank_" + motif + "/"
    PATH_OUTPUT_DF_COMPARE_RANK_DIRECT =PATH_OUTPUT_COMPARE_RSLT + "compare_rank_method.xlsx"

    df_compare_rank = pd.read_excel(PATH_OUTPUT_DF_COMPARE_RANK_DIRECT,index_col = 0)

    top_n = [5,10,20,50,4215]#[10,50,4215]
    for top_selected in top_n:

        methods = ['RSD','RA']

        for m in methods:
            # filter by top
            df_compare_rank_f = df_compare_rank[df_compare_rank[m] <= top_selected ] 
            # extract the patients from RSD
            if param_2 == "and":
                list_patient_rsd =  df_compare_rank[(df_compare_rank['RSD'] >= 1) & df_compare_rank['RA'] >= 1]['patient'].tolist()
            elif param_2 == "or":
                list_patient_rsd =  df_compare_rank[(df_compare_rank['RSD'] >= 1) | df_compare_rank['RA'] >= 1]['patient'].tolist()
            elif param_2 == "rsd_only":
                list_patient_rsd =  df_compare_rank[(df_compare_rank['RSD'] >= 1) ]['patient'].tolist()
            elif param_2 == "ra_only":
                list_patient_rsd =  df_compare_rank[df_compare_rank['RA'] >= 1]['patient'].tolist()

            # filter depending on the patient 
            df_compare_rank_f = df_compare_rank_f[df_compare_rank_f['patient'].isin(list_patient_rsd)]
            if top_selected == 4215:
                df_compare_rank_f = df_compare_rank.copy()

            nb_patient = len(df_compare_rank_f['patient'].drop_duplicates().tolist())

            ## MRR
            mmr_missing_val = (1/df_compare_rank_f[m]) 
            mmr_missing_val = mmr_missing_val.fillna(0)
            mmr_var = ((1/df_compare_rank_f[m]).mean(skipna=True),mmr_missing_val.mean(skipna=False))
 
            ## mean rank
            mean_var = ( df_compare_rank_f[m].mean(skipna=True),df_compare_rank_f[m].sum()/len(df_compare_rank_f))

            ## AUC
            print(f'\n{one_vector}\t{top_selected}\t{m} real tot Nb patient={len(df_compare_rank_f)}')
            # var = drop nan no 
            auc_var_y = set_auc('y',df_compare_rank_f[m])
            auc_var_n = set_auc('n',df_compare_rank_f[m])

            print(f"\t\t MRR with nan {mmr_var[1]}, without {mmr_var[0]}")
            print(f"\t\t Mean rank with nan {mean_var[1]}, without {mean_var[0]}")


            scoring.append({
                'vector': one_vector,
                'top':top_selected,
                'patient':nb_patient,
                'method' : m,
                'auc yes nan' :auc_var_y,
                #'auc no nan': auc_var_n,
                'mean yes nan' : mean_var[1],
                #'mean no nan' : mean_var[0],
                'mrr yes nan' : mmr_var[1],
                #'mrr no nan' : mmr_var[0],
                })


comparison_results = pd.DataFrame(scoring)
comparison_results.to_excel(PATH_OUTPUT + f'{param_2}_compare_score.xlsx')
# drop na oui , drop nan non 

  
# --- 1. Load and prepare data ---
# Adjust the path to your actual file location
df = comparison_results.copy()

# Clean column names
df.columns = [col.strip() for col in df.columns]

# --- 2. Split methods ---
df_ra = df[df['method'] == 'RA'].copy()
df_rsd = df[df['method'] == 'RSD'].copy()

# --- 3. Build comparison table across all shared vectors and tops ---
comparison = []
for top_val in sorted(df['top'].unique()):
    ra_top = df_ra[df_ra['top'] == top_val]
    rsd_top = df_rsd[df_rsd['top'] == top_val]
    shared = set(ra_top['vector']) & set(rsd_top['vector'])
    
    for vec in shared:
        ra = ra_top[ra_top['vector'] == vec].iloc[0]
        rsd = rsd_top[rsd_top['vector'] == vec].iloc[0]
        
        # Compare metrics
        better_auc = 'RA' if ra['auc yes nan'] > rsd['auc yes nan'] else ('RSD' if ra['auc yes nan'] < rsd['auc yes nan'] else 'Tie')
        better_mean = 'RA' if ra['mean yes nan'] < rsd['mean yes nan'] else ('RSD' if ra['mean yes nan'] > rsd['mean yes nan'] else 'Tie')
        better_mrr = 'RA' if ra['mrr yes nan'] > rsd['mrr yes nan'] else ('RSD' if ra['mrr yes nan'] < rsd['mrr yes nan'] else 'Tie')
        
        # Decide overall winner by priority
        if better_auc != 'Tie':
            winner = better_auc
        elif better_mean != 'Tie':
            winner = better_mean
        else:
            winner = better_mrr
        
        comparison.append({
            'top': top_val,
            'vector': vec,
            'n_ra': ra['patient'],
            'n_rsd': rsd['patient'],
            'better_auc': better_auc,
            'better_mean': better_mean,
            'better_mrr': better_mrr,
            'winner': winner
        })

df_comp = pd.DataFrame(comparison)
df_comp.to_excel(PATH_OUTPUT + f'{param_2}_compare_quali.xlsx')


# # 2) Loop over each 'top' threshold
# for top_val in sorted(df_comp['top'].unique()):
#     # Filter to this threshold
#     df_comp_top = df_comp[df_comp['top'] == top_val].copy()
    
#     # 3) Sort by RA patient count descending
#     df_comp_top = df_comp_top.sort_values(['n_ra','n_rsd'], ascending=False).reset_index(drop=True)
    
#     vectors = df_comp_top['vector']
#     x = np.arange(len(vectors))
#     width = 0.35
    
#     # Edge color: green if RA wins, red if RSD
#     edge_colors = df_comp_top['winner'].map({'RA':'green', 'RSD':'red'}).fillna('gray')
    
#     # 4) Create the grouped bar chart
#     fig, ax = plt.subplots(figsize=(12, 6))
#     bars_ra  = ax.bar(x - width/2, df_comp_top['n_ra'], width,
#                       label='RA patients', color='bisque',
#                       edgecolor=edge_colors, linewidth=2)
#     bars_rsd = ax.bar(x + width/2, df_comp_top['n_rsd'], width,
#                       label='RSD patients', color='lavender',
#                       edgecolor=edge_colors, linewidth=2)
    
#     # 5) Annotate counts on each bar
#     for bar in list(bars_ra) + list(bars_rsd):
#         h = bar.get_height()
#         ax.text(bar.get_x() + bar.get_width()/2, h + 1,
#                 str(int(h)), ha='center', va='bottom', fontsize=9)
    
#     # Formatting
#     ax.set_xticks(x)
#     ax.set_xticklabels(vectors, rotation=45, ha='right')
#     ax.set_ylabel("Number of Patients")
#     ax.set_title(f"Top-{top_val}: Patient counts per vector (sorted by RA, edge=winner)")
#     ax.legend()
#     ax.grid(axis='y', linestyle='--', alpha=0.5)
#     plt.tight_layout()
#     plt.show()




metrics = ['auc yes nan', 'mean yes nan', 'mrr yes nan']

for top_val in sorted(df['top'].unique()):
    df_top = df[df['top'] == top_val]
    
    # Find top 5 vectors based on ΔMRR
    pivot_mrr = (
        df_top
        .pivot(index='vector', columns='method', values='mrr yes nan')
        .dropna()
    )
    pivot_mrr['delta'] = pivot_mrr['RA'] - pivot_mrr['RSD']
    top_vectors = pivot_mrr['delta'].abs().sort_values(ascending=False).head(5).index
    
    # Subplots
    fig, axes = plt.subplots(1, len(metrics), figsize=(5*len(metrics), 4), sharey=False)
    for ax, metric in zip(axes, metrics):
        # build pivot for this metric
        pivot = df_top.pivot(index='vector', columns='method', values=metric).loc[top_vectors]
        pivot.plot(kind='bar', ax=ax, color=['skyblue','salmon'])
        
 
        # now annotate patient counts
        for i, vec in enumerate(top_vectors):
            n_ra  = int(df_top[(df_top.vector==vec)&(df_top.method=='RA')]['patient'].iloc[0])
            n_rsd = int(df_top[(df_top.vector==vec)&(df_top.method=='RSD')]['patient'].iloc[0])
            # bar positions: RA bar is at i-0.2, RSD at i+0.2 (approx)
            ax.text(i-0.2, ax.get_ylim()[0] + (ax.get_ylim()[1]*0.02),
                    f"n={n_ra}", ha='center', va='bottom', color='black', fontsize=6)
            ax.text(i+0.2, ax.get_ylim()[0] + (ax.get_ylim()[1]*0.02),
                    f"n={n_rsd}", ha='center', va='bottom', color='black', fontsize=6)
        ax.get_legend().remove()
        ax.set_title(f"Top-{top_val} | {metric.replace('yes nan','')}")
        ax.grid(axis='y', linestyle='--', alpha=0.5)
        ax.set(xlabel=None)

    handles, labels = axes[-1].get_legend_handles_labels()
    fig.legend(handles, labels,
            loc='lower center',
            ncol=2,
            frameon=False,
            bbox_to_anchor=(0.5, -0.02))
    plt.tight_layout()
    plt.show()

 
