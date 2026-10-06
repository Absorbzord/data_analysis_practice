import numpy as np
import pandas as pd
# from numpy import linalg
# from numpy import genfromtxt

print("\nZadanie 1\n")
file_path = "Zadanie_1.csv"
zad_1 = pd.read_csv(file_path)

zad_1_clean = zad_1.iloc[:, 0].str.split(";", expand=True).apply(pd.to_numeric, errors="coerce")
zad_1_arr = zad_1_clean.to_numpy()

# 1a
cells_count = zad_1_arr.size
print(f"\nMacierz posiada {cells_count} komórek.\n")

# 1b
rows_count, cols_count = zad_1_arr.shape
print(f"\nMacierz posiada {rows_count} wierszy i {cols_count} kolumn.")

# 1c
mean = np.nanmean(zad_1_arr)
median = np.nanmedian(zad_1_arr)
variance = np.nanvar(zad_1_arr)

print(f"\nDla macierzy: \n Średnia: {mean}; \n Mediana: {median}; \n Wariancja: {variance} ")

# 1d
mask_zad_1 = np.ma.masked_invalid(zad_1_arr)
mask_mean = mask_zad_1.mean()
mask_median = np.ma.median(mask_zad_1)
mask_variance = mask_zad_1.var()

print(f"\nDla macierzy zamaskowanej: \n Średnia: {mask_mean}; \n Mediana: {mask_median}; \n Wariancja: {mask_variance} ")

# zad2
# a
print("\nZadanie 2\n 2a")
zad_2 = pd.read_csv("Zadanie_2.csv", header=None)

zad2_clean = zad_2.iloc[:, 0].str.split(";", expand=True).apply(pd.to_numeric, errors="coerce").to_numpy()

eigenvalue, eigenvectors = np.linalg.eig(zad2_clean)


print(f"\nwartości własne: \n{eigenvalue}\nwektory własne: \n{eigenvectors}\n")

# b
inverse_matrix = np.linalg.inv(zad2_clean)
print(f"2b\n macierz odwrotna: \n{inverse_matrix}")


# # zad4

zadanie_4 = pd.read_csv('Zadanie_4.csv')


zad4_clean = zadanie_4.iloc[:, 0].str.split(';', expand=True)

zad4_clean.columns = ['DateTime', 'DoctorID', 'Type', 'City', '', '', '', '']

zad4_clean = zad4_clean[['DateTime', 'DoctorID']]  # Keep relevant columns



zad4_clean['DateTime'] = pd.to_datetime(zad4_clean['DateTime'], format='%d.%m.%Y %H:%M')

zad4_clean['Available'] = 1  # Mark all entries as available



intervals = (zad4_clean['DateTime'].diff() != pd.Timedelta(minutes=1)).cumsum()

zad4_clean['IntervalGroup'] = intervals


availability = zad4_clean.groupby('IntervalGroup').agg(

    Start=('DateTime', 'first'),

    End=('DateTime', 'last')

).reset_index(drop=True)


output_path = 'dostepnosc_lekarza.csv'

availability.to_csv(output_path, index=False)



availability, output_path