from bin.classes.datagenerate import *



class DataSet(DataGenerate):
    def __init__(self, input_path, output_path):
        super().__init__(input_path, output_path)

    ############################################################
    #####                 Build df patients                #####
    ############################################################

    def build_patients_df(self):
        pheno_with_invalid_id = set()
        empty_no_phenotypic_feature = set()

        patients_raw = os.listdir(self.input_path)

        list_case_HPO = []

        for onefile in patients_raw:
            with open(self.input_path+str(onefile),'r',encoding = 'utf8') as file_phenopacket_result:
                try :
                    one_phenopacket_result = json.load(file_phenopacket_result)

                    id_phenopacket = one_phenopacket_result['id']
                    ### get the SOLVED/UNSOLVED info if exist
                    try :
                        progress_status = one_phenopacket_result['interpretations'][0]['progressStatus']
                    except KeyError:
                        progress_status = 'no_info'
                        #self.no_progressStatus.add(id_phenopacket)

                    ### get the ERN info     
                    ern = one_phenopacket_result['metaData']['externalReferences'][0]['id']

                    ### get the genetic information -gene variant) if exist
                    type_gene = 'no_info'
                    gene = 'no_info'
                    variant = 'no_info'
                    interpretations_section = one_phenopacket_result['interpretations'][0]
                    if 'diagnosis' in interpretations_section.keys():
                        try :
                            gene_section = interpretations_section['diagnosis']['genomicInterpretations']
                            # le cas ou le type du gene est present sinon pas d'info
                            if 'interpretationStatus' in gene_section[0].keys():
                                type_gene = gene_section[0]['interpretationStatus']
                            if 'gene' in gene_section[0].keys():
                                gene = gene_section[0]["gene"]['symbol']
                            elif 'variantInterpretation' in gene_section[0].keys():
                                variant = gene_section[0]["variantInterpretation"]['acmgPathogenicityClassification']
                                gene = gene_section[0]["variantInterpretation"]['variationDescriptor']['geneContext']['symbol']
                        except KeyError:
                            #self.no_genomicInterpretations.add(id_phenopacket)
                            pass


                    ### get the disease inf if exist
                    disease = 'no_info'
                    disease_omim = "no_info"
                    disease_orphanet = "no_info"
                    if 'diseases' in one_phenopacket_result.keys():
                        for oneel in one_phenopacket_result['diseases']:
                            disease = oneel['term']['id']
                            if "OMIM" in disease:
                                disease_omim = disease
                            elif "Orphanet" in disease:
                                splited = disease.split(':') 
                                disease_orphanet =str("ORPHA:") + splited[1]  # to avoid Orphanet:000



                    ### phenotypicFeatures dict key store hpo
                    if 'phenotypicFeatures' in one_phenopacket_result.keys():
                        #  list_hpo contains all HPO terms
                        list_hpo = one_phenopacket_result['phenotypicFeatures']
                        if not bool(list_hpo):
                            # empty list
                            #self.empty_no_phenotypic_feature.add(id_phenopacket)
                            pass


                        else :
                            # HERE dict hpo not empty and exist !!
                            hpo_temp = []
                            for onehpo in list_hpo:
                                # sometime it s like this  [{}] ... list filled with en empty dict !
                                if not bool(onehpo):
                                    #self.empty_no_phenotypic_feature.add(id_phenopacket)
                                    pass
                                else:
                                    # fill the hpo_temp list
                                    try:
                                        id_hpo = ""
                                        label_hpo = ""
                                        if (("Invalid id" == onehpo['type.label'])):
                                            pheno_with_invalid_id.add(id_phenopacket)


                                        elif ( 'type.negated' not in onehpo.keys()):
                                            hpo_temp.append(onehpo['type.label']['id'])
                                            id_hpo = onehpo['type.label']['id']
                                            label_hpo = onehpo['type.label']['label']

                                    except KeyError:
                                        # json format dict may also have this structure : label and not type.label
                                        if (("Invalid id" == onehpo['type']['label']) ):
                                            pheno_with_invalid_id.add(id_phenopacket)

                                        elif ( 'negated' not in onehpo.keys()):
                                            hpo_temp.append(onehpo)
                                            id_hpo = onehpo['type']['id']
                                            label_hpo = onehpo['type']['label']

                                if ((id_phenopacket not in pheno_with_invalid_id) and (id_phenopacket not in empty_no_phenotypic_feature)):
                                    # if the number of element in hpo_temp is hight than 5 then the phenopacket contains more than 5HPO
                                    list_case_HPO.append((id_phenopacket,progress_status,disease_orphanet,disease_omim,ern,gene,type_gene,variant,id_hpo,label_hpo))

                    else:
                        # if not phenotypicFeatures dict in the phenopacket file
                        #self.no_phenotypic_feature.add(id_phenopacket)
                        pass

                except (json.JSONDecodeError,UnicodeDecodeError):
                    # can t read the json file
                    #self.invalid_json.add(id_phenopacket)
                    pass
        df_raw_info = pd.DataFrame(list_case_HPO, columns=["phenopacket",'status','Orphanet','OMIM','ern','gene','type_gene','variant','hpo_id','hpo_label'])
        return df_raw_info
    

    ############################################################
    #####         comfirmed patients SolveRD               #####
    ############################################################

    def filter_df_keep_comfirmed_only(self,path_input_p,df_input_p,col_patient):
        """import df of confirmed patient and merge it with the df patient with hpo to get the final df confirmed patient with hpo"""
        df_phenopacket_confirmed = pd.read_excel(path_input_p,engine='openpyxl',sheet_name='Feuil2')

        # filter keep only comfirmed and not the solve and comfirmed 
        df_phenopacket_confirmed = df_phenopacket_confirmed[df_phenopacket_confirmed['Result'] == "yes"]
        #df_phenopacket_confirmed = df_phenopacket_confirmed[df_phenopacket_confirmed['Result'].isin(["yes","ext","inc"])]

        # nb of patients comfirmed 
        patients_c = df_phenopacket_confirmed['Patient ID'].drop_duplicates().tolist()
        # extract col
        df_phenopacket_confirmed = df_phenopacket_confirmed[['Patient ID',"Gene","Disease found ORPHA"]]
        # rename col 
        df_phenopacket_confirmed.columns = [col_patient,"Gene_p","Disease"]

        # filter based on comfirmed patients 
        df_raw_comfirmed = df_input_p[df_input_p[col_patient].isin(patients_c)]
        
        # merge 
        df_m = pd.merge(df_raw_comfirmed, df_phenopacket_confirmed, on=col_patient,how='outer')

        return df_m.dropna(subset=['hpo_id'])
    
    ########################################################################################################################

    ############################################################
    #####              Build df orpha with hpo             #####
    ############################################################

    def from_rsd_build_orpha_df(self):
        """ Build the df rd 
            warn and list disorders with no HPO associations """
        # Load the JSON data
        with open(self.input_path, 'r') as f:
            data = json.load(f)

        rows = []
        missing = []  # will hold ORPHA codes with zero associations

        for disorder in data['JDBOR']['DisorderList']['Disorder']:
            orpha = disorder.get('OrphaCode')
            assoc = disorder.get('HPODisorderAssociationList', {}).get('HPODisorderAssociation', [])

            # normalize single‐dict → list
            if isinstance(assoc, dict):
                assoc = [assoc]

            # if no associations, add into the missing list and skip
            if not assoc:
                missing.append(f"ORPHA:{orpha}")
                continue

            # otherwise one row per HPO association
            for a in assoc:
                ok_rsd = 1
                onehpo = a.get('HPO', {})
                freq_text = a.get('HPOFrequency', {}).get('Name', {}).get('#text', None)
                # because it s for RDS some frequence are not taking into account 

                if (('Very frequent' in freq_text) or ('Occasional' in freq_text) or ('Obligate' in freq_text)):
                    if   "Very frequent" in freq_text: 
                        freq = 4/5

                    elif "Occasional" in freq_text: 
                        freq = 2/5

                    elif ("Obligate"  in freq_text ): 
                        freq = 1

                    elif "Frequent" in freq_text: 
                        freq = 3/5

                    elif "Very rare"in freq_text: 
                        freq = 1/5
        
                    elif  ("Excluded"  in freq_text ):
                        freq = 0

                    else: freq = None
                    
                    rows.append({
                        'ORPHAcode': f"ORPHA:{orpha}",
                        'hpo_id':    onehpo.get('HPOId'),
                        #'hpo_term':  onehpo.get('HPOTerm'),
                        'hpo_frequency':  freq
                    })


        df = pd.DataFrame(rows)
        print(f"{df.ORPHAcode.nunique() } RDs with HPO associations.")
        # Warn the user about missing associations
        if missing:
            print(f"Warning: {len(missing)} disorders have no HPO associations.")
            print(", ".join(missing))

        return df




    def build_orpha_df(self):  
        """ Build the df of orphacode and it s called in the call_build_df methods"""
        with open(self.input_path,'r') as file_phenopacket_result:
            root = json.load(file_phenopacket_result)
        all_interactions = []

        root_diseases = root['JDBOR']['HPODisorderSetStatusList']['HPODisorderSetStatus']

        for one_dict in root_diseases:
            the_dict = one_dict['Disorder']
            id_disease =  the_dict['OrphaCode']
            #print(id_disease)
            section_hpo = the_dict['HPODisorderAssociationList']
            if "HPODisorderAssociation" in section_hpo.keys():
                the_dict_hpo = section_hpo['HPODisorderAssociation']
            
                for one_hpo_dict in the_dict_hpo:

                    try :
                        if "@id" in one_hpo_dict.keys():
                            hpo_id = one_hpo_dict['HPO']['HPOId']
                            hpo_frequency = one_hpo_dict['HPOFrequency']["Name"]["#text"]

                        else:
                            hpo_id = one_hpo_dict['HPO']['HPOId']
                            hpo_frequency = one_hpo_dict['HPOFrequency']["Name"]["#text"]


                    except AttributeError:
                        hpo_id = the_dict_hpo['HPO']['HPOId']
                        hpo_frequency = the_dict_hpo['HPOFrequency']["Name"]["#text"]
                     
                    # set frequency a number
                    hpo_frequency_int = 0
                    if "Very frequent" in hpo_frequency:
                        hpo_frequency_int = 4/5
                    elif "Frequent" in hpo_frequency:
                        hpo_frequency_int = 3/5
                    elif "Occasional " in hpo_frequency:
                        hpo_frequency_int = 2/5
                    elif "Very rare" in hpo_frequency:
                        hpo_frequency_int = 1/5
                    elif "Obligate" in hpo_frequency:
                        hpo_frequency_int = 1
                    elif "Excluded" in hpo_frequency:
                        hpo_frequency_int = 0 # way to recognize the hpo excluded 
                        # excluded mean that if the patient hase the hpo thus he don't have the disease
                    else:
                        print('issue ?')

                    all_interactions.append((str("ORPHA:")+id_disease,hpo_id,hpo_frequency_int))
        
        df_orpha_info = pd.DataFrame(all_interactions,columns=['ORPHAcode','hpo_id','hpo_frequency'])
        return df_orpha_info
 


    ########################################################################################################################
    
    ############################################################
    #####               Build df for pd1                   #####
    ############################################################
    def df_pd1(self):
        with open(self.input_path,'r') as file_phenopacket_result:
            root = json.load(file_phenopacket_result)

        root_diseases_json = root['JDBOR']['DisorderList']['Disorder']
        all_interactions_json = set()
        for one_dict in root_diseases_json:
            id_disease =  one_dict['OrphaCode']
            name_disease =  one_dict['Name']['#text']

            section_type = one_dict['DisorderType']['Name']['#text']
            section_group = one_dict['DisorderGroup']['Name']['#text']
            all_interactions_json.add((str("ORPHA:"+id_disease),name_disease,section_type,section_group))
        df_pd1 = pd.DataFrame(all_interactions_json,columns=["ORPHACode","Name","Type","Group"])
        return df_pd1

    def df_pd7(self):
        with open(self.input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Récupérer la liste des maladies
        try:
            disorders = data['JDBOR']['DisorderList']['Disorder']
        except KeyError as e:
            raise KeyError(f"Clé manquante dans la structure JSON : {e}")

        all_interactions = set()

        # Parcourir les maladies
        for disorder in disorders:
            # print(disorder)
            disease_id = disorder.get('OrphaCode')
            association_list = disorder.get('DisorderDisorderAssociationList', {})
            count_value = association_list.get('@count', '0')
            
            if count_value == '0':
                print(f"{disease_id} has no association classif ")
            # Si le nombre d'associations est différent de '1', on considère qu'il y a plusieurs associations
            elif count_value != '1':
                associations = association_list.get('DisorderDisorderAssociation')
                # Dans le cas où associations n'est pas une liste (mais un seul objet), le transformer en liste
                if not isinstance(associations, list):
                    associations = [associations]
                
                for association in associations:
                    target = association.get('TargetDisorder')
                    if target:
                        parent_id = f"ORPHA:{target.get('OrphaCode', '')}"
                        # Récupérer le nom via la clé '#text'
                        parent_name = target.get('Name', {}).get('#text', '')
                        verif_pp = association.get('DisorderDisorderAssociationType', {})\
                                            .get('Name', {})\
                                            .get('#text', '')
                        all_interactions.add((f"ORPHA:{disease_id}", parent_id, parent_name, verif_pp))
            else:
                # Cas d'une seule association
                association = association_list.get('DisorderDisorderAssociation')
                if association:
                    target = association.get('TargetDisorder')
                    if target:
                        parent_id = f"ORPHA:{target.get('OrphaCode', '')}"
                        parent_name = target.get('Name', {}).get('#text', '')
                        verif_pp = association.get('DisorderDisorderAssociationType', {})\
                                            .get('Name', {})\
                                            .get('#text', '')
                        all_interactions.add((f"ORPHA:{disease_id}", parent_id, parent_name, verif_pp))
        

        df_pd7 = pd.DataFrame(all_interactions,columns=["ORPHACode","Classif_id","Classif_name","Classif_type"])
        return df_pd7

    ###################################################################################
    #####                                  From orphacode get classif             #####
    ###################################################################################
    # jsp si c'est compatible pour toute les classif 
    def traverse_node(self,node, root_orpha_id, root_orpha_name, interactions):
        """
        Recursively traverses a classification node, adds the association between the
        parent and each child to the interactions set, and continues deeper into each node.
        
        Each tuple in interactions is of the form:
        (root_orpha_id, root_orpha_name, parent_id, parent_type, child_id, child_type)
        """
        # Get current node's disorder info
        current_disorder = node.get("Disorder", {})
        parent_id = "ORPHA:" + current_disorder.get("OrphaCode", "")
        parent_type = current_disorder.get("DisorderType", {}).get("Name", {}).get("#text", "")
        
        # Get the child list if present
        child_list = node.get("ClassificationNodeChildList", {})
        associations = child_list.get("ClassificationNode")
        
        if associations:
            # Ensure associations is a list (even if there's only one child)
            if not isinstance(associations, list):
                associations = [associations]
            
            for association in associations:
                target = association.get("Disorder", {})
                child_id = "ORPHA:" + target.get("OrphaCode", "")
                child_type = target.get("DisorderType", {}).get("Name", {}).get("#text", "")
                
                # Add the link from the current (parent) node to the child
                interactions.add((root_orpha_id, root_orpha_name, parent_id, parent_type, child_id, child_type))
                
                # Recursively traverse the current child association for deeper levels
                DataSet.traverse_node(self,association, root_orpha_id, root_orpha_name, interactions)
    
    def df_classif(self):
        with open(self.input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Initialize the set to store associations
        all_interactions = set()

        # Extract the root classification node
        classification = data['JDBOR']['ClassificationList']["Classification"]
        root_node = classification['ClassificationNodeRootList']['ClassificationNode']
        root_disorder = root_node.get("Disorder", {})
        root_orpha_id = "ORPHA:" + root_disorder.get("OrphaCode", "")
        root_orpha_name = root_disorder.get("Name", {}).get("#text", "")

        # Get immediate child nodes; ensure it is a list
        child_nodes = root_node.get("ClassificationNodeChildList", {}).get("ClassificationNode", [])
        if not isinstance(child_nodes, list):
            child_nodes = [child_nodes]

        # Traverse every immediate child node
        for node in child_nodes:
            DataSet.traverse_node(self,node, root_orpha_id, root_orpha_name, all_interactions)

        # Create a Pandas DataFrame with the collected data
        df_pd_classif = pd.DataFrame(
            list(all_interactions),
            columns=["root", "root_name", "parent_id", "parent_type", "child_id", "child_type"]
        )
        return df_pd_classif



    ###################################################################################
    #####       From orphacode get theirs parents(orphapckets and pd1)            #####
    ###################################################################################

    def orphacodes_n_parents(self,path,df_pd1):
        ## extract the list of orphacode that are available on pd1
        orphacodes_from_pd1 = df_pd1['ORPHACode'].drop_duplicates().tolist()

        ## extract all orphapackets
        all_orphapackets  = glob.glob(os.path.join(path+"/orphapackets/", "*.json"))

        ## based on orphapacket files and pd1 build the df oh orphacode and their child 
        all_interactions = set()
        #all_orphapackets = ['./input//orphapackets/ORPHApacket_66629.json']
        for one_file in all_orphapackets:
            with open(one_file,'r') as file_orphapacket:

                root = json.load(file_orphapacket)
                root_diseases = root['Orphapacket']

                orpha_code = str("ORPHA:" + root_diseases["ORPHAcode"]) 
                disorder_type = root_diseases["DisorderType"]['value']
                
                if "Parents" in root_diseases.keys():
                    parents = root_diseases['Parents']
                    if isinstance(parents, dict):
                        parent_id = str("ORPHA:"+parents['Parent'][0]['ORPHAcode'])
                        if parent_id in orphacodes_from_pd1:
                                        parent_type = df_pd1[df_pd1['ORPHACode'] == parent_id]['Type'].values[0]
                                        all_interactions.add((orpha_code,disorder_type,parent_id,parent_type))
                    else:
                        for one_parent in parents:
                            for one_parent_list in one_parent['Parent']:
                                #print(one_parent_list['ORPHAcode'])
                                parent_id = str("ORPHA:"+one_parent_list['ORPHAcode'])
                                if parent_id in orphacodes_from_pd1:
                                    parent_type = df_pd1[df_pd1['ORPHACode'] == parent_id]['Type'].values[0]
                                    all_interactions.add((orpha_code,disorder_type,parent_id,parent_type))
                else:
                    ## the orphacode don't have parent 
                    all_interactions.add((orpha_code,disorder_type,"",""))

        orphacode_parent = pd.DataFrame(all_interactions,columns=['ORPHACode',"Type","ORPHACode_p","Type_p"])
        return orphacode_parent







    ########################################################################################################################

    ############################################################
    #####     Build df match omim orpha id and gene        #####
    ############################################################
    def df_omim_orpha(self,root):

        tuple_interaction = []
 
        root_diseases = root['JDBOR']['DisorderList']['Disorder']

        for one_dict in root_diseases:
            id_disease =  one_dict['OrphaCode']
            try :
                section_externalref = one_dict['ExternalReferenceList']['ExternalReference']
                for key,value in section_externalref[0].items():
                    if value == 'OMIM':
                        id_omim =  section_externalref[0]['Reference']
                        tuple_interaction.append((id_disease,id_omim))
                        #print("{}\t{}".format(id_disease,id_omim))
            except KeyError as exc:
                #print('generated an exception: %s' % ( exc))   
                pass
        print("build df pd1  ")
        
        return pd.DataFrame(tuple_interaction,columns=['OrphaCode','OMIM'])



    ########################################################################################################################

    ############################################################
    #####               Build DICT prevalence              #####
    ############################################################
    def build_df_prevalence(self):
        all_prev = []

        with open(self.path_json,'r',encoding="ISO-8859-1") as file_result:
            root = json.load(file_result)
        
        for onedict in root:
            orpha = onedict['orpha']
            preval = onedict['preval']
            all_prev.append((orpha,preval))
        
        return pd.DataFrame(all_prev,columns=["ORPHAcode","Estimated_prevalence"])

     
    def from_dict_to_df(self,dict_synth_patient,str_type):
        all_interactions = []
        for key,value in dict_synth_patient.items():
            for onehpo in value:
                all_interactions.append((str(str_type)+str(key),onehpo))
        df_patient_synthetic = pd.DataFrame(all_interactions,columns=['Patient','hpo_id'])
        return df_patient_synthetic



    
    ############################################################
    #####                synthetic patient                 #####
    ############################################################

    """ 
    Générer de trois nombre aléatoire uniformément  distrbuter entre 0 et 100.

    inférieur a 50 -> caractéristique A est donnée au patient simulé

    inférieur a 70 -> caractéristique B est donnée au patient simulé

    inférieur a 10 -> caractértisque C est donnée au patient

    Independance a chaque fois on generer trois nombres.
    <i> ref phenomiser </i>
    --> pas besoin de faire tout cela on a deja nos patients !!!!
    """

    ############################################################
    #####                   Noisy patients                 #####
    ############################################################
    """ 
    Les hpos aléatoire ne doivent pas etre en doublons des hpo optimaux
    Generate random set of HPO based on patients confirmed and uniform distribution
    """

    def build_noisy_patient(self,list_random_hpo,dict_omim):
    
        dict_omim_random = {}
        for key,value in dict_omim.items():
            half_stop = len(value) // 2
            # garde uniquement la deuxieme moitié 
            half_value = value[half_stop:]
            while len(half_value) != len(value):
                random_number = np.random.randint(0, len(list_random_hpo))
                random_hpo= list_random_hpo[random_number].strip()
                if random_hpo not in value:
                    half_value.append(random_hpo)
                    
            dict_omim_random[key] = half_value
        return dict_omim_random



    ############################################################
    #####              Imprecision patients                #####
    ############################################################
    ### Imprecision simulated dataset 
    #### Generate imprecision simulated patients dataset replace half hpo by their ancestor
    """ 
    - remove half of the hpo of each patients
    - call hpo3
    - replace by the first ancester
    - dont make verif because sometime some hpo have the same parent    
    """

    def build_imprecision_patient(self,dict_omim):
        dict_omim_imprecision = {}
        for key,value in dict_omim.items():
            half_stop = len(value) // 2
            
            half_second_oneline = list(value[half_stop:])
            half_first_oneline = value[:half_stop]
            # focus on the half first because it's what we want to replace
            new_half_first_oneline = []
            for one_el in half_first_oneline:
                try :
                    # convert into hpoterm type
                    terme = Ontology.get_hpo_object(one_el)
                    # direct patient
                    parent_term = terme.parent_ids()
                    # get the first parents
                    parent_term_id = Ontology.get_hpo_object(parent_term[0]).id
                except Exception as e:

                    # meaning there is not direct parent so :
                    # undirected_parent = list(terme.all_parents)
                    # oneparent_undirected = undirected_parent[0].id

                    # etant donnée que les hpo qui arrive ici n'ont pas de lien avec la racine je met phenotypic abormality comme parent ... HP:0000118
                    parent_term_id = "HP:0000118"

                # dont make verif because sometime some hpo have the same parent 
                new_half_first_oneline.append(parent_term_id)
            newonline = half_second_oneline+new_half_first_oneline
            dict_omim_imprecision[key] = newonline
        return dict_omim_imprecision

    ########################################################################################################################

    ############################################################
    #####            Load and Build matrice MM             #####
    ############################################################
    def load_build_mm(self,json_to_extract):

        ## get all files mm 
        all_mm_files = glob.glob(os.path.join(self.input_path, "*.xlsx"))

        i=0
        all_mm_files_f = []
        for file in all_mm_files:
            for motif in json_to_extract:
                if motif in file:
                    all_mm_files_f.append(file)
                    i=i+1
    
        ## concatenate all df loaded into one big
        df_all_mm_resnik = pd.concat((pd.read_excel(f) for f in set(all_mm_files_f)), ignore_index=True)
        ## change the structure 
        df_matrice_mm = df_all_mm_resnik.pivot(index='j', columns='i', values='resnik')

        df_matrice_mm_sub = df_matrice_mm.loc[json_to_extract,json_to_extract]

        return df_matrice_mm_sub
