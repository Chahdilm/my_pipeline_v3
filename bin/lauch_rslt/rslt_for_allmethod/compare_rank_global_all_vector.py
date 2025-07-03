


from bin.set_log import * 
print(f"START  1_compare_rank_global")
os.makedirs(PATH_OUTPUT_COMPARE_RSLT,exist_ok=True)

#############################################
### input
#############################################
col_cdf_patient=  "patients" # patient  patients
col_cdf_rd = "RDs" # ORPHAcode  RDs
rsd_type = "withdupli_noontologyX"
# withdupli_noontologyX
# nodupli_noontologyX
# nodupli_withontologyX

folder_pd4 = "productmai2024_controvector_withontologyX"

# PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER_v2
patients = pd.read_excel(PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER_WITH_ONTOLOGYX,index_col=0) 
list_patients = patients[COL_DF_PATIENT_PATIENT].drop_duplicates().tolist()
couple_patients = patients[[COL_DF_PATIENT_PATIENT,COL_DF_PATIENT_ORPHACODE]].drop_duplicates()
couple_patients.columns  = [col_cdf_patient,col_cdf_rd]
 
dict_df_ra_sm = {}

list_ra= os.listdir(PATH_OUTPUT_SM)
list_ra_sm = []
for ra in list_ra:
    if ("xlsx" in ra) and ('~' not in ra): #folder_pd4 in ra:
        list_ra_sm.append(ra)
 
for ra in list_ra_sm:
    if ('xlsx' in ra) and ('CDF' not in ra):
        ra_noext=  ra.rsplit('.', 1)[0] # remore the extension
        ra_list=  ra_noext.split('_') # remore the extension
        ra_rslt = '_'.join(ra_list[:])

        ## list of df from RA but with different vector 
        df_sm = pd.read_excel(PATH_OUTPUT_SM + ra,index_col=0 )
        list_sm = df_sm["patients"].drop_duplicates().tolist()
        dict_df_ra_sm[ra_rslt] = df_sm
 
        ## LOAD CDF file 
        # df_cdf = pd.read_excel(PATH_OUTPUT_SM + "/CDF_" + ra ,index_col=0 )
        # list_cdf = df_cdf["patients"].drop_duplicates().tolist()
        
        print(f"for ra : {ra_rslt}, nb of patient is {len(list_sm)}")


 

# ## RW
# for ra in list_ra_sm:
#     if ('xlsx' in ra) and ('CDF' not in ra):
#         ra_noext=  ra.rsplit('.', 1)[0] # remore the extension
#         ra_list=  ra_noext.split('_') # remore the extension
#         ra_rslt = '_'.join(ra_list[:])

#         ## list of df from RA but with different vector 
#         df_sm = pd.read_excel(PATH_OUTPUT_SM + ra,index_col=0 )
#         list_sm = df_sm["patients"].drop_duplicates().tolist()
#         dict_df_ra_sm[ra_rslt] = df_sm
 
#         ## LOAD CDF file 
#         # df_cdf = pd.read_excel(PATH_OUTPUT_SM + "/CDF_" + ra ,index_col=0 )
#         # list_cdf = df_cdf["patients"].drop_duplicates().tolist()
        
#         print(f"for ra : {ra_rslt}, nb of patient is {len(list_sm)}")


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
            print(f'{op} empty')

        print(f"for the rsdA2: {op_rslt} : {op_split[1]} + {op_split[2]}, nb of patient is {len(list_rsd)}")


######################################################
#### compare patient match
 

patient_available_everywhere = list_rsd#list(set(list_cdf).intersection(list_rsd) )
list_rank_all = []
all_interactions = set()
for one_patient in patient_available_everywhere:
    print(one_patient)
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
    

 
# df_compare_rank_wide.to_excel(f"{PATH_OUTPUT}compare_rank_{folder_pd4}_{rsd_type}_CAD_v2.xlsx")
df_compare_rank_wide.to_excel(f"benchmark_all_OBG_vector.xlsx")

print(f"END  1_compare_rank_global")


 
