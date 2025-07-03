
from bin.set_log import * 
print(f"START  4_metric_ranking_per_patient")
t0 = time.perf_counter()

os.makedirs(PATH_OUTPUT_COMPARE_RSLT_PER_PATIENT, exist_ok=True)

#############################################
# Set up argument parsing
parser = argparse.ArgumentParser(description="Process inputs for the script.")

# Arguments for file paths and file names
parser.add_argument('--ra', type=str, required=True)
parser.add_argument('--alpha', type=str, required=True)

# Parse the arguments
args = parser.parse_args()
 
ra = args.ra  
alpha = args.alpha

#############################################
# ra = "3_2_2_2_1_rsd_resnik_n_productmai2024_all_vectors_withontologyX"
# alpha=str(0.04)


##### load cdf and sm files 
df_sm = pd.read_excel(PATH_OUTPUT_SM + ra+".xlsx",index_col=0 )
df_cdf = pd.read_excel(PATH_OUTPUT_SM + "CDF_" + ra + ".xlsx",index_col=0 )

list_patient = df_sm['patients'].drop_duplicates().tolist()
# list_patient = df_cdf['patients'].drop_duplicates().tolist()

patient_no_cdf = set(df_sm['patients'].drop_duplicates().tolist()).difference(list_patient)


k = 0
j = 0
logger.info(f"{len(list_patient)} Patient have a rdi available(cdf) ")
path_rw_patient =os.path.join(PATH_OUTPUT_FOLDER_RW,str(alpha),CONFIG_RD)

###################################
## fill and get the ranking  per patients
for i,onev in enumerate(list_patient):
    user_seed = onev
    #print(f"{i}\t{user_seed}")

    ########################################################
    ## Get the pagerank result

    try : 
        ## Open RW dataframe
        df_pg = pd.read_excel(path_rw_patient +"/"+ user_seed +".xlsx")
        try :
            df_pg  =df_pg[["rd","rank_pg",'sum_degres','nb_classif', 'rank_sum_degres_pg']]
        except KeyError:
            df_pg  =df_pg[["Unnamed: 0","rank_pg",'sum_degres','nb_classif','rank_sum_degres_pg']]

    except FileNotFoundError:
        df_pg = pd.DataFrame(columns=["rd","rank_pg",'sum_degres','nb_classif','rank_sum_degres_pg'])
    
    df_pg.columns = ["rd","rank_pg",'sum_degres','nb_classif','rank_sum_degres_pg']

    df_smdpg = df_pg.sort_values(by='rank_sum_degres_pg')
    df_pg = df_pg.sort_values(by='rank_pg')
    ## Rename col for homogenity 
    df_pg = df_pg.rename(columns={'rd':'ORPHAcode','rank_pg':'rank'})
    df_smdpg = df_smdpg.rename(columns={'rd':'ORPHAcode'})


    ########################################################
    ## Compare with other results
    ########################################################

    try:
    
        ## LOAD SM file
        df_sm_seed = df_sm[df_sm['patients'] == user_seed]
        # get the RDI of the user_seed
        # df_p_seed = df_p[df_p['phenopacket'] ==user_seed ]
        # cdf_seed_ORPHA = df_p_seed['Disease'].values[0]
        df_cdf_seed = df_cdf[df_cdf['patients'] == user_seed]
        cdf_seed_ORPHA = df_cdf_seed["RDs"].values[0]
    except IndexError:
        logger.info(f"{user_seed} the RDI : {cdf_seed_ORPHA}  is not in the pd  ")
        df_sm_seed = pd.DataFrame([],columns=['RDs','patients','score','rank'])
        j=j+1
    ## Rename col for homogenity 
    df_sm_seed = df_sm_seed.rename(columns={'patients': 'patient','RDs':'ORPHAcode'})

 
    ## LOAD STEP file 
    path_rsdA2_resniksy = '/home/maroua/Bureau/wip/only_rsd_step/only_jar/SolveRD/output_files_hpo2025_rsdpd4mai2025_withduplicate_noontologyX/stepA2_withdupli_noontologyX_Resnik (symmetric).tsv'

    tsv_step = ['stepA2.tsv']#['stepB2.tsv','stepA1.tsv','stepA2.tsv']
    for step_f in tsv_step :
        
        df_step = pd.read_csv(path_rsdA2_resniksy,sep = '\t')
        if step_f in  ['stepB2.tsv','stepC1.tsv']:
            df_step_seed =  df_step[(df_step['case'] == user_seed )]
        else:
            df_step_seed =  df_step[(df_step['phenopacket'] == user_seed )]

        try:
            df_step_seed_o = df_step_seed[ (df_step_seed['ORPHAcode'] == cdf_seed_ORPHA ) | (df_step_seed['ORPHAcode_child'] == cdf_seed_ORPHA ) ]
            rank_step = int(df_step_seed_o['rank'].values[0])
            if cdf_seed_ORPHA in df_step_seed_o['ORPHAcode'].values[0]:
                type_o = "P"
            else:
                type_o = "C"
        except:
            logger.info(f"{user_seed} don't have RDI {cdf_seed_ORPHA} top50 RSD ")
            type_o = "N"
            rank_step = np.nan
            k = k+1
        
    ## C1 et C2 no need puisqu'on regarde le rang d'un autre case en fonciton du case d'interet
    ## Rename col for homogenity 
    df_step_seed = df_step_seed.rename(columns={'phenopacket': 'patient'})


    ### save all in excel file 
    with pd.ExcelWriter(PATH_OUTPUT_COMPARE_RSLT_PER_PATIENT + user_seed +".xlsx") as writer:  
        df_step_seed.to_excel(writer,sheet_name='RSD')  
        df_sm_seed.to_excel(writer,sheet_name='RA')  
        df_pg.to_excel(writer,sheet_name='RARW')  
        df_smdpg.to_excel(writer,sheet_name='RARW_sumdegres')  


logger.info(f"{j} patient have  RDI which is not in the pd in RSD  ")
logger.info(f"{k} patients don't have RDI in top50 step  ")

logger.info(f'Build df of all methods with all ranking  ')
logger.info(f"END  4_metric_ranking_per_patient")



logger.info(f"END  4_metric_ranking_per_patient done in {time.perf_counter() - t0:.1f}s")
print(f"END  4_metric_ranking_per_patient done in {time.perf_counter() - t0:.1f}s")

