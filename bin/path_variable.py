import os 
from bin.config_json import CONFIG_RD,CONFIG_ALPHA


#CONFIG_ALPHA = "0.04"
#CONFIG_RD = "resnik_n_all_product4_avril_2025_1_1_0_0_0"

CONFIG = CONFIG_RD + "_" + CONFIG_ALPHA


#PATH_INIT  = "/my_pipeline/"
PATH_INIT  = "/home/maroua/Bureau/wip/my_pipeline_v2/"
PATH_OUTPUT = PATH_INIT + "output/"
PATH_INPUT = PATH_INIT + "input/"

PATH_INPUT_HPO = PATH_INIT + "input/hpo/"

os.makedirs(PATH_OUTPUT,exist_ok=True)
os.makedirs(PATH_INPUT,exist_ok=True)

## Log folder
PATH_LOG = PATH_OUTPUT + f"log/"
PATH_LOG_FILE  = PATH_LOG+ f"log_{CONFIG}.log"
os.makedirs(PATH_LOG,exist_ok=True)

 

## folder where mp is stored 
PATH_OUTPUT_SM = PATH_OUTPUT + "mp_sm/"
PATH_OUTPUT_SM_CDF_FILE = PATH_OUTPUT_SM + f"CDF_{CONFIG}.xlsx"

PATH_OUTPUT_MM = PATH_OUTPUT + "mm_sm/"
os.makedirs(PATH_OUTPUT_SM,exist_ok=True)
os.makedirs(PATH_OUTPUT_MM,exist_ok=True)

## folder where the mm network is stored 
# folder_matrix = "mm_matrix/"
# PATH_OUTPUT_FOLDER_MATRIX = PATH_OUTPUT + folder_matrix
# os.makedirs(PATH_OUTPUT_FOLDER_MATRIX,exist_ok=True)

PATH_OUTPUT_FOLDER_MATRIX_ADD_PATIENT = PATH_OUTPUT_MM + "/patient_added/"
os.makedirs(PATH_OUTPUT_FOLDER_MATRIX_ADD_PATIENT,exist_ok=True)

PATH_OUTPUT_DF_PATIENT = PATH_OUTPUT + "patient_solverd/patient_confirmed_solverd.xlsx"  
PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER = PATH_OUTPUT + "patient_solverd/patient_confirmed_solverd_only_disorder.xlsx"  
## meme principe que l'autre v2
PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER_v2 = PATH_OUTPUT + "patient_solverd/patient_confirmed_solverd_only_disorder_v2.xlsx" 
## patient with ongologyX
PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER_WITH_ONTOLOGYX = PATH_OUTPUT + "patient_solverd/patient_confirmed_solverd_only_disorder_with_ontologyX.xlsx" 

COL_DF_PATIENT_PATIENT = "phenopacket"  #"phenopacket" Patient
COL_DF_PATIENT_ORPHACODE = "Disease" #"ORPHAcode"   Disease

#PATH_OUTPUT_FOLDER_RW = PATH_OUTPUT + "/rw_funsimavg_resnik_pd4rsd/"
PATH_OUTPUT_FOLDER_RW = PATH_OUTPUT + "/rarw/"
os.makedirs(PATH_OUTPUT_FOLDER_RW,exist_ok=True)


#####################################
 
PATH_OUTPUT_COMPARE_RSLT = PATH_OUTPUT + "/compare_rank_" + CONFIG + "/"
PATH_OUTPUT_COMPARE_RSLT_PER_PATIENT =PATH_OUTPUT_COMPARE_RSLT + "/metric_patient/"

PATH_OUTPUT_DF_COMPARE_RANK_DIRECT =PATH_OUTPUT_COMPARE_RSLT + "compare_rank_method.xlsx"
PATH_OUTPUT_COMPARE_RSLT_ANALYSIS_PER_PATIENT = PATH_OUTPUT_COMPARE_RSLT + "/analysis_per_patient/"
PATH_OUTPUT_COMPARE_METRIC_CLASSIF =PATH_OUTPUT_COMPARE_RSLT + "/metric_classif/" 

PATH_OUTPUT_COMPARE_GLOBAL =PATH_OUTPUT_COMPARE_RSLT + "/global/"

#####################################

PATH_OUTPUT_PRODUCT = PATH_OUTPUT + "pd_orphanet/"
PATH_OUTPUT_PRODUCT_CLASSIF = PATH_OUTPUT_PRODUCT+ "/Classifications/"
os.makedirs(PATH_OUTPUT_PRODUCT_CLASSIF,exist_ok=True)
os.makedirs(PATH_OUTPUT_PRODUCT,exist_ok=True)
PATH_OUTPUT_DF_PC_CLASSIF = PATH_OUTPUT_PRODUCT + "/parent_child_classif.xlsx"
PATH_OUTPUT_DF_PC = PATH_OUTPUT_PRODUCT + "/parent_child_noclassif.xlsx"
## mercredi 21 mai normalement pas de dif avec la v1 
PATH_OUTPUT_DF_PC_CLASSIF_v2 = PATH_OUTPUT_PRODUCT + "/parent_child_noclassif_v2.xlsx"
PATH_OUTPUT_DF_PC_v2 = PATH_OUTPUT_PRODUCT + "/parent_child_classif_v2.xlsx"


PATH_OUTPUT_PRODUCT4_JSON_RSD = PATH_OUTPUT_PRODUCT +  "/all_rsdpd4_mai_2025.json"
PATH_OUTPUT_DF_PRODUCT4_RSD = PATH_OUTPUT_PRODUCT + "/all_rsdpd4_mai_2025.xlsx"

PATH_OUTPUT_PRODUCT4_JSON = PATH_OUTPUT_PRODUCT +  "/all_enpd_mai_2025.json"
PATH_OUTPUT_DF_PRODUCT4 = PATH_OUTPUT_PRODUCT + "/all_enpd_mai_2025.xlsx"
PATH_OUTPUT_DF_PRODUCT4_MATCH_RSD = PATH_OUTPUT_PRODUCT + "/all_enpd_mai_2025_same_rd_rsd_v2.xlsx" #"/all_enpd_mai_2025_same_rd_rsd.xlsx"


COL_DF_PRODUCT4_ORPHACODE = 'ORPHAcode'
PATH_LIST_PRODUCT4 = PATH_OUTPUT_PRODUCT + "/list_rds.txt"
PATH_YAML_PRODUCT4 = PATH_OUTPUT_PRODUCT + "/RDs_all.yaml"
PATH_CLASSIFICATION_JSON =  PATH_OUTPUT_PRODUCT + "/classif_orpha.json"

PATH_OUTPUT_PRODUCT7_JSON = PATH_OUTPUT_PRODUCT + "en_product7.json"
PATH_OUTPUT_DF_PRODUCT7 = PATH_OUTPUT_PRODUCT + "en_product7.xlsx"

PATH_OUTPUT_PRODUCT1_JSON = PATH_OUTPUT_PRODUCT + "en_product1.json"
PATH_OUTPUT_DF_PRODUCT1 = PATH_OUTPUT_PRODUCT + "en_product1.xlsx"

 
## for synthetic patients
# PATH_OUTPUT_DF_PREVALENCE = PATH_OUTPUT_PRODUCT + "prevalence_orphanet.xlsx"
# PATH_OUTPUT_DF_OMIM_ORPHA = PATH_OUTPUT_PRODUCT +  "map_omim_orphanet.xlsx"
# PATH_OUTPUT_DF_OMIM_ORPHA_GENE = PATH_OUTPUT_PRODUCT +  "map_omim_orphanet_gene.xlsx"
# PATH_OUTPUT_DF_ORPHA_GENE = PATH_OUTPUT_PRODUCT +  "map_orphanet_gene.xlsx"

# PATH_OUTPUT_API_OMIM_FILES = PATH_OUTPUT_PRODUCT +  "/api_json_synth_omim/"
# PATH_INPUT_HPO_RAND_FD = PATH_INPUT +  "patient/hpo_random_from_phenopacket_comfirmed.txt"

# PATH_OUTPUT_JSON_ORPHA_IMP = PATH_OUTPUT_PRODUCT + "patient/orphanet_imprecision.json"
# PATH_OUTPUT_JSON_ORPHA_NOI = PATH_OUTPUT_PRODUCT + "patient/orphanet_noisy.json"
# PATH_OUTPUT_JSON_ORPHA_OPT = PATH_OUTPUT_PRODUCT + "patient/orphanet_optimal.json"
# PATH_OUTPUT_JSON_OMIM_IMP = PATH_OUTPUT_PRODUCT + "patient/omim_imprecision.json"
# PATH_OUTPUT_JSON_OMIM_NOI = PATH_OUTPUT_PRODUCT + "patient/omim_noisy.json"
# PATH_OUTPUT_JSON_OMIM_OPT = PATH_OUTPUT_PRODUCT + "patient/omim_optimal.json"

##########################################################################
PATH_INPUT_PRODUCT =  PATH_INPUT + "/pd_orphanet/"
PATH_INPUT_PRODUCT4RSD_XML = PATH_INPUT_PRODUCT +  "/all_rsdpd4_mai_2025.xml"
PATH_INPUT_PRODUCT4_XML = PATH_INPUT_PRODUCT +  "/all_enpd_mai_2025.xml" #"/all_product4_avril_2025.xml"

PATH_INPUT_PRODUCT1_XML = PATH_INPUT_PRODUCT +  "/en_product1.xml"
PATH_INPUT_PRODUCT7_XML = PATH_INPUT_PRODUCT +  "/en_product7.xml"

PATH_INPUT_PRODUCTCLASSIF_XML =  PATH_INPUT_PRODUCT +  "/Classifications/"

PATH_INPUT_PREVALENCE = PATH_INPUT_PRODUCT + "/prevalences.json"

PATH_INPUT_PATIENTS_FOLDER = PATH_INPUT +  "patient/SolveRD_WP1_phenopackets_v2_with_ern_13301/"
PATH_INPUT_PATIENTS_FOLDER_ONTOLOGYX = PATH_INPUT +  "patient/study_population/"

PATH_INPUT_PATIENTS_FC = PATH_INPUT +  "patient/PATIENTS_SOLVED_FC_v2.xlsx"

PATH_INPUT_STEP_A2 = PATH_INPUT + "/stepA2.tsv"