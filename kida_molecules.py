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

    name = ""
    cas = ""
    mass = ""
    charge = ""
    inchi = ""
    inchikey = ""

    if info is not None:
        for j,data_table in enumerate(data_tables):
            if data_table.empty == False:
                if j==0:
                    '''    
                    if data_table.iloc[5,0] == "Inchi":
                        inchi = data_table.iloc[5,1]
                    else:
                        inchi = "" 
                    '''
                    if data_table.iloc[6,0] == "InchiKey":
                        inchikey = data_table.iloc[6,1]
                    else:
                        inchikey = ""
                    if "CAS" in data_table.iloc[4,0]:
                        cas = data_table.iloc[4,1]
                    else:
                        cas = "" 
                    if "Charge" in data_table.iloc[3,0]:
                        charge = data_table.iloc[3,1]
                    else:
                        charge = ""
                    if "Mass" in data_table.iloc[2,0]:
                        mass = data_table.iloc[2,1]
                    else:
                        mass = ""     
                    if data_table.iloc[1,0] == "Name":
                        name = data_table.iloc[1,1]
                    else:
                        name = ""
                                                
    return(info, name, cas, mass, charge, inchikey)

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

def ent(info_tables):
    if info_tables is not None:
        ck = False
        for j,data_table in enumerate(info_tables):
            if data_table.empty == False:            
                if data_table.shape[1] == 6 and data_table.columns.values[1] == "T (K)":
                    ck = True
                    row_ent = data_table.shape[0]
                    ent_list = []
                    for k in range(row_ent):
                        t = data_table.iloc[k,1]
                        val = data_table.iloc[k,2]
                        ent_list.append([t,val])
        if ck == False:
            ent_list = None
    else:
        e0   =  ""
        e298 =  ""

    if ent_list is not None:
        if len(ent_list) > 1:
            e = ent_list[0][1].replace(" ","")
            t = ent_list[0][0].replace(" ","")
            if "0" in t:
                e0   =  e 
                e298 = ""
            else:
                e0   =  ""
                e298 = e 

            if len(e0) == 0:
                e = ent_list[1][1].replace(" ","")
                t = ent_list[1][0].replace(" ","")
                if "0" in t:
                    e0   =  e 
                else:
                    e0   =  ""

            if len(e298) == 0:
                e = ent_list[1][1].replace(" ","")
                t = ent_list[1][0].replace(" ","")
                if "0" in t:
                    e298   =  ""
                else:
                    e298   =  e 
        else: 
            e = ent_list[0][1].replace(" ","")
            t = ent_list[0][0].replace(" ","")
            if "0" in t:
                e0   =  e 
                e298 = ""
            else:
                e0   =  ""
                e298 = e 
    else:
        e0   =  ""
        e298 = ""                
    return(e0,e298)

def info_dataFormat(list_species):
    species = []
    formula = []
    Inchi = []
    mass = []
    name = []
    charge = []
    InchiKey = []
    cas = []
    enthalpy0 = []
    enthalpy298 = [] 

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
        Inchi.append(tmp_inchi)

        tmp_info = kida_info(ch_url)
        if tmp_info[0] == None:
            cas.append("")
            mass.append("")
            name.append("")
            charge.append("")
            InchiKey.append("")
            cas.append("")
        else:
            tmp_name = tmp_info[1]
            tmp_name = tmp_name.replace(" ","")
            name.append(tmp_name)

            tmp_cas = tmp_info[2]
            tmp_cas = tmp_cas.replace(" ","")
            cas.append(tmp_cas)
            
            tmp_mass = tmp_info[3]
            tmp_mass = tmp_mass.replace(" ","")
            tmp_mass = tmp_mass.replace("\n","")
            mass.append(tmp_mass)

            tmp_charge = tmp_info[4]
            tmp_charge = tmp_charge.replace(" ","")
            charge.append(tmp_charge)

            tmp_InchiKey = tmp_info[5]
            tmp_InchiKey = tmp_InchiKey.replace(" ","")
            InchiKey.append(tmp_InchiKey)

        tmp_ent = ent(tmp_info[0])
        tmp_ent0 = tmp_ent[0].replace(" ","")
        if "±" in tmp_ent0:
            k = tmp_ent0.find("±")
            tmp_ent0 = tmp_ent0[:k]
        tmp_ent298 = tmp_ent[1].replace(" ","")
        if "±" in tmp_ent298:
            k = tmp_ent298.find("±")
            tmp_ent298 = tmp_ent298[:k]
        enthalpy0.append(tmp_ent0)
        enthalpy298.append(tmp_ent298)

        #print(i, tmp_spec, tmp_form, tmp_inchi, tmp_InchiKey, tmp_name, tmp_cas, tmp_charge, tmp_mass, tmp_ent0,tmp_ent298)
    return(species, formula, name, cas, mass, charge, Inchi, InchiKey, enthalpy0, enthalpy298) 

with open("molecules_kida_info.csv", "w+") as output:
    list_species = kida_mol()
    
    if list_species is not None:
        info_spec = info_dataFormat(list_species)
        species = info_spec[0]
        formula = info_spec[1]
        name = info_spec[2]
        cas = info_spec[3]
        mass = info_spec[4]
        charge = info_spec[5]
        Inchi = info_spec[6]
        InchiKey = info_spec[7]
        enthalpy0 = info_spec[8]
        enthalpy298 = info_spec[9]  
    else:
        print("Error in List Species")
    data = []
    for i in range(list_species.shape[0]):
        data.append([species[i], formula[i], name[i], cas[i], mass[i], charge[i], Inchi[i], InchiKey[i], enthalpy0[i], enthalpy298[i]])
    df = pd.DataFrame(data, columns=["C_formula","S_formula", "Name", "CAS", "Mass", "Charge","Inchi","InchiKey","enthalpy0","enthalpy298"])
    #print(df.to_csv(sep="\t", index=False))
    output.write(df.to_csv(sep="\t", index=False))
