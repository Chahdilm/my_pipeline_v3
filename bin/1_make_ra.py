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
    # combine = "funSimAvg" #funSimMax funSimAvg  BMA
    # method = "resnik"
    # is_freq = 'n'
    # pd4 = "all_product4_mai_2025"
    # vector_str = '0.99_0.77_0.65_0.63_0.94'


    vector_weight = [float(x)for x in vector_str.split('_')]
    param_RD_file = param_RD.replace(':',"-")


    # ################################################


    concat_config = f"{index}_{param_RD}"

    logger.info(f"{index}\t{param_RD}\t{combine}\t{method}\t{is_freq}\t{pd4}\t{vector_str}\t Folder name {concat_config}")


    out_dir = os.path.join(PATH_OUTPUT_SM, combine, method, is_freq, pd4, vector_str)
    os.makedirs(out_dir, exist_ok=True)



    ############################################################
    #####                     Load df                     #####
    ###########################################################

    ## Patients 
    # PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER_WITH_ONTOLOGYX 
    # PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER
    df_patient = pd.read_excel(PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER_WITH_ONTOLOGYX,index_col=0)
    # df_patient = df_patient[df_patient['phenopacket'] == 'P0001068']  #P0001068 

    patients_id_list = df_patient["phenopacket"].drop_duplicates().tolist()    
    patients_rds_list = df_patient["Disease"].drop_duplicates().tolist()    
    #print(f"run_mp_cdf: Nb patients : {len(patients_id_list)}")

    ## Diseases
    df_raredisease = pd.read_excel(PATH_OUTPUT_DF_PRODUCT4_MATCH_RSD,index_col =0) 
    # df_raredisease = df_raredisease[df_raredisease['ORPHAcode'] == param_RD]  # 610   166024

    ############################################################
    #####                     Load sm                     #####
    ###########################################################
    ## Build df sm 
    sim_measure = Sim_measure(df_patient,df_raredisease,'phenopacket','ORPHAcode')


    ############################################################
    #####               Load Rare Diseases                 #####
    ###########################################################



    if  param_RD in df_raredisease['ORPHAcode'].tolist():    
        df_sm_no_dict = sim_measure.run_sm_freq(param_RD,patients_id_list,combine,method,is_freq,vector_weight)    
        path_sm = os.path.join(out_dir, f"{index}_{param_RD_file}.xlsx")

        sim_measure.export_sm(df_sm_no_dict,path_sm)
        #logger.info(f"{index}\t{param_RD}\t{combine}\t{method}\t{is_freq}\t{vector_str}\t Export df ")
        # ############################################################
        # #####                     CDF                          #####
        # ###########################################################
        path_cdf = os.path.join(out_dir, f"CDF_{index}_{param_RD_file}.xlsx")
        if param_RD in patients_rds_list:
            df_cdf = sim_measure.from_sm_make_cdf(df_sm_no_dict)
            ## Export cdf
            #logger.info(f"{index}\t{param_RD}\t{combine}\t{method}\t{is_freq}\t{vector_str}\t CDF Export df ")

        else:
            df_cdf = pd.DataFrame(columns=["patients","RDs"], index=range(1))
            #logger.info(f"{index}\t{param_RD}\t{combine}\t{method}\t{is_freq}\t{vector_str}\t CDF Empty df export") 
        sim_measure.export_sm(df_cdf,path_cdf)

    else:
        df_empty = pd.DataFrame(columns=['RDs','patients','score'], index=range(1))
        path_empty = os.path.join(out_dir, f"{index}_{param_RD_file}.xlsx")
        sim_measure.export_sm(df_empty, path_empty)



    #print("run_mp_cdf: END.\n")

    #logger.info(f"#####################   END 1_make_ra")
