
from bin.set_log import * 

if __name__ == "__main__":  

    # df_rd = pd.read_excel(path_input +'en_product4nf.xlsx',index_col = 0)
    # rds = df_rd['ORPHAcode'].drop_duplicates().tolist()[:10]
    logger.info(f"#####################   START generate_yml_input")


    df_raredisease = pd.read_excel(PATH_OUTPUT_DF_PRODUCT4_MATCH_RSD,index_col =0) 
    list_rd = df_raredisease[COL_DF_PRODUCT4_ORPHACODE].drop_duplicates().tolist()

    rds = []
    for rd in list_rd:
        rdstrip = rd.strip()
        if 'ORPHA' in rdstrip:
            # we need 
            if  rdstrip in list_rd:
                rds.append(rdstrip )
    
    rds_no_doublons = list(set(rds))

    # Generate dictionary format for Snakemake
    config_data = {
        "n": len(rds_no_doublons),  # Number of runs
        ## No Constant parameter
        "param_RD": {i+1: param1 for i, param1 in enumerate(rds_no_doublons)}
    }

    # Save to config.yaml
    with open(PATH_YAML_PRODUCT4 , "w") as f:
        yaml.dump( config_data, f, default_flow_style=False)
    
    logger.info(f"Generate yml, nb of RDs : {len(list_rd)} ")
    logger.info(f"#####################   END ")


