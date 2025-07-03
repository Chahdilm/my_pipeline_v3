
from bin.set_log import *
from collections import deque
 

df_parent_child_noclassif = pd.read_excel(PATH_OUTPUT_DF_PC_v2,index_col=0)

 

df_patient = pd.read_excel(PATH_OUTPUT_DF_PATIENT,index_col=0)
df_patient_f = df_patient[['phenopacket',"hpo_id","Disease"]]


valid_types = [
    "Disease",
    "Morphological anomaly",
    "Malformation syndrome",
    "Biological anomaly",
    "Clinical syndrome",
    "Particular clinical situation in a disease or syndrome"
]
all_interactions= []
dict_df_patient_f =  df_patient_f.to_dict('index')
for value in dict_df_patient_f.values():
    patient = value['phenopacket']
    hpoid = value['hpo_id']
    disease = value['Disease']
    # test the disease type 
    type_disease = ""
    df_get_type = df_parent_child_noclassif[(df_parent_child_noclassif['parent_id'] ==disease ) | (df_parent_child_noclassif['child_id'] ==disease) ]
    print(disease)
    print(df_get_type)
    dict_df_get_type =  df_get_type.to_dict('index')
    for value in dict_df_get_type.values():
        parent_id = value['parent_id']
        parent_type = value['parent_type']
        child_id = value['child_id']
        child_type = value['child_type']
        
        foundin = ""
        # si la maladie est dans la colonne child 
        if disease in child_id:
            if child_type in valid_types:
                type_disease = child_type
                foundin = "child_id"
            # si non trouver alors il est dans la col parent  
            elif disease in parent_id: 
                type_disease = parent_type
                foundin = "child_id but parent "
            # sinon c'est un subtype meaning the parent are disorder
            elif parent_type in valid_types:
                foundin = "child_id_subtype"
                # get the related parent
                new_disease = parent_id 
                disease = parent_id 

                print(f"before {disease}, after {new_disease}")
                          
        elif disease in parent_id:
            if parent_type in valid_types:
                type_disease = parent_type
                foundin = "parent_id"
                print(f"before {disease}, after {new_disease}")
            elif child_type in valid_types:
                foundin = "parent_id_is_category"
                new_disease = child_id 
                disease = child_id 
                print(f"before {disease}, after {new_disease}")
        else :
            print(disease)
        

        print(f"{disease} type is {type_disease} found in {foundin}")
    all_interactions.append((patient,hpoid,disease,type_disease))

df_patient_only_disorder = pd.DataFrame(all_interactions,columns=["phenopacket",'hpo_id','Disease',"Disease_type"])

## verification 
list_rd_rd = df_patient_only_disorder['Disease'].drop_duplicates().tolist()
len(list_rd_rd)
for one in list_rd_rd:
    disease_rd = one
    print("##############################")
    print("###  ",one,"\n")
    print(df_parent_child_noclassif[(df_parent_child_noclassif['parent_id'] ==disease_rd ) | (df_parent_child_noclassif['child_id'] ==disease_rd) ])
    print("##############################")



rd_patient = df_patient_f['Disease'].drop_duplicates().tolist()
rd_only_disorder_patient = df_patient_only_disorder['Disease'].drop_duplicates().tolist()

len(set(rd_patient).intersection(rd_only_disorder_patient))

# difference between rd_patient et rd_only_disorder_patient
set(rd_patient).difference(rd_only_disorder_patient)
len(set(rd_patient).difference(rd_only_disorder_patient))

# difference between rd_patient et rd_only_disorder_patient meaning the subtype 
set(rd_patient).difference(rd_only_disorder_patient)
len(set(rd_patient).difference(rd_only_disorder_patient))

## verif the type of a rd
disease_rd =  'ORPHA:216975'
df_parent_child_noclassif[(df_parent_child_noclassif['parent_id'] ==disease_rd ) | (df_parent_child_noclassif['child_id'] ==disease_rd) ]

df_patient_only_disorder.to_excel(PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER_v2)
 
 
