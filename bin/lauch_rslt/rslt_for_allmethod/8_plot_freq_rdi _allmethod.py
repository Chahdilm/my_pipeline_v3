
"""
crée un dataframe a partir du folder xlsx 
metric_classif/with_rdi/xlsx/
merge tout les patients 
et je garde que l'info rdi ca me fait une global rdi par patient et method 


puis je prend cette df 
conter le nombre de fois ou rdi aparait dans le top 10 pour chaque méthode le faire tout les autre top (plus tard psk je dosi trouver une facon d'automatiser je pense reecrée le global classif icien donnant le choix 
)

"""
 

from bin.set_log import * 

###################################################""
## PROPORTION OF THE RD TOP N IN THE SAME GROUP AS RDI GROUP 
# Pour tout nos patients combien de maladies dans le top n sont dans le même groupe que la maladie d’intérêt ?
# rdi peut appartenir a plusieurs groupe different issu de la meme classif (ou de classif differente)


# # Set up argument parsing
# parser = argparse.ArgumentParser(description="Process inputs for the script.")

# # Arguments for file paths and file names
# parser.add_argument('--col_rank', type=str, required=True)
# parser.add_argument('--add_dot', type=str, required=True)
# parser.add_argument('--logic_patient', type=str, required=True)

# # Parse the arguments
# args = parser.parse_args()

# col_rank = args.col_rank  
# add_dot = args.add_dot  
# param_2 = args.logic_patient 

col_rank = 'rank' #'reciprocal_rank' # or rank 
add_dot = "y"


print(f"START  8_plot_freq_rdi")

rsd_type = "nodupli_noontologyX"


# df_compare_rank = pd.read_excel(f"{PATH_OUTPUT}compare_rank_productmai2024_all_vectors_withontologyX_withdupli_noontologyX.xlsx",index_col = 0)

df_compare_rank = pd.read_excel(f"benchmark_OBG.xlsx",index_col = 0)
df_rarw= pd.read_excel('/home/maroua/Bureau/wip/my_pipeline_v2/output//rarw/RARW_1_1_1_1_0_rsd_resnik_n_productmai2024_with_only_rsd.xlsx', index_col=0)
df_rarw.columns = ['patient','RD','score','rarw']
df_rarw = df_rarw[['patient','RD','rarw']]



methods = df_compare_rank.columns.tolist()[2:]




df_compare_rank =df_compare_rank[["patient","RD",
  '3_2_2_2_1_rsd_resnik_n_productmai2024_all_vectors_withontologyX',
  'Resnik (symmetric)'
]]                               
df_compare_rank = df_compare_rank.merge(df_rarw, on=['patient','RD'],how='outer')
#df_compare_rank.to_excel('final_compare_rank.xlsx')


list_patient_rsd =  df_compare_rank['patient'].tolist()
# param_2 = "and"
# if param_2 == "and":
#     list_patient_rsd =  df_compare_rank[(df_compare_rank['RSD'] >= 1) & df_compare_rank['RA'] >= 1]['patient'].tolist()
# elif param_2 == "or":
#     list_patient_rsd =  df_compare_rank[(df_compare_rank['RSD'] >= 1) | df_compare_rank['RA'] >= 1]['patient'].tolist()
# elif param_2 == "rsd_only":
#     list_patient_rsd =  df_compare_rank[(df_compare_rank['RSD'] >= 1) ]['patient'].tolist()
# elif param_2 == "ra_only":
#     list_patient_rsd =  df_compare_rank[df_compare_rank['RA'] >= 1]['patient'].tolist()

# df_compare_rank = df_compare_rank[df_compare_rank["patient"].isin(list_patient_rsd)]

methods = df_compare_rank.columns.tolist()[2:]

df_rank_melt = df_compare_rank.melt(
    id_vars=['patient', 'RD'],
    value_vars=methods,
    var_name='method',
    value_name='rank'
)

 

df_rank_melt['reciprocal_rank'] = 1/ df_rank_melt['rank']

list_method = df_rank_melt['method'].drop_duplicates().tolist()

## reflexion au final je vais cliver top 50 vu que rsd est limiter a ca pour comparer 
# et je fais un boxplot solo de RA apres 
df_rdi = df_rank_melt[df_rank_melt['rank']<= 10]

rank_value = []
labels = []
subsets = []
for onem in list_method:
    # Start builind boxplot
    rank_value.append( df_rdi[(df_rdi['method'] == onem)][col_rank])
    labels.append(onem)
    # for dots
    subsets.append(df_rdi[(df_rdi['method'] == onem)])

#cmap   = plt.get_cmap('nipy_spectral', len(methods))
#colors = [cmap(i) for i in range(len(labels))]    
colors = ['#c4ff33','#78cbd6',"#51a524"] # tomato

fig, ax = plt.subplots()

bplot = ax.boxplot(rank_value,
                patch_artist=True,  # fill with color
                tick_labels=labels)  # will be used to label x-ticks
ax.tick_params(axis='x', rotation=80)
# fill with colors
for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)

if add_dot == 'y':

    list_nb_p= []
    for i, (sub, color) in enumerate(zip(subsets, colors), start=1):
        y = sub[col_rank].values
        x = np.random.normal(loc=i, scale=0.05, size=len(y))
        ax.scatter(x, y,c=color,edgecolor='black',linewidth=0.3,alpha=0.7,zorder=3)
        # for xi, yi, t in zip(x, y, sub['type']):
        #     ax.text(xi, yi, t,
        #     fontsize=8,
        #     ha='center', va='bottom',
        #     rotation=45)
        list_nb_p.append(len(y))

    
    ax.set_ylabel(f'{col_rank}')
    ax.set_title(f'{col_rank} distribution of RDIs and RDIs group of multiple method')
    plt.savefig(f"{PATH_OUTPUT}/boxplot_benchmark_OBG.png", dpi=300)
    plt.show()
else: 
    ax.set_ylabel(f'{col_rank} ')
    ax.set_title(f'{col_rank} distribution of RDIs and RDIs group of multiple method')
    # plt.savefig(f"{PATH_OUTPUT}/{col_rank}_distri_{rsd_type}.png", dpi=300)
    plt.savefig(f"{PATH_OUTPUT}/boxplot_benchmark_OBG.png", dpi=300)

    plt.show()






################################################################################
## boxplot above top 50  rsd 
df_rdi = df_rank_melt
rank_value = []
for method in list_method:
    s = df_rdi[df_rdi['method'] == method][col_rank]

    # 1) coerce non-finite → NaN
    s = s.replace([np.inf, -np.inf], np.nan)


    # 2) drop NaNs
    s = s.dropna()

    # 3) now safe to convert
    vals_int = s.astype(int).values
    rank_value.append(vals_int)

fig, ax = plt.subplots()
 
bplot = ax.boxplot(rank_value,
                patch_artist=True,  # fill with color
                tick_labels=labels)   
ax.tick_params(axis='x', rotation=80)

# fill with colors
for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)

ax.set_ylim(0,1000)
ax.set_ylabel(f'{col_rank} ')
ax.set_title(f'{col_rank} distribution of RDIs  multiple method')
plt.savefig(f"{PATH_OUTPUT}/{col_rank}_{rsd_type}.png", dpi=300)
plt.show()

print(f"end boxplot for the rank distribution of the rank depending on methods for rdi and group of orpha that belong to rdi ")



#############################################################################
# usage:
# ks = [5,10,15,20,50]
# methods = ['RA','RARW','RSD']
# match_rdi_grouprdi = freq_at_k(df_global_classif, ks, methods)



# # On suppose que df_results contient les colonnes : k, method, Group_recall, RDI_recall
# for metric in ['Group_freq', 'RDI_freq']:
#     plt.figure()
#     for m in methods:
#         sub = match_rdi_grouprdi[match_rdi_grouprdi['method'] == m]
#         plt.plot(sub['k'], sub[metric], label=m)  # trace la courbe pour chaque méthode
#     plt.xlabel('k')                             # étiquette de l’axe des abscisses
#     plt.ylabel('Frequence')                        # étiquette de l’axe des ordonnées
#     title = 'Freq de groupe' if metric=='Group_freq' else 'Freq RDI'
#     plt.title(f'{title} en fonction de k')      # titre du graphique
#     plt.legend()                                # affiche la légende
#     #plt.show()

#     plt.savefig(f"{PATH_OUTPUT_COMPARE_RSLT}/{metric}.png", dpi=300)
print(f"end build line plot for group orpha and rdi depending ont the methods")

print(f"END  8_plot_freq_rdi")
 