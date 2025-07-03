

from bin.set_log import * 

print(f"START  6_make_it_global")
t0 = time.perf_counter()

os.makedirs(PATH_OUTPUT_COMPARE_GLOBAL , exist_ok=True)

path_xlsx = PATH_OUTPUT_COMPARE_METRIC_CLASSIF + "/xlsx/"
 
list_patient = os.listdir(path_xlsx)
list_patient_f = []
for onep in list_patient:
    if '~' not in onep:
        list_patient_f.append(onep)


list_df1 = []
list_df2 = []
list_df3 = []
list_df4 = []
for one_p in list_patient_f:
    df_patient = pd.read_excel(path_xlsx + one_p ,sheet_name='patient',index_col=0)
    df_rdi = pd.read_excel(path_xlsx + one_p ,sheet_name='rdi',index_col=0)

    df_couple = pd.read_excel(path_xlsx + one_p  ,sheet_name='couple',index_col=0)
    df_classif_grp_rd = pd.read_excel(path_xlsx + one_p ,sheet_name='classif',index_col=0)


    list_df1.append(df_patient)
    list_df2.append(df_rdi)
    list_df3.append(df_couple)
    list_df4.append(df_classif_grp_rd)


df_global_patient = pd.concat(list_df1)
df_global_rdi = pd.concat(list_df2)
df_global_couple= pd.concat(list_df3)
df_global_classif = pd.concat(list_df4)

## save en mode global sans filtration
df_global_classif.to_excel(PATH_OUTPUT_COMPARE_GLOBAL + "/global_classif.xlsx")
df_global_rdi.to_excel(PATH_OUTPUT_COMPARE_GLOBAL + "/global_rdi.xlsx")
df_global_couple.to_excel(PATH_OUTPUT_COMPARE_GLOBAL + "/global_couple.xlsx")
df_global_patient.to_excel(PATH_OUTPUT_COMPARE_GLOBAL + "/global_patient.xlsx")


logger.info(f"END  6_make_it_global done in {time.perf_counter() - t0:.1f}s")
print(f"END  6_make_it_global done in {time.perf_counter() - t0:.1f}s")
