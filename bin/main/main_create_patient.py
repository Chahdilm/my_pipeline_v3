

from bin.set_log import * 
from bin.classes.dataset import * 






if __name__ == "__main__":

    # -------------------------------------------------------------------------------
    #                        1. DATA LOADING AND PREPROCESSING
    #    - Load data from input phenopacket solverd
    #    - Kepp comfirmed one 
    #    - Normalize/Standardize data
    #-------------------------------------------------------------------------------
        
    ################################################################################
    ##### Load patients from json solveRD and filter keep only comfirmed       #####
    ################################################################################
    # notused_path = ''
    # build_patient = DataSet(PATH_INPUT_PATIENTS_FOLDER,notused_path) 
    # df_patient = build_patient.build_patients_df()
    # df_patient_confirmed = build_patient.filter_df_keep_comfirmed_only(PATH_INPUT_PATIENTS_FC,df_patient,'phenopacket')
    # df_patient_confirmed = df_patient_confirmed.rename(columns={"Disease found ORPHA":"Disease"})
    # # df_patient_confirmed.to_excel(PATH_OUTPUT_DF_PATIENT)
    # # df_patient.to_excel(PATH_OUTPUT + "patient_solverd/patients_from_phenopacket_solverd.xlsx")



    patients_raw = os.listdir(PATH_INPUT_PATIENTS_FOLDER_ONTOLOGYX)

    list_case_HPO = []

    for onefile in patients_raw:
        with open(PATH_INPUT_PATIENTS_FOLDER_ONTOLOGYX+str(onefile),'r',encoding = 'utf8') as file_phenopacket_result:
            one_phenopacket_result = json.load(file_phenopacket_result)

            id_phenopacket = one_phenopacket_result['id']
            
            phenotype_list = one_phenopacket_result['phenotypes']
            for onep in phenotype_list:
                #print(onep)
                list_case_HPO.append((id_phenopacket,onep['type']['id'],onep['type']['label']))


    df_raw_info = pd.DataFrame(list_case_HPO, columns=["phenopacket",'hpo_id','hpo_label'])


    patients = pd.read_excel(PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER_v2,index_col=0)

    df_final = df_raw_info.merge(patients,on = ["phenopacket",'hpo_id'])
    df_final = df_final[["phenopacket","hpo_id","Disease","Disease_type"]]
    #df_final.to_excel(PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER_WiITH_ONTOLOGYX)
