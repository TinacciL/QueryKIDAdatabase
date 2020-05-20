from kida_query_lib import kida_info, kida_mol, info_dataFormat
import requests
import pandas as pd

with open("molecules_kida.csv", "w+") as output:
	list_species = kida_mol()
	if list_species is not None:
		#tmp = ['CN','CO2','C2H4+']
		#list_species = list_species[list_species['Formula'].isin(tmp)]
		info_spec = info_dataFormat(list_species)
		species = info_spec[0]
		formula = info_spec[1]
		cas = info_spec[2]
		Inchi = info_spec[3]
		enthalpy = info_spec[4]
		temp = info_spec[5]
		be = info_spec[6]
	else:
		print("Error in List Species")
	data = []
	for i in range(len(formula)):
		if type(be[i]) == str:
			de_2 = 'NoData'
			de_3 = 'NoData'
			de_4 = 'NoData'
			de_5 = 'NoData'
			de_6 = 'NoData'
			de_7 = 'NoData'
			de_8 = 'NoData'
			de_9 = 'NoData'
			de_10 = 'NoData'
			de_11 = 'NoData'
			data.append([species[i], formula[i], cas[i], Inchi[i], enthalpy[i], temp[i], de_2, de_3, de_4, de_5, de_6, de_7, de_8, de_9, de_10, de_11])
		else:
			for j,item in enumerate(be[i]):
				de_2 = item[0]
				de_3 = item[1]
				de_4 = item[2]
				de_5 = item[3]
				de_6 = item[4]
				de_7 = item[5]
				de_8 = item[6]
				de_9 = item[7]
				de_10 = item[8]
				de_11 = item[9]
				data.append([species[i], formula[i], cas[i], Inchi[i], enthalpy[i], temp[i], de_2, de_3, de_4, de_5, de_6, de_7, de_8, de_9, de_10, de_11])
	df = pd.DataFrame(data, columns=["Species","Formula","CAS","Inchi","Enthalpy","T(K)_Enthalpy","E_mean", "E_min", "E_max", "Pre-exponential_factor", "Order_factor", "Method", "Origin", "Reference", "Type_of_surface",	"Description"])
	output.write(df.to_csv(sep="\t", index=False))