
"""

2. etude de la similarité entre maladie 
PUIS avec le script python compare_rank_topn.py je peux avoir le ranking top50  des maladies
(peut etre mettre le ranking global psk y'a des RDI avec des rank tres bas)

une fois cela fait je dois definir une limite de a quel nivea je compae mes Orphacode (pour pouvoir fourmer des groupes)
classif ? group of disorder ?cf discussion avec Caterina (apres besoins d'une correction manuelle)
pd7 linéairisation pour parent préférentiel 
cb de group of disorder ils ont en communs 
et facteurs comme patient-maladies


"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from bin.set_log import * 
from bin.classes.dataset import * 

def interpret_variable(name_col, onep, df_profile, df_profile_stats,name_col_el):
    output = {}
    # Get values from the DataFrame and statistics
    onep_value = int(df_profile[df_profile[name_col_el] == onep][name_col].values[0])
    mean_value = df_profile_stats[name_col]["mean"]
    min_value =  df_profile_stats[name_col]["min"]
    max_value = df_profile_stats[name_col]["max"]
    
    factor = onep_value / mean_value
    
    # Build a descriptive message based on the variable type.
    if name_col == 'nb_hpo_terms':
        if onep_value > mean_value:
            compare_to_mean = (f"Higher")
        elif onep_value <  mean_value:
            compare_to_mean = (f"Lower")

    elif name_col == 'nb_hpo_categorie':
        if onep_value > mean_value:
            compare_to_mean = (f"Higher")
        elif onep_value < mean_value:
            compare_to_mean = (f"Lower")
        else:
            compare_to_mean = (f"equal")
    elif name_col == 'mean_depth':
        if onep_value > mean_value:
            compare_to_mean = (f"Higher")
        elif onep_value < mean_value:
            compare_to_mean = (f"Lower")
        else:
            compare_to_mean = (f"equal")
    elif name_col == 'semantic_variability':
        if onep_value > mean_value:
            compare_to_mean = (f"Higher")
        elif onep_value < mean_value:
            compare_to_mean = (f"Lower")
        else:
            compare_to_mean = (f"equal")
    elif name_col == 'mean_IC':
        if onep_value > mean_value:
            compare_to_mean = (f"Higher")
        elif onep_value < mean_value:
            compare_to_mean = (f"Lower")
        else:
            compare_to_mean = (f"equal")
    elif name_col == 'proportion_general_terms':
        if onep_value > mean_value:
            compare_to_mean = (f"Higher")
        elif onep_value < mean_value:
            compare_to_mean = (f"Lower")
        else:
            compare_to_mean = (f"equal")   
    elif name_col == 'nb_exact_matches':
        if onep_value > mean_value:
            compare_to_mean = (f"Higher")
        elif onep_value < mean_value:
            compare_to_mean = (f"Lower")
        else:
            compare_to_mean = (f"equal")  
    elif name_col == 'nb_branch_matches':
        if onep_value > mean_value:
            compare_to_mean = (f"Higher")
        elif onep_value < mean_value:
            compare_to_mean = (f"Lower")
        else:
            compare_to_mean = (f"equal")       
    else:
        compare_to_mean = "Aucune condition pour cette variable."
    
    # Fill the output dictionary
    output["variable"] = name_col
    output["value"] = onep_value
    output["global_mean"] = mean_value
    output["global_min"] = min_value
    output["global_max"] = max_value
    output["factor"] = factor
    output["compare_to_mean"] = compare_to_mean

    return output


def group_analysis_element(onep, df_profiles_onep, df_profiles_onep_stat,variables,name_el):
    analysis_results = {}
    # List of variables we wish to analyze.
    for var in variables:
        analysis_results[var] = interpret_variable(var, onep, df_profiles_onep, df_profiles_onep_stat,name_el)
    
    return analysis_results


####################################################################################


def get_name_rype_pd1(pd1,rd_oi):
    rd_name = pd1[pd1['ORPHACode'] == rd_oi]['Name']
    rd_type = pd1[pd1['ORPHACode'] == rd_oi]['Group']
    return rd_name.values[0],rd_type.values[0]

def similarity_word(a, b):
    """Return a similarity ratio between two strings using difflib."""
    return SequenceMatcher(None, a, b).ratio()

def get_related_group_pp(pp_name,list_rd_method_name,pd_orphanet_classif_xlsx):
    ##  RDs list 
    print(f"RDs list : {len(list_rd_method_name)}")
    for one_rd in list_rd_method_name: # ici
        rd_name, rd_type = get_name_rype_pd1(df_pd1,one_rd)
        print(f"{one_rd} - {rd_name} \t Type: {rd_type} " )

    
    ## matching pp classif with the classification related file to get the group 
    print("\nMatching pp classif with the classification related file to get the group ")
    best_matches = {}
    for motif in pp_name:  
        best_file = None
        best_score = 0
        # Compare each JSON file against the motif
        for file_name in pd_orphanet_classif_xlsx:
            score = similarity_word(motif.lower(), file_name.lower())
            if score > best_score:
                best_score = score
                best_file = file_name
        best_matches[motif] = best_file

    print(best_matches.keys())


    for key,value in best_matches.items():
        ## load a df per classif 
        interaction_rd = set()

        print(f"\nClassification name : {key}")
        df_pd_classif = pd.read_excel(PATH_OUTPUT_PRODUCT_CLASSIF + value,index_col=0)
 
        for one_rd in list_rd_method_name: # ici
            ## get the related parents if the rd belong to a child classif (disorder, subtype)
            child_df = df_pd_classif[df_pd_classif['child_id']==one_rd]
            for parent_of_one_rd in child_df["parent_id"].tolist():
                if ("Category" or "Clinical group" in child_df):
                    interaction_rd.add((one_rd,parent_of_one_rd))

            ## get the related child if the rd belong to a parent classif (disorder)
            parent_df = df_pd_classif[df_pd_classif['parent_id']==one_rd]
            for child_of_one_rd in parent_df["child_id"].tolist():
                if ("Category" or "Clinical group" in child_df):
                    interaction_rd.add((one_rd,parent_of_one_rd))

        df_match_classif = pd.DataFrame(interaction_rd,columns=["Rd_from_method","related_group"])
        grouped = df_match_classif.groupby("related_group")["Rd_from_method"].apply(list).to_dict()
        for key,value_list in grouped.items():
            gp_name, gp_type = get_name_rype_pd1(df_pd1,key)
            print(f"Group :\n{key} - {gp_name} \t Type : {gp_type} have {len(value_list)}  Rds from the methods : ")
            for onev in value_list:
                v_name, v_type = get_name_rype_pd1(df_pd1,onev)
                print(f" {onev} - {v_name} \t Type : {v_type} ")


def get_related_group_pp_json(dict_append,name_method_json_key,rank_method,get_pp_step,list_rd_step,pd_orphanet_classif_xlsx):
    dict_append[name_method_json_key] = {}
    # 1. Collect RD information.
    rd_info = {}
    for one_rd in list_rd_step:
        rd_name, rd_type = get_name_rype_pd1(df_pd1, one_rd)
        rd_info[one_rd] = {"name": rd_name, "type": rd_type}

    dict_append[name_method_json_key] =  {
                    "rank_rdi" : int(rank_method ),
                    "rds": rd_info,
                    "count": len(rd_info),
                }
    
    


    # 2. Match each motif (preferred parent classification name) with the best matching xlsx file.
    best_matches = {}
    for motif in get_pp_step:
        best_file = ""
        best_score = 0
        # Compare each classification file (xlsx) against the motif.
        for file_name in pd_orphanet_classif_xlsx:
            score = similarity_word(motif.lower(), file_name.lower())
            if score > best_score:
                best_score = score
                best_file = file_name
        best_matches[motif] = best_file

    list_classif_f = []  # will accumulate one entry per motif

    for key_m, excel_file in best_matches.items():
        # Load the classification DataFrame for this motif.
        df_pd_classif = pd.read_excel(os.path.join(PATH_OUTPUT_PRODUCT_CLASSIF, excel_file), index_col=0)

        # Collect unique interactions as tuples: (rd, related_group)
        interaction_rd = set()

        # For each RD in our list, get related groups from both the child and parent positions.
        for one_rd in list_rd_step:
            child_df = df_pd_classif[df_pd_classif['child_id'] == one_rd]
            for parent_of_one_rd in child_df["parent_id"].tolist():
                interaction_rd.add((one_rd, parent_of_one_rd))
            parent_df = df_pd_classif[df_pd_classif['parent_id'] == one_rd]
            for child_of_one_rd in parent_df["child_id"].tolist():
                interaction_rd.add((one_rd, child_of_one_rd))
        
        # Group the interactions by the related group identifier.
        groupe_by_classif = {}
        for rd, group in interaction_rd:
            groupe_by_classif.setdefault(group, []).append(rd)
        
        # Build a list of group dictionaries for the current motif.
        list_classif = []  
        for key_classif, rd_list in groupe_by_classif.items():
            # Create a new dictionary for each group.
            gp_name, gp_type = get_name_rype_pd1(df_pd1, key_classif)
            group_entry = {
                "classif": {
                    "id": key_classif,
                    "name": gp_name,
                    "type": gp_type,
                    "count": len(rd_list),
                    "rds": []  # to hold a list of RD dictionaries
                }
            }
            # Populate the list of related RDs.
            for rd_v in rd_list:
                gp_name_v, gp_type_v = get_name_rype_pd1(df_pd1, rd_v)
                rd_info = {
                    "id": rd_v,
                    "name": gp_name_v,
                    "type": gp_type_v
                }
                group_entry["classif"]["rds"].append(rd_info)
            list_classif.append(group_entry)
        
        # Build an entry for this motif which includes a preferred parent classification "name"
        # along with all its grouped RDs.
        motif_entry = {
            "classif_name": {
                "name": key_m,
                "id" : df_pd_classif['root'].values[0],
                "count":int(len(groupe_by_classif.keys())),
                "rds": list_classif
            }
        }
        list_classif_f.append(motif_entry)

    # Add the accumulated information into the result dictionary.
    dict_append[name_method_json_key]["Matching_pp"] = {"count" : len(list_classif_f),
                                                        "elements" : list_classif_f}
    return dict_append



print("#################################################################")
print("rank_factor_part2")
# Set up argument parsing
parser = argparse.ArgumentParser(description="Process inputs for the script.")

# Arguments for file paths and file names
parser.add_argument('--user_nb_top_rd', type=int, required=True)
parser.add_argument('--onep', type=str, required=True)


# Parse the arguments
args = parser.parse_args()

user_nb_top_rd = args.user_nb_top_rd  
onep = args.onep 


user_nb_top_rd = 10
onep = "P0011778"

## Load classif preferentiel parent (pd 7) and type (pd1)
df_pd1 = pd.read_excel(PATH_OUTPUT_DF_PRODUCT1,index_col=0)
df_pd7 = pd.read_excel(PATH_OUTPUT_DF_PRODUCT7,index_col=0)

## Load df with all ranking RDI per patient
df_compare_methode_global = pd.read_excel(PATH_OUTPUT_DF_COMPARE_RANK_DIRECT,index_col=0)

## Load df with all ranking RDI per patient
df_profile_couple = pd.read_excel(PATH_OUTPUT_COMPARE_RSLT + "patient_rdi_profil.xlsx",index_col= 0)
df_profile_couple_stats = pd.read_excel(PATH_OUTPUT_COMPARE_RSLT + "patient_rdi_profil_stats.xlsx",index_col= 0)


## Get file from product (for classification)
pd_orphanet_classif = os.listdir(PATH_OUTPUT_PRODUCT_CLASSIF)
pd_orphanet_classif_xlsx = []
for one in pd_orphanet_classif:
    if ".xlsx" in one:
        pd_orphanet_classif_xlsx.append(one)



# Load data from Excel files (adjust PATH_OUTPUT_COMPARE_RSLT as needed)
df_profiles_onep = pd.read_excel(PATH_OUTPUT_COMPARE_RSLT + "patient_profil.xlsx", index_col=0)
df_profiles_onep_stat = pd.read_excel(PATH_OUTPUT_COMPARE_RSLT + "patient_profil_stats.xlsx", index_col=0)
df_profiles_rd = pd.read_excel(PATH_OUTPUT_COMPARE_RSLT + "rd_profil.xlsx", index_col=0)
df_profiles_rd_stat = pd.read_excel(PATH_OUTPUT_COMPARE_RSLT + "rd_profil_stats.xlsx", index_col=0)
df_compare_methode_global = pd.read_excel(PATH_OUTPUT_DF_COMPARE_RANK_DIRECT, index_col=0)

# Get ranking RDI for the given patient
df_init_g = df_compare_methode_global[df_compare_methode_global['patients'] == onep]
rdi = df_init_g["RDs"].values[0]
rdi_name,rdi_type = get_name_rype_pd1(df_pd1,rdi)
minirdi = df_profile_couple[df_profile_couple['patient'] == onep]

variables = ["nb_hpo_terms", "nb_hpo_categorie", "mean_depth", "semantic_variability", "mean_IC", "proportion_general_terms"]


# Create the result dictionary
result_dict = {}
result_dict["patient"] = {"id": minirdi["patient"].values[0]}
result_dict["patient"]["analysis"] = group_analysis_element(onep, df_profiles_onep, df_profiles_onep_stat,variables,"element")

result_dict["rdi"] = {"id": minirdi["disease"].values[0], 
                      "Name": rdi_name,
                      "Type":rdi_type,
                      "classif":df_pd7[df_pd7['ORPHACode']==minirdi["disease"].values[0] ]['Classif_name'].values[0]
                      }
result_dict["rdi"]["analysis"] = group_analysis_element(rdi, df_profiles_rd, df_profiles_rd_stat,variables,"element")



result_dict["patient-rdi"] ={"nb_exact_matches": int(minirdi["nb_exact_matches"].values[0]), 
                        "nb_branch_matches": int(minirdi["nb_branch_matches"].values[0]),
                        "nb_hpo_categorie":int( minirdi["nb_hpo_categorie"].values[0]), 
                        "mean_depth":int( minirdi["mean_depth"].values[0]),
                        "semantic_variability": int(minirdi["semantic_variability"].values[0]), 
                        "mean_IC": int(minirdi["mean_IC"].values[0]),
                        "proportion_general_terms": int(minirdi["proportion_general_terms"].values[0])
                        }

variables_rdi = ["nb_exact_matches", "nb_branch_matches","nb_hpo_categorie", "mean_depth", "semantic_variability", "mean_IC", "proportion_general_terms"]
result_dict["patient-rdi"]["analysis"] = group_analysis_element(str(onep), df_profile_couple, df_profile_couple_stats,variables_rdi,"patient") # par patient psk les patients sont unique dans la df pas les orpha



## c'est moche le faire plus proprement
#df_init = pd.read_excel(PATH_OUTPUT_COMPARE_RSLT_PER_PATIENT+onep+".xlsx",index_col=0)
#rdi = df_init["cdf_orphacode"].drop_duplicates().tolist()
get_pp_rdi = df_pd7[df_pd7['ORPHACode'] ==rdi]['Classif_name'].drop_duplicates().tolist()
print(f" The RDI {rdi} belong to {len(get_pp_rdi)} preferentiel parent classification \n{get_pp_rdi}")
print("#################################################################")

## 2. now let get the top 10 RDs of each methods and its classif pp
print("Get the top 10 RDs of each methods and its classif pp")
## STEP  
df_step = pd.read_excel(PATH_OUTPUT_COMPARE_RSLT_PER_PATIENT+onep+".xlsx",index_col=0,sheet_name="step")
df_step_top10 = df_step[df_step['rank'].isin([*range(1,user_nb_top_rd+1)])].reset_index().sort_values(by='rank')
df_step_top10 = df_step_top10[["phenopacket","ORPHAcode","score",'rank']].drop_duplicates()
list_rd_step = df_step_top10['ORPHAcode'].tolist()
get_pp_step = df_pd7[df_pd7['ORPHACode'].isin(list_rd_step)]['Classif_name'].drop_duplicates().tolist()
print(f"STEP : The top 10 RDs belong to {len(get_pp_step)} preferentiel parent classification \n{get_pp_step}")

result_dict = get_related_group_pp_json(result_dict,"RD_top10_STEP",df_init_g["rank_steps"].values[0],get_pp_step,list_rd_step,pd_orphanet_classif_xlsx)




print("#################################################################")

## SM
df_sm = pd.read_excel(PATH_OUTPUT_COMPARE_RSLT_PER_PATIENT+onep+".xlsx",index_col=0,sheet_name="sm")
df_sm_top10 = df_sm[df_sm['rank'].isin([*range(1,user_nb_top_rd+1)])].reset_index().sort_values(by='rank')
list_rd_sm = df_sm_top10['RDs'].tolist()
get_pp_sm = df_pd7[df_pd7['ORPHACode'].isin(list_rd_sm)]['Classif_name'].drop_duplicates().tolist()
print(f"SM : The top 10 RDs belong to {len(get_pp_sm)} preferentiel parent classification \n{get_pp_sm}")

result_dict = get_related_group_pp_json(result_dict,"RD_top10_SM",df_init_g["ranks_config"].values[0],get_pp_sm,list_rd_sm,pd_orphanet_classif_xlsx)

print("#################################################################")

## RW
df_pg = pd.read_excel(PATH_OUTPUT_COMPARE_RSLT_PER_PATIENT+onep+".xlsx",index_col=0,sheet_name="pagerank")
df_smdpg_top10 = df_pg[df_pg['rank_pg'].isin([*range(1,user_nb_top_rd+1)])].reset_index().sort_values(by='rank_sum_degres_pg')
# Get hubs
# df_smdpg_top10 = df_pg[df_pg['rank_sum_degres_pg'].isin([*range(1,user_nb_top_rd+1)])].reset_index().sort_values(by='rank_sum_degres_pg')
list_rd_pg = df_smdpg_top10['rd'].tolist()
get_pp_rw = df_pd7[df_pd7['ORPHACode'].isin(list_rd_pg)]['Classif_name'].drop_duplicates().tolist()
print(f"RW : The top 10 RDs belong to {len(get_pp_rw)} preferentiel parent classification \n{get_pp_rw}")
result_dict = get_related_group_pp_json(result_dict,"RD_top10_RW",df_init_g["rank_rw"].values[0],get_pp_rw,list_rd_pg,pd_orphanet_classif_xlsx)

print("#################################################################")


### build df to make fig
rslt_tuple = []
rslt_tuple = from_json_to_df(result_dict,"RD_top10_STEP")
rslt_tuple = from_json_to_df(result_dict,"RD_top10_SM")
rslt_tuple = from_json_to_df(result_dict,"RD_top10_RW")

def from_json_to_df(json_dict,method_name):
    method_section = json_dict[method_name]
    rank = method_section["rank_rdi"]
    classif_count = method_section['Matching_pp']['count']
    list_classif_rd = method_section['Matching_pp']['elements']
    for oneclassif in list_classif_rd:
        classif_name = oneclassif['classif_name']['name']
        classif_id = oneclassif['classif_name']['id']
        classif_nb_rd_related = oneclassif['classif_name']['count']
        list_rd_from_group =oneclassif['classif_name']['rds']
        for onegrp in list_rd_from_group:
            group_id = onegrp['classif']['id']
            group_name = onegrp['classif']['name']
            group_count = onegrp['classif']['count']
            list_group_rd_match =  onegrp['classif']['rds']
            #if group_count >= 1:
            for onerds in list_group_rd_match:
                rd_id = onerds["id"]
                rd_name = onerds["name"]
                rd_type = onerds["type"]
                rslt_tuple.append((rank,classif_count,classif_name,classif_id,classif_nb_rd_related,group_name,group_id,group_count,
                                rd_name,rd_id,rd_type ))
            # else:
            #     print(f"This group {group_id} have only one rd match ")
    return rslt_tuple



df_classif_grp_rd = pd.DataFrame(rslt_tuple,columns=["rank","nb_classif_pp","classif_name","classif_id","classif_count","group_name","group_id","group_count","rd_name","rd_id","rd_type"])

def get_metric(json_section,name_metric):
    #name_metric = json_section['analysis']['nb_hpo_terms']['variable']
    factor_metric = json_section['analysis']['nb_hpo_terms']['factor']
    compare_metric = json_section['analysis']['nb_hpo_terms']['compare_to_mean']
    return factor_metric,compare_metric


## df metrics
rslt_tuple = []
type_name = "patient"
type_section = result_dict[type_name]
type_section['id']

factor_nbhpo,compare_nbhpo = get_metric(type_section,"nb_hpo_terms")
factor_nbcat,compare_nbcat = get_metric(type_section,"nb_hpo_categorie")
factor_meand,compare_meand = get_metric(type_section,"mean_depth")
factor_meandsd,compare_meandsd = get_metric(type_section,"semantic_variability")
factor_meanIC,compare_meanIC = get_metric(type_section,"mean_IC")
factor_proG,compare_proG = get_metric(type_section,"proportion_general_terms")

rslt_tuple. 



# Save to JSON.
out_filename = os.path.join(PATH_OUTPUT_COMPARE_RSLT, "json", onep + ".json")
with open(out_filename, "w", encoding="utf-8") as outfile:
    json.dump(result_dict, outfile, indent=4)

print("END")
print("#################################################################")



##################################################################################
result_dict


### 

result_dict["patient"]["id"]

 