
from bin.set_log import * 
print(f"START  1_compare_rank_global")
t0 = time.perf_counter()
#############################################
### input
#############################################
col_cdf_patient=  "patients" # patient  patients
col_cdf_rd = "RDs" # ORPHAcode  RDs
rsd_type = "withdupli_noontologyX"
# withdupli_noontologyX
# nodupli_noontologyX
# nodupli_withontologyX

col_cdf_patient=  "patients" # patient  patients
col_cdf_rd = "RDs" # ORPHAcode  RDs

#############################################
# Set up argument parsing
parser = argparse.ArgumentParser(description="Process inputs for the script.")

# Arguments for file paths and file names
parser.add_argument('--ra', type=str, required=True)
parser.add_argument('--rarw', type=str, required=True)
parser.add_argument('--alpha', type=str, required=True)

# Parse the arguments
args = parser.parse_args()
 
ra = args.ra  
rarw = args.rarw  
alpha = args.alpha

# ra = "3_2_2_2_1_rsd_resnik_n_productmai2024_all_vectors_withontologyX"
# rarw = "RARW_1_1_1_1_1_concat_matrix"
# alpha=str(0.04)
 
#############################################
os.makedirs(PATH_OUTPUT_COMPARE_RSLT,exist_ok=True)
 

patients = pd.read_excel(PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER_v2,index_col=0)
list_patients = patients[COL_DF_PATIENT_PATIENT].drop_duplicates().tolist()
couple_patients = patients[[COL_DF_PATIENT_PATIENT,COL_DF_PATIENT_ORPHACODE]].drop_duplicates()
couple_patients.columns  = [col_cdf_patient,col_cdf_rd]

##############################################""""


##############################################""""

dict_df_ra_sm = {}
 

df_sm = pd.read_excel(PATH_OUTPUT_SM + ra + ".xlsx",index_col=0 )
list_sm = df_sm["patients"].drop_duplicates().tolist()

 
## HERE IF I WANT TO ADD ANOTHER SM 
dict_df_ra_sm[ra] = df_sm

## a list of df from rsd A2
## get the list 
# output_files_hpo2025_rsdpd4mai2025_withduplicate_noontologyX
#output_files_hpo2025_rsdpd4mai2025_noduplicate_noontologyX
#output_files_hpo2025_rsdpd4mai2025_noduplicate_withontologyX
path_rsdA2 = '/home/maroua/Bureau/wip/only_rsd_step/only_jar/SolveRD/output_files_hpo2025_rsdpd4mai2025_withduplicate_noontologyX/'
list_rsdA2 =  os.listdir(path_rsdA2)
dict_rsd = {}
for op in list_rsdA2:
    if ('tsv' in op):
        op_split = op.split("_")
        
        op_rslt = op_split[3].replace('.tsv','')
        try:
            rsds_patients = pd.read_csv(path_rsdA2 + op,sep='\t')
            # merge two col into one 
            # rsds_patients['ORPHAcode_merged'] = rsds_patients['ORPHAcode'].combine_first(rsds_patients['ORPHAcode_child'])
            rsds_patients_tronq = rsds_patients[["phenopacket","ORPHAcode","rank"]]
            rsds_patients_tronq.columns  = [col_cdf_patient,col_cdf_rd,"rank"]
            list_rsd = rsds_patients_tronq[col_cdf_patient].drop_duplicates().tolist()
            dict_rsd[op_rslt] = rsds_patients_tronq
        except KeyError :
            logger.info(f'{op} empty')

        logger.info(f"for the rsdA2: {op_rslt} : {op_split[1]} + {op_split[2]}, nb of patient is {len(list_rsd)}")


######################################################
#### compare patient match
 

patient_available_everywhere = list_rsd
list_rank_all = []
all_interactions = set()
for one_patient in patient_available_everywhere:
    #print(one_patient)
    one_couple = couple_patients[couple_patients[col_cdf_patient]==one_patient]
    patient = one_couple[col_cdf_patient].values[0]
    if one_patient != patient:
        print(f"patient name different ? {one_patient}\t{patient}")

    rdi = one_couple[col_cdf_rd].values[0]
    
    for key,rsds_patients_tronq in dict_rsd.items():
        # extract rank from rsds
        matches_rsd = pd.merge(one_couple, rsds_patients_tronq, on=[col_cdf_patient, col_cdf_rd])
        if matches_rsd.empty:
            rank_rsd = np.nan
        else:
            rank_rsd = int(matches_rsd['rank'].values[0])
        list_rank_all.append((one_patient,rdi,key,rank_rsd))

    for key,df_sm  in dict_df_ra_sm.items():
        ## extract rank from sm
        matches_sm = pd.merge(one_couple, df_sm, on=[col_cdf_patient, col_cdf_rd])
        if matches_sm.empty:
            rank_sm = np.nan
        else:
            rank_sm = int(matches_sm['rank'].values[0])
        
        list_rank_all.append((one_patient,rdi,key,rank_sm))




df = pd.DataFrame(list_rank_all,columns=["patient","RD","metric",'rank'])

df_compare_rank_wide = df.pivot(index=['patient', 'RD'], 
                   columns='metric', 
                   values='rank')\
            .reset_index()
    
df_compare_rank = df_compare_rank_wide[["patient","RD",ra,"Resnik (symmetric)"]]

path_rw_patient =os.path.join(PATH_OUTPUT_FOLDER_RW,str(alpha))
df_rarw= pd.read_excel(path_rw_patient +"/"+ rarw+".xlsx", index_col=0)
df_rarw.columns = ['patient','RD','score','rarw']
df_rarw = df_rarw[['patient','RD','rarw']]


df_compare_rank = df_compare_rank.merge(df_rarw, on=['patient','RD'],how='outer')
df_compare_rank.columns = ["patient","RD","RA","RSD","RARW"]
 
df_compare_rank.to_excel(PATH_OUTPUT_DF_COMPARE_RANK_DIRECT)
logger.info(f"END  1_compare_rank_global done in {time.perf_counter() - t0:.1f}s")
print(f"END  1_compare_rank_global done in {time.perf_counter() - t0:.1f}s")




