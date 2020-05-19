from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

def kida_info(url_mol):
    url =  requests.get("http://kida.astrophy.u-bordeaux.fr" + url_mol).text
    soup = BeautifulSoup(url,features="html.parser")
    tables = soup.find_all("table", {"class":"table table-striped table-hover table-responsive"})
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
        for j,data_table in enumerate(data_tables):
            if data_table.empty == False:
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
        if ck == False:
            ent = None                                        
    return(info,ent,cas)

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
    return(species, formula, cas, Inchi, enthalpy, temp) 

with open("molecules_kida_enthalpy.csv", "w+") as output:
    list_species = kida_mol()
    if list_species is not None:
        info_spec = info_dataFormat(list_species)
        species = info_spec[0]
        formula = info_spec[1]
        cas = info_spec[2]
        Inchi = info_spec[3]
        enthalpy = info_spec[4]
        temp = info_spec[5]   
    else:
        print("Error in List Species")
    data = []
    for i in range(len(formula)):
        data.append([species[i], formula[i], cas[i], Inchi[i], enthalpy[i], temp[i]])
    df = pd.DataFrame(data, columns=["Species","Formula","CAS","Inchi","Enthalpy","T(K)"])
    #print(df.to_csv(sep="\t", index=False))
    output.write(df.to_csv(sep="\t", index=False))

with open("formula_kida.csv", "w+") as output:
    fr  = pd.DataFrame(['Formula'])
    fr['formula'] = df['Formula']

    print(fr)

    exc = ["***","GRAIN0","GRAIN-","GRAIN+","XH","e-","e","CR","CRP","Photon"]
