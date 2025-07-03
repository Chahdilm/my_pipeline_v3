from bin.set_log import * 



class Sim_measure():
    def __init__(self,df_group1,df_group2,colname_1,colname_2):
        #self.dict_ic = dict_ic
        self.df_group1 = df_group1
        self.df_group2 = df_group2
        self.colname_1  = colname_1
        self.colname_2  = colname_2

    ############################################################
    #####                  calcul section                  #####
    ############################################################
    
    

    def get_hpo_set(self, hpo_list):
        valid_terms = []
        for term in hpo_list:
            try:
                # Check if the term is valid by attempting to create a single-term HPOSet
                term_v = Ontology.get_hpo_object(term)
                valid_terms.append(term_v.id)
            except RuntimeError:
                logging.warning(f"Unknown HPO term encountered and skipped: {term}")
        
        if not valid_terms:
            raise ValueError("No valid HPO terms found in the provided list.")

        # Now create the HPOSet with only valid terms
        return valid_terms

   
    def sm_hpoSet_add(self,listHPO_goup1,listHPO_group2,type_sm): 
        
        list_1_HPO = self.get_hpo_set(listHPO_goup1)
        list_2_HPO = self.get_hpo_set(listHPO_group2)
                
        list_1_HPOSet = HPOSet.from_queries(list_1_HPO)
        list_2_HPOSet = HPOSet.from_queries(list_2_HPO)

                    
        ###### Sim measure function #######
        # resnik, lin, graphic 
        type_sm_max = list_1_HPOSet.similarity(list_2_HPOSet,method=type_sm,kind ='orpha')
     
        return type_sm_max # because now i have one interaction and not on patient in all


    def sm_hpoTerm_add(self,listHPO_1,listHPO_2,type_sm,mini_df_ok_freq):
        hpo_freq = 1
        all_max_sm = []
        for id_hpo1 in listHPO_1:
            id_hpo1_v = Ontology.get_hpo_object(id_hpo1)
            dict_sm ={}

            try:
                for id_hpo2 in listHPO_2:
                    id_hpo2_v = Ontology.get_hpo_object(id_hpo2)
                                        
                    if type_sm == 'hpo_frequency':
                        sm =  id_hpo1_v.similarity_score(id_hpo2_v, kind="orpha",method=type_sm)
                    else:
                        sm =  id_hpo1_v.similarity_score(id_hpo2_v, kind="orpha",method=type_sm)

                    dict_sm[sm] = (id_hpo1,id_hpo2)
                
                sm_max = max(dict_sm.keys())
                sm_max_hpo1 = dict_sm[sm_max][0]
                sm_max_hpo2 = dict_sm[sm_max][1]
                #print(sm_max_hpo2,sm_max_hpo1)
                if type_sm == 'hpo_frequency':
                    hpo_freq = mini_df_ok_freq[ (mini_df_ok_freq['hpo_id'] == sm_max_hpo2)]["hpo_frequency"].values[0]



            except RuntimeError:
                sm_max = 0
                sm_max_hpo1 = 0
                sm_max_hpo2 = 0
                hpo_freq = 0
            



            sm_max_freq  = sm_max * hpo_freq
            all_max_sm.append(sm_max_freq)

        return sum(all_max_sm)/len(listHPO_1) 
    
    def choose_set_term(self,listHPO_1,listHPO_2,type_sm,mini_df_ok_freq,set_type):
        sm_val = ""
        if set_type == 1:
            sm_val = Sim_measure.sm_hpoTerm_add(self,listHPO_1,listHPO_2,type_sm,mini_df_ok_freq)
        elif set_type == 2:
            sm_val = Sim_measure.sm_hpoSet_add(self,listHPO_1,listHPO_2,type_sm)
        return sm_val




    ############################################################
    #####                Export association                #####
    ############################################################

    def export_association(self,path_output,col_name_1,col_name_2,type_sm,hpo3_type):
        list_groupe1 = self.df_group1[self.colname_1].drop_duplicates().tolist()
        list_groupe2 = self.df_group2[self.colname_2].drop_duplicates().tolist()

        ## Construction toute les associations 
        print(f"Build nb :  {len(list_groupe1)} - {len(list_groupe2)}")
        ## export MM association
        i = 0
        for g1_id in list_groupe1: 
            listHPO_1 = self.df_group1[self.df_group1[self.colname_1] == g1_id]["hpo_id"].drop_duplicates() 

            tuple_MR_sim = []
            j=0
            for g2_id in list_groupe2: 
                
                listHPO_2 = self.df_group2[self.df_group2[self.colname_2] == g2_id]["hpo_id"].drop_duplicates() 
                
                if ((hpo3_type == 'hpoTERM')):
                    # frequency section 
                    if 'hpo_frequency' in self.df_group1.columns:
                        df_ok_freq  = self.df_group1 
                        mini_df_ok_freq = df_ok_freq[(df_ok_freq['ORPHAcode'] == g1_id)]
                    elif 'hpo_frequency' in self.df_group2.columns:
                        df_ok_freq  = self.df_group2
                        mini_df_ok_freq = df_ok_freq[(df_ok_freq['ORPHAcode'] == g2_id)]


                    rslt_sim = Sim_measure.sm_hpoTerm_add(self,listHPO_1,listHPO_2,type_sm,mini_df_ok_freq)


                else:
                    rslt_sim = Sim_measure.sm_hpoSet_add(self,listHPO_1,listHPO_2,type_sm)
                tuple_MR_sim.append((g1_id,g2_id,rslt_sim))


                j=j+1
                #print(f"{i},{j}")
            print(f"{i},{j}")
            df_sm =  pd.DataFrame(tuple_MR_sim, columns=[col_name_1,col_name_2,type_sm])
            
            #create rank
            df_sm = df_sm.sort_values(type_sm,ascending=False)
            df_sm['rank'] = list(range(1,len(df_sm)+1))
            #df_sm.to_excel(path_output+g1_id+hpo3_type+".xlsx")
            df_sm.to_excel(path_output+g1_id+'_'+hpo3_type+".xlsx")

            i=i+1
        return df_sm

    ###############################################################################""
    # PHASE TWO
    ###############################################################################""

    def set_freq_for_sm(self,one_hpo_valid,the_mini_df,vector_weight,is_freq):
        try:
            #temp_df = minidf_2.set_index('hpo_id').drop_duplicates()
            temp_df = the_mini_df[the_mini_df['hpo_id'] == one_hpo_valid.id]['hpo_frequency']
            hpo_frequency = temp_df.values[0]
            #logger.info(f"({one_hpo_valid.id}\t Freq : {hpo_frequency}")
            add_weight=1
            if (hpo_frequency == 1) : 
                # Obligate  5/5
                add_weight = vector_weight[0] 
            elif  (hpo_frequency == 0.8) : 
                # Very frequent 4/5 
                add_weight = vector_weight[1] 
            elif  hpo_frequency == 0.6  :
                # Frequent3/5
                add_weight = vector_weight[2]  
            elif hpo_frequency == 0.4:
                # Occasional 2/5
                add_weight = vector_weight[3]  
                # Very rare  1/5
            elif hpo_frequency ==0.2:
                add_weight = vector_weight[4]    

        except KeyError:
            hpo_frequency_el = 1
        
        if is_freq == "y":
            hpo_frequency_el = hpo_frequency * add_weight
        if is_freq == "n":
            hpo_frequency_el =  add_weight
        
        #logger.info(f"AFTER \t{one_hpo_valid.id}\t Freq : {hpo_frequency_el}")

        return hpo_frequency_el



    def run_sm_freq(self,element2,patient_id_list,combine,method,is_freq,vector_weight): # rajouter un vecteur ici pour les frequences 
        combine_method_rsl = 0

        hpo_frequency_el1 = hpo_frequency_el2 = 1
        # add poid frequence vecteur c'est pas le hpo frequency

        interaction_all = set()
        ## usually a loop here but the loop will be done on the snakefile

        minidf_2 = self.df_group2[self.df_group2[self.colname_2]==element2]
        hpo_el_2 = minidf_2['hpo_id'].drop_duplicates().tolist() 
        hpo_excluded = minidf_2[minidf_2['hpo_frequency'] == 0]['hpo_id'].drop_duplicates().tolist()

        for e1,element1 in enumerate(patient_id_list):
            if element2 == element1 : 
                combine_method_rsl = 0
            else:
                minidf_1 = self.df_group1[self.df_group1[self.colname_1]==element1]
                hpo_el_1 = minidf_1['hpo_id'].drop_duplicates().tolist() 

                ## test if the patients as hpo excluded if true no need to make sm the result will be 0
                is_match_excluded = set(hpo_excluded).intersection(hpo_el_1)
                if len(is_match_excluded) != 0:
                    ## the patient have at least one  hpo excluded from disease -> he don t have the disease
                    combine_method_rsl = 0
                    #print(f"{element2} - {element1} : excluded  ")

                else:
                    ## implement matrix 
                    score_matrix = np.zeros(shape=(len(hpo_el_2), len(hpo_el_1))) # row,col

                    for i,one_hpo_2 in enumerate(hpo_el_2):
                        try:  # try/except hpo term invalid
                            one_hpo_rd_term = Ontology.get_hpo_object(one_hpo_2)
                            hpo_frequency_el2 = self.set_freq_for_sm(one_hpo_rd_term,minidf_2,vector_weight,is_freq)

                            for j,one_hpo_1 in enumerate(hpo_el_1):
                                try :  # try/except hpo term invalid
                                    one_hpo_p_term = Ontology.get_hpo_object(one_hpo_1)
                                    finale_score = 0

                                    ## build matrix 
                                    ic_mica = one_hpo_rd_term.similarity_score(one_hpo_p_term, 'orpha', method)
                                    finale_score = ic_mica * hpo_frequency_el1 * hpo_frequency_el2 # patient have a frequency of 1 

                                    score_matrix[i, j] = finale_score

                                    #print(f"Score between RD : {element1} - Patient :{element2} :{one_hpo_rd_term.id}  and {one_hpo_p_term.id}: {score_matrix[i, j]} \n")   


                                except RuntimeError:
                                    #logger.info(f"Hpo term invalid : {one_hpo_2}")
                                    ic_mica = 0                       
                        except RuntimeError:
                            #logger.info(f"Hpo term invalid : {one_hpo_1}")
                            ic_mica = 0

                        # max for each row 
                        max_row = np.amax(score_matrix, axis=1)
                        # max for each col 
                        max_col = np.amax(score_matrix, axis=0)
                        if combine == "funSimAvg":
                            combine_method_rsl = ((sum(max_row) / len(max_row)) + (sum(max_col) / len(max_col))) / 2

                        if combine == "funSimMax":
                            combine_method_rsl =  max([sum(max_row) / len(max_row), sum(max_col) / len(max_col)])

                        if combine == "BMA": 
                            combine_method_rsl= (sum(max_row) + sum(max_col)) / (len(max_row) + len(max_col))
                        if combine == "BUMS":      
                            bums = self.iterative_bums(score_matrix)
                            combine_method_rsl = sum(bums.values())/ len(hpo_el_1)
                        if combine == "rsd":
                            # For patient → disease: for each patient‐HPO term (each column) take the best disease match
                            combine_method_rsl = sum(max_col) / len(hpo_el_1)
                        
                        #logger.info(f"{element2} - {element1} \t {combine}\t{combine_method_rsl}")
                        #logger.info(f"{element2} - {element1} \t {combine}\t Score {combine_method_rsl} \t max col : {max_col}\tm max row : {max_row}")

                        #logger.info(f"{element2} - {element1} \t {combine}\t{combine_method_rsl} \n{score_matrix}")

                
            ## build the result matrix here  put condition if here 
            #matrix_sm[e1, e2] = combine_method_rsl  #round(combine_method_rsl,2)
            interaction_all.add((element2,element1,combine_method_rsl))
        df_mp = pd.DataFrame(interaction_all,columns=['RDs','patients','score'])



        return df_mp




    def run_mm_freq(self,element2,patient_id_list,combine,method,is_freq,vector_weight): # rajouter un vecteur ici pour les frequences 
        combine_method_rsl = 0

        hpo_frequency_el1 = hpo_frequency_el2 = 1
        # add poid frequence vecteur c'est pas le hpo frequency

        interaction_all = set()
        ## usually a loop here but the loop will be done on the snakefile

        minidf_2 = self.df_group2[self.df_group2[self.colname_2]==element2]
        hpo_el_2 = minidf_2['hpo_id'].drop_duplicates().tolist() 
        hpo_excluded = minidf_2[minidf_2['hpo_frequency'] == 0]['hpo_id'].drop_duplicates().tolist()

        for e1,element1 in enumerate(patient_id_list):
            if element2 == element1 : 
                combine_method_rsl = 0
            else:
                minidf_1 = self.df_group1[self.df_group1[self.colname_1]==element1]
                hpo_el_1 = minidf_1['hpo_id'].drop_duplicates().tolist() 

                ## implement matrix 
                score_matrix = np.zeros(shape=(len(hpo_el_2), len(hpo_el_1))) # row,col

                for i,one_hpo_2 in enumerate(hpo_el_2):
                    try:  # try/except hpo term invalid
                        one_hpo_rd_term = Ontology.get_hpo_object(one_hpo_2)
                        hpo_frequency_el2 = self.set_freq_for_sm(one_hpo_rd_term,minidf_2,vector_weight,is_freq)

                        for j,one_hpo_1 in enumerate(hpo_el_1):
                            try :  # try/except hpo term invalid
                                one_hpo_p_term = Ontology.get_hpo_object(one_hpo_1)
                                finale_score = 0

                                ## build matrix 
                                ic_mica = one_hpo_rd_term.similarity_score(one_hpo_p_term, 'orpha', method)
                                finale_score = ic_mica * hpo_frequency_el1 * hpo_frequency_el2 # patient have a frequency of 1 

                                score_matrix[i, j] = finale_score

                                #print(f"Score between RD : {element1} - Patient :{element2} :{one_hpo_rd_term.id}  and {one_hpo_p_term.id}: {score_matrix[i, j]} \n")   


                            except RuntimeError:
                                #logger.info(f"Hpo term invalid : {one_hpo_2}")
                                ic_mica = 0                       
                    except RuntimeError:
                        #logger.info(f"Hpo term invalid : {one_hpo_1}")
                        ic_mica = 0

                    # max for each row 
                    max_row = np.amax(score_matrix, axis=1)
                    # max for each col 
                    max_col = np.amax(score_matrix, axis=0)
                    if combine == "funSimAvg":
                        combine_method_rsl = ((sum(max_row) / len(max_row)) + (sum(max_col) / len(max_col))) / 2

                    if combine == "funSimMax":
                        combine_method_rsl =  max([sum(max_row) / len(max_row), sum(max_col) / len(max_col)])

                    if combine == "BMA": 
                        combine_method_rsl= (sum(max_row) + sum(max_col)) / (len(max_row) + len(max_col))
                    if combine == "BUMS":      
                        bums = self.iterative_bums(score_matrix)
                        combine_method_rsl = sum(bums.values())/ len(hpo_el_1)
                    if combine == "rsd":
                        # For patient → disease: for each patient‐HPO term (each column) take the best disease match
                        combine_method_rsl = sum(max_col) / len(hpo_el_1)

                
            ## build the result matrix here  put condition if here 
            #matrix_sm[e1, e2] = combine_method_rsl  #round(combine_method_rsl,2)
            interaction_all.add((element2,element1,combine_method_rsl))
        df_mp = pd.DataFrame(interaction_all,columns=['RDs','patients','score'])



        return df_mp




    def export_sm(self,df,path_output):
        df.to_excel(path_output )


    def from_sm_make_cdf(self,df_sm):
        ## Filter the df patients
        df_patient_confirmed = self.df_group1[[self.colname_1,COL_DF_PATIENT_ORPHACODE]] 
        df_patient_confirmed.columns = ["patients","RDs"] 
        df_patient_confirmed = df_patient_confirmed.drop_duplicates()
        
        df_cdf = pd.merge(df_sm[["patients","RDs"]], df_patient_confirmed, how='inner', on=["RDs","patients"]).dropna()
        # print("Nb Patients {}\t Nb diseases : {} ".format(len(df_cdf['patients'].drop_duplicates().tolist()), len(df_cdf['RDs'].drop_duplicates().tolist())))
        return df_cdf

    def from_mm_make_cdf(self,df_sm):
        ## Filter the df patients
        df_rd = self.df_group1[[self.colname_1,'ORPHAcode']] 
        df_rd.columns = ["patients","RDs"] 
        df_rd = df_rd.drop_duplicates()
        
        df_cdf = pd.merge(df_sm[["patients","RDs"]], df_rd, how='inner', on=["RDs","patients"]).dropna()
        # print("Nb Patients {}\t Nb diseases : {} ".format(len(df_cdf['patients'].drop_duplicates().tolist()), len(df_cdf['RDs'].drop_duplicates().tolist())))
        return df_cdf

    def iterative_bums(self,score_array):
        result_bums = {}
        # print(f"Starting : \n{score_array}\n")
        ## Number of elements in the array are not egal to 0 
        while score_array.size > 0:
            max_in_array =  np.amax(score_array) # max for col
            # print(f"max_in_array :\n {max_in_array}")
            max_index = np.where(score_array ==max_in_array)
            # print(f"Max index :\n {max_index}")

            ## Store the result (index and value)
            result_bums[str(max_index[0][0]) + " - " +  str(max_index[1][0])] = max_in_array
            # print(f'Rslt BUMS in t instant \n{result_bums}')
            ## Remove section 
            score_array = np.delete(score_array, max_index[0], axis=0)  # Remove row
            # print(f"Row removed \n{score_array}")
            score_array = np.delete(score_array, max_index[1], axis=1)  # Remove column
            # print(f"col removed \n{score_array}")

        #print("BUMS process:\n", result_bums)
        return result_bums
