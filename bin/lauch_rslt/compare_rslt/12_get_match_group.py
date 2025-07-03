
from bin.set_log import * 

print(f"START  12_get_match_group")
t0 = time.perf_counter()

# PATH_OUTPUT_COMPARE_GLOBAL = '/home/maroua/Bureau/wip/my_pipeline_v2/output//compare_rank_1_1_1_1_1_concat_matrix//global/'
df = pd.read_excel(PATH_OUTPUT_COMPARE_GLOBAL + "/global_classif.xlsx",index_col=0)

# ─────── STEP 1: GROUP BY (patient, method) ───────
#
# We will loop over each combination of (type, method). In each sub‐DataFrame:
#  a) pick out the row(s) where is_rdi == 'y'.  (There should normally be exactly one distinct rd_id flagged as RDI, although you may see multiple rows for it if it's classified under multiple classif_id/group_id.)
#  b) record:  RDI_rd_id,  RDI_rank,  RDI_classif_ids, RDI_group_ids.
#  c) build a list of all unique rd_id sorted by ascending rank, then take the top 10.
#  d) for each of those top 10 rd_id, compare its (classif_id, group_id) sets to the RDI’s. If there is no overlap, compute a small “difference score.”
#     (Here we define “difference score” = (# of non‐overlapping categories). In other words:
#         – +1 if classif_id set has zero intersection
#         – +1 if group_id set has zero intersection
#       so difference ∈ {0,1,2}.)
#
# Finally, we’ll assemble a summary DataFrame at the end that shows, for each (patient, method), each of the top 10 rd_id, and that rd_id’s difference score.

# df=df[df["type"] == 'P0001068']

results = []  # we will append a row‐dict for every (patient,method,top10_rd_id)

# iterate over each (patient,method)
for (patient, mtd), sub in df.groupby(['type','method']):
    # 1a) find the RDI row(s)
    is_rdi_sub = sub[sub['is_rdi'] == 'y']
    if is_rdi_sub.empty:
        # no RDI marked for this (patient,method) – skip or record NaNs
        continue

    # We assume all rows in is_rdi_sub share the same rd_id and rank.
    # If by chance there are multiple distinct rd_id's with is_rdi='y', you could loop further,
    # but typically there is exactly one disease flagged as the RDI.
    RDI_rd_id   = is_rdi_sub['rd_id'].iloc[0]
    RDI_rank    = is_rdi_sub['rank'].iloc[0]

    # 1b) collect all the classif_id and group_id that belong to this RDI_rd_id
    RDI_rows = sub[sub['rd_id'] == RDI_rd_id]
    RDI_classif_ids = set(RDI_rows['classif_id'].unique())
    RDI_group_ids   = set(RDI_rows['group_id'].unique())

    # 2) Find the top 10 distinct diseases by smallest rank:
    #    (a) take just ('rd_id','rank'), drop duplicates so each rd_id appears once
    #    (b) sort by ascending rank
    #    (c) pick the first 10 rd_id's
    top10_rd = (
        sub[['rd_id','rank']]
        .drop_duplicates(subset=['rd_id'])
        .sort_values(by='rank', ascending=True)
        .head(10)['rd_id']
        .tolist()
    )

    # 3) For each rd_id in the top 10, compute a “difference score” versus the RDI’s sets.
    for candidate in top10_rd:
        cand_rows = sub[sub['rd_id'] == candidate]
        cand_classif_ids = set(cand_rows['classif_id'].unique())
        cand_group_ids   = set(cand_rows['group_id'].unique())

        # check overlap:
        classif_overlap = RDI_classif_ids.intersection(cand_classif_ids)
        group_overlap   = RDI_group_ids.intersection(cand_group_ids)
         # difference score = count of (no overlap in classif, no overlap in group)
        diff_score = (0 if classif_overlap else 1) + (0 if group_overlap else 1)

        # record one row in our results
        results.append({
            'patient': patient,
            'method': mtd,
            'RDI_rd_id': RDI_rd_id,
            'RDI_rank': RDI_rank,
            'RDI_classif_ids': sorted(RDI_classif_ids),
            'RDI_group_ids': sorted(RDI_group_ids),
            'candidate_rd_id': candidate,
            'candidate_rank': int(cand_rows['rank'].values[0]),
            'candidate_classif_ids': sorted(cand_classif_ids),
            'candidate_group_ids': sorted(cand_group_ids),
            'classif_overlap': len(classif_overlap),
             'group_overlap': len(group_overlap)

        })


# Turn our list of dicts into a DataFrame for easy viewing:
summary_df = pd.DataFrame(results)
#summary_df.to_excel('summary_df.xlsx')

# ─── 2) AGGREGATE OVERLAP COUNTS BY METHOD ───
agg_df = summary_df.groupby("method")[["classif_overlap", "group_overlap"]].sum().reset_index()

# ─── 3) PLOT A GROUPED BAR CHART ───
methods = agg_df["method"].tolist()
x = range(len(methods))
width = 0.35

fig, ax = plt.subplots(figsize=(6, 4))

# Bar for total classif overlap
ax.bar([i - width/2 for i in x], agg_df["classif_overlap"], width, label="Total classif overlap")
# Bar for total group overlap
ax.bar([i + width/2 for i in x], agg_df["group_overlap"], width, label="Total group overlap")

ax.set_xticks(x)
ax.set_xticklabels(methods)
ax.set_ylabel("Sum of Overlap Counts")
ax.set_title("Overlap with RDI by Method")
ax.legend()

plt.tight_layout()
plt.savefig(f"{PATH_OUTPUT_COMPARE_RSLT}/sum_overlap_methos.png", dpi=300)
# plt.show()

 

# ─── 2) COMPUTE CLASSIFICATION AND GROUP SIMILARITY PERCENTAGES SEPARATELY ───
def compute_classif_pct(row):
    rdi_cls = set(row['RDI_classif_ids'])
    cand_cls = set(row['candidate_classif_ids'])
    if len(rdi_cls) == 0:
        return 0.0
    return 100 * (len(rdi_cls & cand_cls) / len(rdi_cls))

def compute_group_pct(row):
    rdi_grp = set(row['RDI_group_ids'])
    cand_grp = set(row['candidate_group_ids'])
    if len(rdi_grp) == 0:
        return 0.0
    return 100 * (len(rdi_grp & cand_grp) / len(rdi_grp))

summary_df['classif_similarity_pct'] = summary_df.apply(compute_classif_pct, axis=1)
summary_df['group_similarity_pct'] = summary_df.apply(compute_group_pct, axis=1)

######################################################### 



# # ─── 2) DEFINE A JITTER FUNCTION ───
# def add_jitter(series, scale=1.5):
#     noise = np.random.normal(loc=0, scale=scale, size=len(series))
#     return series + noise

# # ─── 3) PLOT ONE SCATTER PER METHOD (WITHOUT RD NAMES) ───
# methods = summary_df['method'].unique()
# for method in methods:
#     sub = summary_df[summary_df['method'] == method].copy()
#     if sub.empty:
#         continue

#     # # Add a small jitter so overlapping points become visible
#     # np.random.seed(0)
#     # sub['x_jitter'] = add_jitter(sub['classif_similarity_pct'])
#     # sub['y_jitter'] = add_jitter(sub['group_similarity_pct'])

#     plt.figure(figsize=(6, 5))
#     plt.scatter(
#         sub['classif_similarity_pct'],
#         sub['group_similarity_pct'],
#         # sub['x_jitter'],
#         # sub['y_jitter'],
#         alpha=0.7,
#         edgecolors='k',
#         s=80
#     )

#     plt.xlabel('Classification Similarity (%)')
#     plt.ylabel('Group Similarity (%)')
#     plt.title(f'Method = {method}: Top-10 RDs vs. RDI')
#     plt.grid(True)
#     plt.xlim(-5, 105)   # keep 0–100 range plus margin for jitter
#     plt.ylim(-5, 105)
#     plt.tight_layout()
#     plt.show()

######################################################### 

 

# ─── 2) DEFINE METHODS AND PATIENTS ───
methods = ['RSD', 'RA', 'RARW']
patients = summary_df['patient'].unique()

# ─── 3) BUILD A FUNCTION THAT RETURNS AN HTML STRING FOR ONE METHOD‐CELL ───
def build_cell_html(pat, method):
    sub = summary_df[(summary_df['patient'] == pat) & (summary_df['method'] == method)]
    i_orange=0
    if sub.empty:
        return "NaN"
    parts = []
    for _, row in sub.iterrows():
        rd = row['candidate_rd_id']
        cls = row['classif_similarity_pct'] > 0
        grp = row['group_similarity_pct'] > 0
        if cls and grp:
            color = 'orange'
            i_orange = i_orange+1
        elif cls:
            color = 'lightblue'
        elif grp:
            color = 'red'
        else:
            color = None
        if color:
            # Wrap the RD in a <span> with background color
            parts.append(f"<span style='background-color:{color};padding:2px'>{rd}</span>")
        else:
            parts.append(rd)
    # Join with <br> so each RD appears on its own line
    return "<br>".join(parts),i_orange

# ─── 4) BUILD WIDE TABLE WITH ONE COLUMN PER METHOD, VALUES=HTML ⋄────────
dict_nbgroup={}
wide_html = pd.DataFrame(columns=['patient'] + methods)
for pat in patients:
    row = {'patient': pat}
    list_group_m = []
    for m in methods:
        row[m],i_group = build_cell_html(pat, m)
        list_group_m.append(i_group)
    
    dict_nbgroup[pat] = list_group_m
    wide_html = pd.concat([wide_html, pd.DataFrame([row])], ignore_index=True)
 
#### get the homogenity values :
rsd = 0
ra = 0
rarw=0
for key,value in dict_nbgroup.items():
    rsd =rsd + value[0]  
    ra =ra + value[1]
    rarw =rarw + value[2]
 

logger.info(f'The total number of RDs that belong to the same medical domain  is : RSD:{rsd}, RA: {ra}, RARW: {rarw}')

result = {}                    
for k, v in dict_nbgroup.items():    
    # get the max from value dict  
    mx = max(v)               
    indices = []  
    # get the index if multiple max             
    for i, x in enumerate(v):  
        if x == mx:
            indices.append(i)
    result[k] = (mx, indices)  


# patient_rarw = []
# patient_ra = []
# patient_rsd = []
# for k, v in dict_nbgroup.items():
#     ## best RARW
#     if (v[2] == max(v)) and (v[1] != max(v)) and (v[0] != max(v)):
#         patient_rarw.append(k)
#     ## best RA
#     if (v[1] == max(v)) and (v[2] != max(v)) and (v[0] != max(v)):
#         patient_ra.append(k)
#     ## best RSD
#     if (v[0] == max(v)) and (v[1] != max(v)) and (v[2] != max(v)):
#         patient_rsd.append(k)

#     ## best RSD RA
#     if (v[0] == max(v)) and (v[1] != max(v)) and (v[2] != max(v)):
#         patient_rsd.append(k)
 
 

# map index → label
labels = ['RSD', 'RA', 'RARW']
from collections import defaultdict
# build a dict: combination_of_labels → list of keys
comb_to_keys = defaultdict(list)

for patient, scores in dict_nbgroup.items():
    m = max(scores)
    # find all indices that tie for the max
    winners = tuple(labels[i] for i, sc in enumerate(scores) if sc == m)
    comb_to_keys[winners].append(patient)

# now extract each group:
patient_rsd         = comb_to_keys.get(('RSD',), [])
patient_ra          = comb_to_keys.get(('RA',), [])
patient_rarw        = comb_to_keys.get(('RARW',), [])
patient_rsd_ra      = comb_to_keys.get(('RSD','RA'), [])
patient_rsd_rarw    = comb_to_keys.get(('RSD','RARW'), [])
patient_ra_rarw     = comb_to_keys.get(('RA','RARW'), [])
patient_all_three   = comb_to_keys.get(('RSD','RA','RARW'), [])

logger.info(f"RSD only:      {len(patient_rsd)}")
logger.info(f"RA only:     {len(patient_ra)}")
logger.info(f"RARW only:    {len(patient_rarw)}")
logger.info(f"RSD + RA:    { len(patient_rsd_ra)}")
logger.info(f"RSD + RARW:   {len(patient_rsd_rarw)}")
logger.info(f"RA + RARW:   { len(patient_ra_rarw)}")
logger.info(f"All three:  {  len(patient_all_three)}")

 

 
wide_html.to_excel(PATH_OUTPUT_COMPARE_RSLT + "match_group_color.xlsx")

logger.info(f"END  12_get_match_group done in {time.perf_counter() - t0:.1f}s")
logger.info(f"END  12_get_match_group done in {time.perf_counter() - t0:.1f}s")

# ─── Convert to HTML with escape=False and display ───
# from IPython.display import HTML
# # wide_html_ff = wide_html[wide_html['patient'] == "P0005327"]
# html_str = wide_html.to_html(escape=False)
# display(HTML(html_str))
 
# wide_html_ff = wide_html[wide_html['patient'].isin(set(allp).difference(patientuniq))]
# html_str = wide_html_ff.to_html(escape=False)
# display(HTML(html_str))

logger.info(f"END  12_get_match_group done in {time.perf_counter() - t0:.1f}s")
print(f"END  12_get_match_group done in {time.perf_counter() - t0:.1f}s")




