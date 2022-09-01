from pymed import PubMed
import pandas as pd 
import matplotlib.pyplot as plt
from scipy.stats import shapiro
from cliffs_delta import cliffs_delta
from scipy.stats import   f_oneway, mannwhitneyu, kruskal, pearsonr , kendalltau, spearmanr
import numpy as np
import pylab as py
import scipy.stats as stats

print('###################### Question 1 #########################################')

pubmed = PubMed(tool="Assignment2", email="sneha198919@gmail.com")
query = '(((Covid-19[Title]) AND (Vaccine[Title])) OR ((Covid-19[Title]) AND (mRNA[Title]))OR ((Covid-19[Title])AND (Booster[Title])) OR ((Vaccine[Title])AND (Booster[Title])) OR ((Vaccine[Title])AND (mRNA[Title])) OR ((mRNA[Title])AND (Booster[Title]))) AND (("2019/01/01"[Date - Publication] : "3000"[Date - Publication]))'
results = pubmed.query(query, max_results=10000)
titles = []
publications = []

# Extract and format information from the article
for article in results:
    article_id = article.pubmed_id
    title = article.title
    titles.append(title)
    publication_date = article.publication_date
    publications.append(publication_date)
    
dataset = pd.DataFrame(list(zip(titles, publications))
                        ,columns =['Title' , 'publication_date'])
dataset['year'] = pd.DatetimeIndex(dataset['publication_date']).year
dataset['month'] = pd.DatetimeIndex(dataset['publication_date']).month
dataset.to_csv('Covid_Vaccine.csv', index = False)

data = pd.read_csv('Covid_Vaccine.csv')

data["Title"] = data["Title"].str.lower().str.replace('\[[^]]*{}\]','')
yearlst = [2019, 2020, 2021,2022] 
monthlst = [1,2,3,4,5,6,7,8,9,10,11,12] 
cntvaccine = []
cntcovid = []
cntmrna = []
cntbooster = []
yr_vaccine = []
year_cnt_vaccine = []
yr_covid = []
year_cnt_covid = []
yr_mrna = []
year_cnt_mrna = []
yr_booster = []
year_cnt_booster = []

for year in yearlst:
    yeardata = data["year"] == year
    data3 = data.loc[yeardata].reset_index(drop=True)

    for mnt in monthlst:
        mondata = data3["month"] == mnt
        data3 = data3.loc[mondata].reset_index(drop=True)
        datafin = data3["Title"]
        data3 = data.loc[yeardata].reset_index(drop=True)
        covid = []
        vaccine = []
        booster = []
        mrna = []
        for i in range (0,len(datafin)):
            covid.append(str(datafin[i]).count("covid-19")) #line level apend in list [1,2,3]
            vaccine.append(str(datafin[i]).count("vaccine"))
            mrna.append(str(datafin[i]).count("mrna"))
            booster.append(str(datafin[i]).count("booster"))
        s_c = sum(covid) # sum of all line level counts [6]
        s_v = sum(vaccine)
        s_m = sum(mrna)
        s_b = sum(booster)
        cntvaccine.append(s_v) #each append of 1 month 
        cntcovid.append(s_c)
        cntmrna.append(s_m)
        cntbooster.append(s_b)

splits = np.array_split(cntvaccine, 4)
for array in splits:
    yr_vaccine = sum(list(array))
    year_cnt_vaccine.append(yr_vaccine)
print("Yearwise count for 'Vaccine' keyword is :{} for 2019,2020,2021,2022 respectively".format(year_cnt_vaccine))

splits = np.array_split(cntcovid, 4)
for array in splits:
    yr_covid = sum(list(array))
    year_cnt_covid.append(yr_covid)
print("Yearwise count for 'Covid-19' keyword is :{} for 2019,2020,2021,2022 respectively".format(year_cnt_covid))

splits = np.array_split(cntbooster, 4)
for array in splits:
    yr_booster = sum(list(array))
    year_cnt_booster.append(yr_booster)
print("Yearwise count for 'Booster' keyword is :{} for 2019,2020,2021,2022 respectively".format(year_cnt_booster))

splits = np.array_split(cntmrna, 4)
for array in splits:
    yr_mrna = sum(list(array))
    year_cnt_mrna.append(yr_mrna)
print("Yearwise count for 'mRNA' keyword is :{} for 2019,2020,2021,2022 respectively".format(year_cnt_mrna))


cntcovid = cntcovid[0:38]
cntvaccine = cntvaccine[0:38]
cntmrna = cntmrna[0:38]
cntbooster = cntbooster[0:38]

print("Total counts for 'Vaccine' monthwise is {}" .format(cntvaccine))  
print("Total counts for 'Covid-19' monthwise is {}" .format(cntcovid))
print("Total counts for 'Booster' monthwise is {}" .format(cntbooster))  
print("Total counts for 'mRNA' monthwise is {}" .format(cntmrna))



## Checking for Gaussian Distribution by Shapiro test for Covid19
stat, p = shapiro(cntcovid)
print('stat= {}, p= {}'.format(stat, p))
if p > 0.05:
	print('Sample looks Gaussian Distributed for "Covid-19" keyword by shapiro test ')
else:
	print('Sample does not look Gaussian Distributed for "Covid-19" keyword by shapiro test')
arr = np.array(cntcovid)    

# Adding Probability plot for visual analysis of the distribution for Covid19
stats.probplot(arr, dist="norm", plot = plt)
plt.title('Probability Plot for "Covid-19" for 2019-2022 data')
py.show()  

# Showing Density plot for Covid19
df_cntcovid = pd.DataFrame(cntcovid,columns =['monthwisecount'])
df_cntcovid.monthwisecount.plot.density(color='green')
plt.title('Density Plot for "Covid-19" for 2019-2022 data')
plt.xlabel("Keyword counts")
plt.show()

## Checking for Gaussian Distribution by Shapiro test for Vaccine
stat, p = shapiro(cntvaccine)
print('stat= {}, p= {}'.format(stat, p))
if p > 0.05:
	print('Sample looks Gaussian Distributed for "Vaccine" keyword')
else:
	print('Sample does not look Gaussian Distributed for "Vaccine" keyword')
arr = np.array(cntvaccine)  

# Adding Probability plot for visual analysis of the distribution for Vaccine
stats.probplot(arr, dist="norm", plot = plt) 
plt.title('Probability Plot for "Vaccine" for 2019-2022 data') 
py.show()  

# Showing Density plot for Vaccine
df_cntvaccine = pd.DataFrame(cntvaccine,columns =['monthwisecount'])
df_cntvaccine.monthwisecount.plot.density(color='green')
plt.title('Density Plot for "Vaccine" for 2019-2022 data')
plt.xlabel("Keyword counts")
plt.show()


## Checking for Gaussian Distribution by Shapiro test for Booster
stat, p = shapiro(cntbooster)
print('stat= {}, p= {}'.format(stat, p))
if p > 0.05:
	print('Sample looks Gaussian Distributed for "Booster" keyword by shapiro test ')
else:
	print('Sample does not look Gaussian Distributed for "Booster" keyword by shapiro test')
arr = np.array(cntbooster)    

# Adding Probability plot for visual analysis of the distribution for Booster
stats.probplot(arr, dist="norm", plot = plt)
plt.title('Probability Plot for "Booster" for 2019-2022 data') 
py.show()  

# Showing Density plot for Booster
df_cntbooster = pd.DataFrame(cntbooster,columns =['monthwisecount'])
df_cntbooster.monthwisecount.plot.density(color='green')
plt.title('Density Plot for "Booster" for 2019-2022 data')
plt.xlabel("Keyword counts")
plt.show()

## Checking for Gaussian Distribution by Shapiro test for mRNA
stat, p = shapiro(cntmrna)
print('stat= {}, p= {}'.format(stat, p))
if p > 0.05:
	print('Sample looks Gaussian Distributed for "mRNA" keyword by shapiro test ')
else:
	print('Sample does not look Gaussian Distributed for "mRNA" keyword by shapiro test')
arr = np.array(cntmrna)    

# Adding Probability plot for visual analysis of the distribution for mRNA
stats.probplot(arr, dist="norm", plot = plt)
plt.title('Probability Plot for "mRNA" for 2019-2022 data') 
py.show()  

# Showing Density plot for mRNA
df_cntmrna = pd.DataFrame(cntmrna,columns =['monthwisecount'])
df_cntmrna.monthwisecount.plot.density(color='green')
plt.title('Density Plot for "mRNA" for 2019-2022 data')
plt.xlabel("Keyword counts")
plt.show()

print('###################### Question 2 #########################################')
pubmed = PubMed(tool="Assignment2", email="sneha198919@gmail.com")
query = '((Obesity[Title]) OR (Cancer[Title])) AND (("2019/01/01"[Date - Publication] : "2021/12/31"[Date - Publication]))'
results = pubmed.query(query, max_results=260000)
titles = []
publications = []

# Extract and format information from the article
for article in results:
    article_id = article.pubmed_id
    title = article.title
    titles.append(title)
    publication_date = article.publication_date
    publications.append(publication_date)
    
dataset = pd.DataFrame(list(zip(titles, publications))
                        ,columns =['Title' , 'publication_date'])
dataset['year'] = pd.DatetimeIndex(dataset['publication_date']).year
dataset['month'] = pd.DatetimeIndex(dataset['publication_date']).month

# print (dataset)
dataset.to_csv('Obcancer.csv', index = False)

data = pd.read_csv('Obcancer.csv')
data["Title"] = data["Title"].str.lower().str.replace('\[[^]]*{}\]','')
yearlst = [2019, 2020, 2021] 
monthlst = [1,2,3,4,5,6,7,8,9,10,11,12] 
cntCancer = []
cntObesity = []
yr_Cancer = []
year_cnt_Cancer = []
yr_Obesity = []
year_cnt_Obesity = []
for year in yearlst:
    yeardata = data["year"] == year
    data3 = data.loc[yeardata].reset_index(drop=True)
    for mnt in monthlst:
        mondata = data3["month"] == mnt
        data3 = data3.loc[mondata].reset_index(drop=True)
        datafin = data3["Title"]
        data3 = data.loc[yeardata].reset_index(drop=True)
        Obesity = []
        Cancer = []
        for i in range (0,len(datafin)):
            Obesity.append(str(datafin[i]).count("obesity")) #line level apend in list [1,2,3]
            Cancer.append(str(datafin[i]).count("cancer"))
            
        s_c = sum(Obesity) # sum of all line level counts [6]
        s_v = sum(Cancer)
        cntCancer.append(s_v) #each append of 1 month 
        cntObesity.append(s_c)

splits = np.array_split(cntCancer, 3)
for array in splits:
    yr_Cancer = sum(list(array))
    year_cnt_Cancer.append(yr_Cancer)
print("Yearwise count for Cancer keyword is :{} for 2019,2020,2021 respectively".format(year_cnt_Cancer))

splits = np.array_split(cntObesity, 3)
for array in splits:
    yr_Obesity = sum(list(array))
    year_cnt_Obesity.append(yr_Obesity)
print("Yearwise count for Obesity keyword is :{} for 2019,2020,2021 respectively".format(year_cnt_Obesity))
    
print("Total counts for Cancer monthwise is {}" .format(cntCancer))  
print("Total counts for Obesity monthwise is {}" .format(cntObesity))

# Analysis of Variance Test
cancer1 = cntCancer[0:12]
cancer2 = cntCancer[12:24]
cancer3 = cntCancer[24:36]

Obesity1 = cntObesity[0:12]
Obesity2 = cntObesity[12:24]
Obesity3 = cntObesity[24:36]

print('###################### Question 2 (a) #########################################')

print('############### ANOVA Parametric Test ##################')
stat, p = f_oneway(cancer1,Obesity1)
print('stat= {}, p= {}'.format(stat, p))
if p > 0.05:
 	print('Possibly there is the same distribution for Cancer and Obesity for 2019')
else:
 	print('Possibly there are different distributions for Cancer and Obesity for 2019')

stat, p = f_oneway(cancer2,Obesity2)
print('stat= {}, p= {}'.format(stat, p))
if p > 0.05:
 	print('Possibly there is the same distribution for Cancer and Obesity for 2020')
else:
 	print('Possibly there are different distributions for Cancer and Obesity for 2020')
     
stat, p = f_oneway(cancer3,Obesity3)
print('stat= {}, p= {}'.format(stat, p))
if p > 0.05:
 	print('Possibly there is the same distribution for Cancer and Obesity for 2021')
else:
 	print('Possibly there are different distributions for Cancer and Obesity for 2021')
     
print('###############  Mann-Whitney U Test(Non-Parametric) ##################')     
stat, p = mannwhitneyu(cancer1,Obesity1)
print('stat= {}, p= {}'.format(stat, p))
if p > 0.05:
 	print('Possibly there is the same distribution for Cancer and Obesity for 2019')
else:
 	print('Possibly there are different distributions for Cancer and Obesity for 2019')
     
stat, p = mannwhitneyu(cancer2,Obesity2)
print('stat= {}, p= {}'.format(stat, p))
if p > 0.05:
 	print('Possibly there is the same distribution for Cancer and Obesity for 2020')
else:
 	print('Possibly there are different distributions for Cancer and Obesity for 2020')
     
stat, p = mannwhitneyu(cancer3,Obesity3)
print('stat= {}, p= {}'.format(stat, p))
if p > 0.05:
 	print('Possibly there is the same distribution for Cancer and Obesity for 2021')
else:
 	print('Possibly there are different distributions for Cancer and Obesity for 2021')
     
print('############### Kruskal Wallis Test(Non-Parametric) ##################')

stat, p = kruskal(cancer1,Obesity1)
print('stat= {}, p= {}'.format(stat, p))
if p > 0.05:
 	print('Possibly there is the same distribution for Cancer and Obesity for 2019')
else:
 	print('Possibly there are different distributions for Cancer and Obesity for 2019')

stat, p = kruskal(cancer2,Obesity2)
print('stat= {}, p= {}'.format(stat, p))
if p > 0.05:
 	print('Possibly there is the same distribution for Cancer and Obesity for 2020')
else:
 	print('Possibly there are different distributions for Cancer and Obesity for 2020')
     
stat, p = kruskal(cancer3,Obesity3)
print('stat= {}, p= {}'.format(stat, p))
if p > 0.05:
 	print('Possibly there is the same distribution for Cancer and Obesity for 2021')
else:
 	print('Possibly there are different distributions for Cancer and Obesity for 2021')
     
print('###################### Question 2 (b) #########################################')

d1, res1 = cliffs_delta(cancer1, Obesity1)
print("The value for effect size test of Cliff D is {} and the magnitude of difference between Cancer and Obesity in 2019 is {}".format(d1,res1))

d2, res2 = cliffs_delta(cancer2, Obesity2)
print("The value for effect size test of Cliff D is {} and the magnitude of difference between Cancer and Obesity in 2020 is {}".format(d2,res2))

d3, res3 = cliffs_delta(cancer3, Obesity3)
print("The value for effect size test of Cliff D is {} and the magnitude of difference between Cancer and Obesity in 2021 is {}".format(d3,res3))


print('###################### Question 3 #########################################')

print('############### Pearson’s Correlation Coefficient ##################')
stat, p = pearsonr(cntCancer, cntObesity)
print('stat= {}, p= {}'.format(stat, p))
if p > 0.05:
 	print('Cancer and Obesity may be not related')
else:
 	print('Cancer and Obesity may be related')
    
    
print('############### Spearman\'s Rank Correlation Test ##################')
stat, p = spearmanr(cntCancer, cntObesity)
print('stat= {}, p= {}'.format(stat, p))
if p > 0.05:
 	print('Cancer and Obesity may be not related')
else:
 	print('Cancer and Obesity may be related')
    
    
print('############### Kendalltau Correlation Test ##################')
stat, p = kendalltau(cntCancer, cntObesity)
print('stat= {}, p= {}'.format(stat, p))
if p > 0.05:
 	print('Cancer and Obesity may be not related')
else:
 	print('Cancer and Obesity may be related')