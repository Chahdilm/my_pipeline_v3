
from bin.set_log import * 


p = argparse.ArgumentParser()

p.add_argument('-f','--filter-type',required=True,help="vector_str (e.g. 2_2_1_1)")
p.add_argument("--col1",required=True)
p.add_argument("--col2",required=True)

args = p.parse_args()
vector_str = args.filter_type
name_col1 = args.col1
name_col2 = args.col2

# name_col1='OC1'
# name_col2='OC2'
# vector_str = '1_1_1_1_1'

 



xlsx_files = glob.glob(f"{PATH_OUTPUT_MM}/**/*.xlsx", recursive=True)
files_mm = []
for xlsx in xlsx_files:
    if f'/{vector_str}/' in xlsx:
        files_mm.append(xlsx)

rows = []
# store all df in a list 
for f in files_mm:
    try:
        df = pd.read_excel(f, usecols=["OC1", "OC2", "score"])
        if len(df) != len(files_mm):
            print(f'{f} don t match all RDs ! issues! ')
        else:
            # wide row → OC1 becomes the row label, OC2s become columns
            row = df.pivot(index="OC1", columns="OC2", values="score")
            rows.append(row)
    except ValueError:
        print(f'{f} dataframe might have an issue.')
        
print(f'all matrix stored in list ')




matrix = pd.concat(rows, axis=0)                 # long → wide
# duplicates = matrix[matrix.index.duplicated(keep=False)]

matrix_f = matrix.dropna()

# -------- square & tidy ----------
all_orphas = sorted(set(matrix_f.index).union(matrix_f.columns))
matrix_f     = matrix_f.reindex(index=all_orphas,
                            columns=all_orphas,
                            fill_value=0)


sm_output_path = os.path.join(PATH_OUTPUT_MM, f"{vector_str}_concat_matrix.xlsx")
matrix_f.to_excel(sm_output_path)

 