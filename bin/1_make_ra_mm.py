from bin.set_log import * 
from bin.classes.sim_measure_cal import *

 
if __name__ == "__main__":

    #logger.info(f"#####################   START 1_make_ra")

    ############################################################
    #####                        Arg                       #####
    ############################################################

    index = sys.argv[1]  # 1 Unique identifier
    param_RD = sys.argv[2]  # "ORPHA:61" non constant parameter
    combine = sys.argv[3]
    method = sys.argv[4]
    is_freq = sys.argv[5] 
    pd4=sys.argv[6]
    vector_str = sys.argv[7]


        
    #######################################################################

    # index = 1 # 1 Unique identifier
    # param_RD = "ORPHA:610"  ##"ORPHA:61"  
    # combine = "rsd" #funSimMax funSimAvg  BMA
    # method = "resnik"
    # is_freq = 'n'
    # pd4 = "productmai2024_all_vectors_withontologyX"
    # vector_str = '3_2_2_2_1'
    #######################################################################

    vector_weight = [float(x)for x in vector_str.split('_')]
    param_RD_file = param_RD.replace(':',"-")


    # ################################################


    concat_config = f"{index}_{param_RD}"

    logger.info(f"{concat_config}\t{combine}\t{method}\t{is_freq}\t{pd4}\t{vector_str}\t Folder name {concat_config}")


    out_dir = os.path.join(PATH_OUTPUT_MM, combine, method, is_freq, pd4, vector_str)
    os.makedirs(out_dir, exist_ok=True)

    path_sm = os.path.join(out_dir, f"{index}_{param_RD_file}.xlsx")

    # if param_RD_file in path_sm:
    #     print("patient already done")
    #     exit(0)
    # else:
    #     print('patient starting')


    ############################################################
    #####                     Load df                     #####
    ###########################################################

    ## Patients 
    # PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER_WITH_ONTOLOGYX 
    # PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER
    df_raredisease_2 = pd.read_excel(PATH_OUTPUT_DF_PRODUCT4_MATCH_RSD,index_col =0) 
    # df_raredisease_2 = df_raredisease_2[df_raredisease_2['ORPHAcode'] == 'ORPHA:166024']  # 610   166024
    rd_id_list_2 = df_raredisease_2['ORPHAcode'].drop_duplicates().tolist()

 
    ## Diseases
    df_raredisease = pd.read_excel(PATH_OUTPUT_DF_PRODUCT4_MATCH_RSD,index_col =0) 
    df_raredisease = df_raredisease[df_raredisease['ORPHAcode'] == param_RD]  # 610   166024
    rd_id_list = df_raredisease['ORPHAcode'].drop_duplicates().tolist()
    ############################################################
    #####                     Load sm                     #####
    ###########################################################
    ## Build df sm 
    sim_measure = Sim_measure(df_raredisease_2,df_raredisease,'ORPHAcode','ORPHAcode')


    ############################################################
    #####               Load Rare Diseases                 #####
    ###########################################################
    #list_rd=  ['ORPHA:610','ORPHA:166024']
    # rd_id_list_2.extend(rd_id_list)
    if  param_RD in rd_id_list_2:    
        df_sm_no_dict = sim_measure.run_mm_freq(param_RD,rd_id_list_2,combine,method,is_freq,vector_weight)    

        df_sm_no_dict.rename({'patients':'OC2','RDs':'OC1'}, axis='columns',inplace=True)
        sim_measure.export_sm(df_sm_no_dict,path_sm)



    else:
        df_empty = pd.DataFrame(columns=['OC1','OC2','score'], index=range(1))
        sim_measure.export_sm(df_empty, path_sm)
        print(f"empty df sm")



    #print("run_mp_cdf: END.\n")

    #logger.info(f"#####################   END 1_make_ra")
