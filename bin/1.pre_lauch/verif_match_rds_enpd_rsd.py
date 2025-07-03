from bin.set_log import * 


df_enpd_raredisease = pd.read_excel(PATH_OUTPUT_DF_PRODUCT4,index_col=0)
list_enpd = df_enpd_raredisease['ORPHAcode'].drop_duplicates()
print(f'nb RD enpd4 {len(list_enpd)}, frequency available {set(df_enpd_raredisease['hpo_frequency'])}')


df_rsd_raredisease = pd.read_excel(PATH_OUTPUT_DF_PRODUCT4_RSD, index_col=0)
list_rsd = df_rsd_raredisease['ORPHAcode'].drop_duplicates()
print(f'nb RD rsd {len(list_rsd)}, frequency available {set(df_rsd_raredisease['hpo_frequency'])}')

################################################################################

print(f"interaction rsd/enpd : {len(set(list_rsd).intersection(list_enpd))}")


df_enpd_raredisease_f = pd.read_excel(PATH_OUTPUT_DF_PRODUCT4_MATCH_RSD, index_col=0)
list_rsd_f = df_enpd_raredisease_f['ORPHAcode'].drop_duplicates()
print(f'nb RD rsd {len(list_rsd_f)}, frequency available {set(df_enpd_raredisease_f['hpo_frequency'])}')


print(f"interaction rsd/enpd filtre : {len(set(list_rsd_f).intersection(list_enpd))}")


################################################################################
## Test if all RDs patient are in pd4 rsd and enpd
## Patients 
df_patient = pd.read_excel(PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER,index_col=0) 
# PATH_OUTPUT_DF_PATIENT PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER
#df_patient = df_patient[df_patient['phenopacket'] == 'P0001068']  #P0001068 

patients_id_list = df_patient["phenopacket"].drop_duplicates().tolist()    
patients_rds_list = df_patient["Disease"].drop_duplicates().tolist() 


print(f"interaction patient - rsd: {len(set(list_rsd).intersection(patients_rds_list))}")
print(f"interaction patient - enpd: {len(set(list_enpd).intersection(patients_rds_list))}")
print(f"interaction patient - enpd f : {len(set(list_rsd_f).intersection(patients_rds_list))}")

set(patients_rds_list).difference(list_rsd_f)

################################################################################

