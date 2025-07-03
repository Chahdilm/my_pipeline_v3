from bin.set_log import *
 

# Ensure base output directory exists
output_dir = PATH_OUTPUT_FOLDER_MATRIX_ADD_PATIENT
noslash = output_dir.rstrip('/')
os.makedirs(noslash, exist_ok=True)

# Parse command-line arguments
parser = argparse.ArgumentParser(
    description="Add patient(s) into an existing MM matrix"
)
parser.add_argument(
    "--mm_prefix",
    required=True,
    help="Filename of the base MM matrix (e.g. mm_from_pd4_april2025.xlsx)",
)
parser.add_argument(
    "--sm_prefix",
    required=True,
    help="Prefix of the similarity-measure files (e.g. resnik_y_en_product4_avril2025_)",
)
args = parser.parse_args()

mm_prefix        = args.mm_prefix
sm_prefix        = args.sm_prefix.rstrip('_')


# mm_prefix="1_1_1_1_1_concat_matrix"
# sm_prefix='3_2_2_2_1_rsd_resnik_n_productmai2024_all_vectors_withontologyX' #"resnik_y_en_product4_avril2025_"
 
mm_file= f"{mm_prefix}.xlsx"
sm_file= f"{sm_prefix}.xlsx"

os.makedirs(PATH_OUTPUT_FOLDER_MATRIX_ADD_PATIENT, exist_ok=True)
# Create subdir for this SM run
run_dir = os.path.join(
    PATH_OUTPUT_FOLDER_MATRIX_ADD_PATIENT,
    mm_prefix
)
os.makedirs(run_dir, exist_ok=True)

print("2.START add patient to the matrix:")
# Load base matrix
df_matrice = pd.read_excel(
    os.path.join(PATH_OUTPUT_MM, mm_file),
    index_col=0
)

# df_matrice_m = df_matrice.pivot(index='OC1', columns='OC2', values='score')
# df_matrice_m.to_excel(f"{PATH_OUTPUT_MM}/matrix_{mm_file}")
print('Base matrix imported')
 
# Load patient list
df_patient = pd.read_excel(PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER_WITH_ONTOLOGYX, index_col=0)
print('Patient df imported')
user_seed = df_patient[COL_DF_PATIENT_PATIENT].drop_duplicates().tolist()
print(f'{len(user_seed)} patients to integrate')

# Load similarity scores
df_sm = pd.read_excel(
    os.path.join(PATH_OUTPUT_SM, sm_file),
    index_col=0
)
 
df_sm_d = df_sm.drop_duplicates(subset=['patients', 'RDs'])
print('Similarity DF imported')
# check the duplicated 
# duplicates = df_sm[df_sm.duplicated(subset=['patients', 'RDs'], keep=False)]
# print(duplicates)
sm_pivot =  df_sm_d.pivot(index='patients', columns='RDs', values='score')

i=0

 

# Iterate and add each patient
for patient in user_seed:
    out_csv = os.path.join(run_dir, f"{patient}.csv")

    if patient in out_csv:
        print(patient,i)
        t0 = time.perf_counter()
    
        scores = sm_pivot.loc[patient]
        # Defragment DataFrame storage for next iteration
        df_matrice_perp= df_matrice.copy()

        # Add column and row
        df_matrice_perp[patient] = scores.reindex(df_matrice_perp.index).fillna(0)
        df_matrice_perp.loc[patient] = scores.reindex(df_matrice_perp.columns).fillna(0)
        df_matrice_perp.at[patient, patient] = 0

        # Save per-patient version
        df_matrice_perp.to_csv(out_csv)
        print(f"Inserted {patient}; saved in {time.perf_counter() - t0:.1f}s")
        i=i+1
    else:
        print("patient already integrated ")


print('All patients integrated.')
