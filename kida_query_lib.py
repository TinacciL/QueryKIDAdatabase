from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

def kida_info(url_mol):
    url =  requests.get("http://kida.astrophy.u-bordeaux.fr" + url_mol).text
    soup = BeautifulSoup(url,features="html.parser")
    tables = soup.find_all("table")#, {"class":"table table-striped table-hover table-responsive"}
    if tables is not None:
        data_tables = []
        for table in tables:    
            table_rows = table.find_all('tr')
            l = []
            for j,tr in enumerate(table_rows):
                if j==0:
                    cl_name = []    
                    th = tr.find_all('th')
                    cl_name = [tr.text for tr in th]
                else:
                    td = tr.find_all('td')
                    row = [tr.text for tr in td]
                    l.append(row)
            if len(cl_name) != 0:
                data_tables.append(pd.DataFrame(l, columns=cl_name))
            else:
                 data_tables.append(pd.DataFrame(l))
        info = data_tables
    else:
        info = None    
    if info is not None:
        ck = False
        ck_de = False
        for j,data_table in enumerate(data_tables):
            if data_table.empty == False:
                #with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                #    display(data_table)
                if j==0:
                    '''
                    if data_table.iloc[0,0] == "Stoichiometric Formula":
                        form = data_table.iloc[0,1]
                    else:
                        form = None  
                    if data_table.iloc[5,0] == "Inchi":
                        inchi = data_table.iloc[5,1]
                    else:
                        inchi = None
                    '''
                    if "CAS" in data_table.iloc[4,0]:
                        cas = data_table.iloc[4,1]
                    else:
                        cas = None            
                if data_table.shape[1] == 6 and data_table.columns.values[1] == "T (K)":
                    ck = True
                    row_ent = data_table.shape[0]
                    ent = []
                    for k in range(row_ent):
                        t = data_table.iloc[k,1]
                        val = data_table.iloc[k,2]
                        ent.append([t,val])
                if data_table.shape[1] == 11 and data_table.columns.values[6] == "Method":
                    ck_de = True
                    row_de = data_table.shape[0]
                    de = []
                    for k in range(row_de):
                        #de_1 = data_table.iloc[k,0].replace(" ","").replace("\n","")
                        de_2 = data_table.iloc[k,1].replace(" ","").replace("\n","")
                        de_3 = data_table.iloc[k,2].replace(" ","").replace("\n","")
                        de_4 = data_table.iloc[k,3].replace(" ","").replace("\n","")
                        de_5 = data_table.iloc[k,4].replace(" ","").replace("\n","")
                        de_6 = data_table.iloc[k,5].replace(" ","").replace("\n","")
                        de_7 = data_table.iloc[k,6].replace(" ","").replace("\n","")
                        de_8 = data_table.iloc[k,7].replace(" ","").replace("\n","")
                        de_9 = data_table.iloc[k,8].replace(" ","").replace("\n","")
                        de_10 = data_table.iloc[k,9].replace(" ","").replace("\n","")
                        de_11 = data_table.iloc[k,10].replace("\n","")
                        de.append([de_2,de_3,de_4,de_5,de_6,de_7,de_8,de_9,de_10,de_11])
        if ck == False:
            ent = None
        if ck_de == False:
            de = None                                        
    return(info,ent,cas,de)

def kida_mol():
    url =  requests.get("http://kida.astrophy.u-bordeaux.fr/species.html").text
    soup = BeautifulSoup(url,features="html.parser")
    table = soup.find("table", {"class":"table table-hover table-striped"})
    if table is not None:
        table_rows = table.find_all('tr')
        l =[]
        for j,tr in enumerate(table_rows):
            if j==0:
                cl_name = []    
                th = tr.find_all('th')
                cl_name.append("Href")
                cl_name = cl_name + [tr.text for tr in th]
            else:   
                td = tr.find_all('td')
                row = []
                h = td[0].a
                row.append(h.get('href'))
                tdn = td[:-1]
                row = row + [tr.text for tr in tdn]
                h = td[-1].a
                row.append(h.get('href'))
                l.append(row)
        data = pd.DataFrame(l, columns=cl_name)
        return_value = data
    else:
        return_value = None    
    return return_value                

def ent_chose(ent_list):
    if len(ent_list) > 1:
        tmp_e = []
        tmp_t = []
        for k,item in enumerate(ent_list):
            tmp_e.append(ent_list[k][1].replace(" ",""))
            tmp_t.append(ent_list[k][0].replace(" ",""))
        tmp_max = max(tmp_t)
        tmp_ind = tmp_t.index(tmp_max)
        e = tmp_e[tmp_ind]
        t = tmp_t[tmp_ind]
    else: 
        e = ent_list[0][1].replace(" ","")
        t = ent_list[0][0].replace(" ","")    
    return(e,t)

def info_dataFormat(list_species):
    species = []
    formula = []
    Inchi = []
    enthalpy = []
    temp = []
    cas = []
    be = []
    for i in range(list_species.shape[0]):
        ch_url = list_species.iloc[i,0]
        tmp_spec = list_species.iloc[i,1]
        tmp_spec = tmp_spec.replace("\n","")
        tmp_spec = tmp_spec.replace(" ","")
        species.append(tmp_spec)
        tmp_form = list_species.iloc[i,2]
        tmp_form = tmp_form.replace(" ","")
        formula.append(tmp_form)
        tmp_inchi = list_species.iloc[i,3].replace(" ","")
        if tmp_inchi == "":
            tmp_inchi = "NoData"  
        Inchi.append(tmp_inchi)
        ch_ent = kida_info(ch_url)
        if ch_ent[0] == None or ch_ent[2] == None:
            cas.append("NoData")
        else:
            tmp_cas = ch_ent[2]
            tmp_cas = tmp_cas.replace(" ","")
            if tmp_cas == "":
                tmp_cas = "NoData"
            cas.append(tmp_cas)
        if ch_ent[0] == None or ch_ent[1] == None:
            enthalpy.append("NoData")
            temp.append("NoData")
        else:
            tmp = ent_chose(ch_ent[1])
            e = tmp[0]
            t = tmp[1]
            enthalpy.append(e)
            temp.append(t)
        if ch_ent[0] == None or ch_ent[3] == None:
            be.append("NoData")
        else:
            be.append(ch_ent[3])
    return(species, formula, cas, Inchi, enthalpy, temp, be)