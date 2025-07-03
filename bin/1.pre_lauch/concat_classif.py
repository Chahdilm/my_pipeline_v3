 
from bin.set_log import * 

path_xlsx = PATH_OUTPUT_PRODUCT_CLASSIF 

list_classif = os.listdir(path_xlsx)
list_classif_f = []
for one in list_classif:
    if 'json' not in one:
        list_classif_f.append(one)

print(f"Nb classif {len(list_classif_f)}")

list_df = []
for one_c in list_classif_f:
    df_class = pd.read_excel(path_xlsx + one_c ,index_col=0)

    list_df.append(df_class)
 
df_global = pd.concat(list_df)
 
# extract parent orpha with tout subtype
df_nosubtype = df_global[df_global["child_type"].isin(["Disease","Morphological anomaly","Malformation syndrome","Biological anomaly","Clinical syndrome" ]) ]


# Transformation: move child to parent, drop child
df_nosubtype['parent_id'] = df_nosubtype['child_id']
df_nosubtype['parent_type'] = df_nosubtype['child_type']
df_nosubtype['child_id'] = None
df_nosubtype['child_type'] = None
 
 
# Define the lists
valid_parent_types = [
    "Disease", "Morphological anomaly", "Malformation syndrome",    "Biological anomaly", "Clinical syndrome","Particular clinical situation in a disease or syndrome",
    "Clinical subtype","Etiological subtype","Histopathological subtype"
]
 

no_valid_child_type = [
    "Disease", "Morphological anomaly", "Malformation syndrome",    "Biological anomaly", "Clinical syndrome","Particular clinical situation in a disease or syndrome"
]

valid_child_subtypes = [
    "Etiological subtype", "Histopathological subtype", "Clinical subtype"
]

# 1. Keep all rows with valid parent_type and child_type as subtype
df_with_subtypes = df_global[
    (df_global["parent_type"].isin(valid_parent_types)) &
    (df_global["child_type"].isin(valid_child_subtypes))
]

# 2. Find parent_ids that have a subtype
parent_ids_with_subtype = df_with_subtypes["parent_id"].unique()
print(f"{len(parent_ids_with_subtype)} have a subtype")

# 3. parent that have no subtype
df_no_subtype = df_global[
    (~df_global["child_id"].isin(no_valid_child_type)) &
    (~df_global["parent_id"].isin(parent_ids_with_subtype))
]

# situation where a disease is relate to another disease 
df_subtype_disease = df_global[
    (df_global["parent_type"].isin(valid_parent_types)) &
    (~df_global["parent_id"].isin(parent_ids_with_subtype))
]

# 4. Concatenate both
df_parent_child = pd.concat([df_with_subtypes, df_no_subtype,df_subtype_disease], ignore_index=True)

df_parent_child[df_parent_child['parent_type'].isin(valid_parent_types)]['child_type'].drop_duplicates()

# Optional: sort by parent_id
df_parent_child = df_parent_child.sort_values(by="parent_id")

"""
ce que je ne veux pas -> des parent disorder avec des enfant vide et subtype (je dois supprimer les subtype)


ce que je veux
des parent groupe enfant disorder
parent disorder enfant subtype
parent disorder enfant disorder
parent subtype enfant subtype
"""
df_parent_child_noclassif = df_parent_child[['parent_id','parent_type','child_id','child_type']].drop_duplicates()

df_parent_child_noclassif[df_parent_child_noclassif['parent_id'] == "ORPHA:141115"]

df_parent_child.to_excel(PATH_OUTPUT_DF_PC_CLASSIF_v2)
df_parent_child_noclassif.to_excel(PATH_OUTPUT_DF_PC_v2)
