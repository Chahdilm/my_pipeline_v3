from bin.set_log import * 


# # Set up argument parsing
# parser = argparse.ArgumentParser(description="Process inputs for the script.")

# # Arguments for file paths and file names
# parser.add_argument('--topn', type=int, required=True)
# parser.add_argument('--logic_patient', type=str, required=True)

# # Parse the arguments
# args = parser.parse_args()
# param_1 = args.topn  
# param_2 = args.logic_patient  



# param_1 = 4215
# param_2 = 'and' # and 'or', 'rsd_only', 'ra_only'


rsd_type = "withdupli_noontologyX"

# print(f"\nSTART  10.10_mean_rank_mrr.py")
df_compare_rank = pd.read_excel(f"{PATH_OUTPUT}compare_rank_productmai2024_all_vectors_withontologyX_withdupli_noontologyX.xlsx",index_col = 0)

df_rarw= pd.read_excel('/home/maroua/Bureau/wip/my_pipeline_v2/output//rarw/RARW_1_1_1_1_0_rsd_resnik_n_productmai2024_with_only_rsd.xlsx', index_col=0)
df_rarw.columns = ['patient','RD','score','rarw']
df_rarw = df_rarw[['patient','RD','rarw']]



methods = df_compare_rank.columns.tolist()[2:]




df_compare_rank =df_compare_rank[["patient","RD",
  '3_2_2_2_1_rsd_resnik_n_productmai2024_all_vectors_withontologyX',
  'Resnik (symmetric)'
]]                               
df_compare_rank = df_compare_rank.merge(df_rarw, on=['patient','RD'],how='outer')

# ## only top 50
# df_compare_rank['RSD'] = df_compare_rank["RSD"].where(df_compare_rank["RSD"] <= param_1, np.nan)
# df_compare_rank['RA'] = df_compare_rank["RA"].where(df_compare_rank["RA"] <= param_1, np.nan)
# print(f'BASE : Nb patient : {len(df_compare_rank)}')

# if param_2 == "and":
#     list_patient_rsd =  df_compare_rank[(df_compare_rank['RSD'] >= 1) & df_compare_rank['RA'] >= 1]['patient'].tolist()
# elif param_2 == "or":
#     list_patient_rsd =  df_compare_rank[(df_compare_rank['RSD'] >= 1) | df_compare_rank['RA'] >= 1]['patient'].tolist()
# elif param_2 == "rsd_only":
#     list_patient_rsd =  df_compare_rank[(df_compare_rank['RSD'] >= 1) ]['patient'].tolist()
# elif param_2 == "ra_only":
#     list_patient_rsd =  df_compare_rank[df_compare_rank['RA'] >= 1]['patient'].tolist()


methods = df_compare_rank.columns.tolist()[2:]


   
 
# Define rank bins
bins = [-1, 5, 10, 20, 50, 1e6]
labels = ['Top 5%', 'Top 10%', 'Top 20%', 'Top 50%', 'Below 50%']

# Prepare result aggregation
results = []
for method in methods:

    df_compare_rank['rank_bin'] = pd.cut(df_compare_rank[method], bins=bins, labels=labels)
    bin_perc = df_compare_rank['rank_bin'].drop_duplicates().tolist()

    # harmonic mean rank 
    # row = {}
    # for perc in bin_perc:
    #     list_rank_f_perbin = df_compare_rank[df_compare_rank['rank_bin'] == perc][method]
    #     reciprocals = []
    #     for x in list_rank_f_perbin:
    #         if not np.isnan(x):
    #             reciprocals.append(1.0 / x)

    #     reciprocal_sum = sum(reciprocals)
    #     row[perc] = reciprocal_sum

    # Mean rank 
    count_per_bin = df_compare_rank['rank_bin'].value_counts().reindex(labels, fill_value=0)
    not_found = df_compare_rank[method].isna().sum()    
    row = count_per_bin.to_dict()
    # row['Not found'] = not_found

    row['method'] = method
    results.append(row)

# Create DataFrame
df_plot = pd.DataFrame(results).set_index('method')

# Order for stacked bar
stack_order = [ 'Below 50%', 'Top 50%', 'Top 20%', 'Top 10%', 'Top 5%'] #'Not found',


# Plot with labels
fig, ax = plt.subplots(figsize=(10, 6))
bottom = [0] * len(df_plot)

colors = plt.get_cmap('tab20').colors
color_map = dict(zip(stack_order, colors[:len(stack_order)]))

for i, bin_label in enumerate(stack_order):
    values = df_plot[bin_label]
    ax.bar(df_plot.index, values, bottom=bottom, label=bin_label, color=color_map[bin_label])
    
    for j, (val, b) in enumerate(zip(values, bottom)):
        if val > 0:
            ax.text(j, b + val / 2, str(int(val)), ha='center', va='center', fontsize=9, color='black')
    
    bottom = [b + v for b, v in zip(bottom, values)]

plt.title(f" Percentage of rank of patient's RDI ")
plt.ylabel("Number of Patients")
plt.xlabel("Method")
plt.xticks(rotation=60)
plt.legend(title='Ranking Bin', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
#plt.savefig(f"{PATH_OUTPUT}/barplot_percentage_{rsd_type}.png", dpi=300)
plt.show()


