

from bin.set_log import * 
from bin.classes.dataset import * 

if __name__ == "__main__":

    # -------------------------------------------------------------------------------
    #                        1. DATA LOADING AND PREPROCESSING
    #    - Load data from input phenopacket solverd
    #    - Kepp comfirmed one 
    #    - Normalize/Standardize data
    #-------------------------------------------------------------------------------
    notused_path = ''

    ################################################################################
    #####       Load json file product4                                        #####
    ################################################################################
    build_rds_json = DataSet(PATH_INPUT_PRODUCT4_XML,notused_path)
    json_rd = build_rds_json.from_xml_to_json()
    # build_rds_json.save_json(PATH_OUTPUT_PRODUCT4_JSON, json_rd) 

    build_raredisease = DataSet(PATH_OUTPUT_PRODUCT4_JSON,notused_path)
    df_enpd_raredisease = build_raredisease.build_orpha_df()
    # df_enpd_raredisease.to_excel(PATH_OUTPUT_DF_PRODUCT4)
    rsd_from_rsd = df_enpd_raredisease['ORPHAcode'].drop_duplicates().tolist()
    print(f'nb RD pd4 {len(rsd_from_rsd)}, frequency available {set(df_enpd_raredisease['hpo_frequency'])}')

    ################################################################################
    # orphacode list from rsd 
    file_rsd_orpha = open("/home/maroua/Bureau/runjdbor_saving/products/ALL/orphacode_rsd.txt",'r')
    rsd_orpha = file_rsd_orpha.readlines()
    rsd_orpha_f = []
    for oneo in rsd_orpha:
        rsd_orpha_f.append("ORPHA:" + oneo.strip())


    difference_orpha = set(rsd_orpha_f).difference(rsd_from_rsd)
    match_orpha = set(rsd_from_rsd).intersection(rsd_orpha_f)

    

    ################################################################################
    #####       Rsd product4                                        #####
    ################################################################################
    # build_rds_json = DataSet(PATH_INPUT_PRODUCT4RSD_XML,notused_path)
    # json_rd = build_rds_json.from_xml_to_json()
    # #build_rds_json.save_json(PATH_OUTPUT_PRODUCT4_JSON_RSD, json_rd) 

    # build_raredisease = DataSet( PATH_OUTPUT_PRODUCT4_JSON_RSD,notused_path)
    # df_rsd_raredisease = build_raredisease.from_rsd_build_orpha_df()
    # #df_rsd_raredisease.to_excel(PATH_OUTPUT_DF_PRODUCT4_RSD)
 
    # print(f'nb RD rsd {len(df_rsd_raredisease['ORPHAcode'].drop_duplicates())}, frequency available {set(df_rsd_raredisease['hpo_frequency'])}')
 
    ################################################################################
    ## get match RDs
    df_enpd_raredisease_f = df_enpd_raredisease[df_enpd_raredisease["ORPHAcode"].isin(match_orpha)]
    df_enpd_raredisease_f.to_excel(PATH_OUTPUT_DF_PRODUCT4_MATCH_RSD)
    
    print(f'nb RD rsd {len(df_enpd_raredisease_f['ORPHAcode'].drop_duplicates())}, frequency available {set(df_enpd_raredisease_f['hpo_frequency'])}')


    ################################################################################
    #####       Load json file product1                                       #####
    ################################################################################
  
    build_rds_json = DataSet(PATH_INPUT_PRODUCT1_XML,"")
    json_rd = build_rds_json.from_xml_to_json()
    build_rds_json.save_json(PATH_OUTPUT_PRODUCT1_JSON, json_rd) 

    build_raredisease = DataSet( PATH_OUTPUT_PRODUCT1_JSON,"")
    df_pd1 = build_raredisease.df_pd1()
    df_pd1.to_excel(PATH_OUTPUT_DF_PRODUCT1)


    ################################################################################
    #####       Load json file product7                                       #####
    ################################################################################
  
    build_rds_json = DataSet(PATH_INPUT_PRODUCT7_XML,"")
    json_rd = build_rds_json.from_xml_to_json()
    build_rds_json.save_json(PATH_OUTPUT_PRODUCT7_JSON, json_rd) 

    build_raredisease = DataSet( PATH_OUTPUT_PRODUCT7_JSON,"")
    df_pd7 = build_raredisease.df_pd7()
    df_pd7.to_excel(PATH_OUTPUT_DF_PRODUCT7)


    ################################################################################
    #####       Load json file classif                                         #####
    ################################################################################
    list_classif = os.listdir(PATH_INPUT_PRODUCTCLASSIF_XML)
    for onec in list_classif:
        motif = onec.split(".")[0]
        #motif = "ORPHAclassification_150_rare_inborn_errors_of_metabolism_en_2024"
        # ORPHAclassification_150_rare_inborn_errors_of_metabolism_en_2024
        # ORPHAclassification_147_rare_developmental_anomalies_during_embryogenesis_en_2024
        # ORPHAclassification_181_rare_neurological_diseases_en_2024

        
        build_rds_json = DataSet(PATH_INPUT_PRODUCTCLASSIF_XML + motif+ ".xml","")
        json_rd = build_rds_json.from_xml_to_json()
        build_rds_json.save_json(PATH_OUTPUT_PRODUCT_CLASSIF + motif+ ".json", json_rd) 

        build_raredisease = DataSet(PATH_OUTPUT_PRODUCT_CLASSIF + motif+ ".json","")
        df_pd_classif = build_raredisease.df_classif()
        df_pd_classif.to_excel(PATH_OUTPUT_PRODUCT_CLASSIF + motif+ ".xlsx")

    
