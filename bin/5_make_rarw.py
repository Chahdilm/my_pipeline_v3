from bin.set_log import *
 
 

def main():
    parser = argparse.ArgumentParser(
        description="Run Random Walk (alpha) for multiple seeds in one pass"
    )
    parser.add_argument(
        "--seeds", required=True,
        help="Space-delimited list of seeds patient IDs, e.g. 'P1 P2 P3'"
    )
    parser.add_argument(
        "--alpha", type=float, required=True,
        help="Teleportation (damping) factor for PageRank"
    )
    parser.add_argument(
        "--path_where_patientadded_is", required=True,
        help="Subdirectory under PATH_OUTPUT_FOLDER_MATRIX_ADD_PATIENT containing patient-added CSVs"
    )
    args = parser.parse_args()

    # Parse arguments
    seeds = args.seeds.split()
    alpha = args.alpha
    matrix_subdir = args.path_where_patientadded_is


    # matrix_subdir='1_1_1_1_1_concat_matrix' #3_2_2_2_1_funSimMax_resnik_n_productmai2024_all_vectors_withontologyX' 
    # alpha=0.04
    # seeds = ['P0007806']
 

    first_seed = seeds[0]


    # Ensure output directory for RW results exists
    os.makedirs(PATH_OUTPUT_FOLDER_RW, exist_ok=True)

    # Directory where per-patient matrices are stored
    matrix_dir = os.path.join(
        PATH_OUTPUT_FOLDER_MATRIX_ADD_PATIENT,
        matrix_subdir
    )

    path_rw_patient =os.path.join(PATH_OUTPUT_FOLDER_RW,str(alpha),matrix_subdir)
    os.makedirs(path_rw_patient, exist_ok=True)

    list_patient_already = os.listdir(path_rw_patient)
    for onep in list_patient_already:
        onep_not_ext = onep.split('.')[0]
        if first_seed == onep_not_ext:
            print("patient already done")
            exit(0)

    print("Patient start : ")
    # Load classification data and build count per RD
    data_classif = json.load(open(PATH_CLASSIFICATION_JSON))

    # Load adjacency matrix for the first seeds to build the graph once
    df_m = pd.read_csv(
        os.path.join(matrix_dir, f"{first_seed}.csv"),
        index_col=0
    )
    
    # Build NetworkX graph and normalize
    G_raw = nx.from_pandas_adjacency(df_m)
    G_raw.remove_edges_from(nx.selfloop_edges(G_raw))
    A = nx.adjacency_matrix(G_raw)
    df_adj = pd.DataFrame(
        A.toarray(),
        index=df_m.index,
        columns=df_m.columns
    )
    df_adj['tot'] = df_adj.sum(axis=1)
    df_norm = (
        df_adj
        .div(df_adj['tot'], axis=0)
        .drop(columns=['tot'])
    )
    G = nx.from_pandas_adjacency(df_norm)

    # Precompute sum of normalized degrees
    sum_degres = df_norm.sum().sort_values(ascending=False)

    # Load classification data and build count per RD
    class_count = {}
    for cls, rds in data_classif.items():
        for rd in rds:
            class_count[rd] = class_count.get(rd, 0) + 1


    t0 = time.perf_counter()

    # Build personalization vector
    personalization = {n: (1 if n == first_seed else 0) for n in G.nodes()}

    # Run PageRank once per alpha
    pr = nx.pagerank(G, personalization=personalization, alpha=alpha)
    pr.pop(first_seed, None)

    # Build result DataFrame
    df_pr = (
        pd.Series(pr, name='pg')
        .to_frame()
        .assign(
            sum_degres=lambda df: df.index.map(sum_degres),
            nb_classif=lambda df: df.index.map(lambda rd: class_count.get(rd, 0))
        )
    )
    df_pr['rank_pg'] = df_pr['pg'].rank(ascending=False, method='min')
    df_pr['rank_sum_degres_pg'] = df_pr['sum_degres'].rank(ascending=False, method='min')

 
    out_path = os.path.join(
        PATH_OUTPUT_FOLDER_RW,
        str(alpha),       
        matrix_subdir,
        f"{first_seed}.xlsx")
    df_pr.to_excel(out_path, engine='openpyxl')

    print(f"{first_seed} done in {time.perf_counter() - t0:.1f}s")

if __name__ == '__main__':
    main()
