
from bin.set_log import * 


p = argparse.ArgumentParser()

p.add_argument('-f','--filter-type',required=True,help="vector_str (e.g. 2_2_1_1)")
p.add_argument("--col1",required=True)
p.add_argument("--col2",required=True)

args = p.parse_args()
vector_str = args.filter_type
name_col1 = args.col1
name_col2 = args.col2

# name_col1='patients'
# name_col2='RDs'
# vector_str = '1_1_1_1_1'
 

xlsx_files = glob.glob(f"{PATH_OUTPUT_SM}/**/*.xlsx", recursive=True)
path_sm_ra = []
for xlsx in xlsx_files:
    if vector_str in xlsx:
        path_sm_ra.append(xlsx)



data_dict = {}

# Define the patterns to match
combine_options ={'BUMS','rsd',"funSimAvg","BMA",'funSimMax'}
sm_methods = {"resnik","graphic",'rel','ic','lin','jc'}
weights = {'n'}
pdtype_pattern = 'productmai2024_controvector_withontologyX'

# Process each file path
for f in path_sm_ra:
    combine = sm_method = weight = pdtype = None  # Reset variables for each file
    
    # Parse the file path
    for one_s in f.split('/'):
        if one_s in combine_options:
            combine = one_s
        elif one_s in sm_methods:
            sm_method = one_s
        elif one_s in weights:
            weight = one_s
        elif pdtype_pattern in one_s:
            pdtype = one_s
    
    # Validate that all components were found (optional safety check)
    if None in (combine, sm_method, weight, pdtype):
        #print(f"Warning: Missing component in file path: {f}")
        continue  # Skip this file if any part is missing
    
    # Build the key
    group_key = f"{vector_str}_{combine}_{sm_method}_{weight}_{pdtype}"
    
    # Append the file to the corresponding key
    data_dict.setdefault(group_key, []).append(f)

  
for key, value in data_dict.items():
    start_time = time.perf_counter()

    #logger.info(f"{key}\tProcessing configuration")
    
    dfs_cdf = []
    dfs_sm = []

    for v in value:
        try:
            one_df = pd.read_excel(v, index_col=0)

            if not one_df.empty:

                if "CDF" in v:
                    dfs_cdf.append(one_df)
                else:
                    dfs_sm.append(one_df)
            else:
                #logger.info("{}\t is empty pass ".format(v))
                pass
        except Exception as e:
            #print(f"Error reading {v}: {e}")
            pass


    df_sm_complete = pd.concat(dfs_sm)
    # ORPHAcode  RDs
    df_sm_complete = df_sm_complete.sort_values(by=[name_col1, "score"], ascending=[True, False])
    # patient patients
    df_sm_complete["rank"] = df_sm_complete.groupby(name_col1)["score"].rank(ascending=False, method="dense")
    


    sm_output_path = os.path.join(PATH_OUTPUT_SM, f"{key}.xlsx")
    df_sm_complete.to_excel(sm_output_path)


    try:
        df_cdf_complete = pd.concat(dfs_cdf)
        # on=["RDs", "ORPHAcode"]
        # patients patient  ORPHAcode RDs
        df_cdf_complete = df_cdf_complete.merge(df_sm_complete, on=[name_col1, name_col2], how="left")
        df_cdf_complete = df_cdf_complete.dropna()
        cdf_output_path = os.path.join(PATH_OUTPUT_SM, f"CDF_{key}.xlsx")
        df_cdf_complete.to_excel(cdf_output_path)
    except:
        #logger.info("{}\t empty CDF ".format(v))
        pass


    #logger.info(f"{key}\tconcat all sm and cdf\tTime : {time.perf_counter() - start_time} \t ")
