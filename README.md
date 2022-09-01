# Anova-Mann-Whitney-U-Test-and-Kruskal-Wallis

Use the Pubmed dataset and download four years of data (2019, 2020,2021, 2022), that include the following keywords. Covid-19, Vaccine, mRNA, Booster in either the “title” or “abstract”. You can download the Pubmed data directly or use python/R libraries such as https://pypi.org/ project/pymed/ or https://cran.r-project.org/web/packages/easyPubMed 
For each of these keywords, check whether it has a Gaussian distribution in the last four years. You should count the appearance of the keyword per year. e.g. “Covid-19”, “2020”, “320” Then, plot their distributions based on the number of the year (use density plot). It means you should download the data for all years and then compare their frequency separately.

I used Title with a combination of 2 words in 6 pairs and researched for the keywords in the pubmed data using pymed for years 2019,2020,2021,2022. 
Checked if the sample look gausian using shapiro test

Compared the following two categories: “Obesity”, “Cancer” on a year basis (2019, 2020, 2021). 
a. With three statistics tests, one parametric(ANOVA), two non-parametric tests(Kruskal Wallis and Mann Whitney) and report results. 
b. Used the effect size test(Cliff D), to quantify the magnitude of differences.

Used three correlation coefficient tests (Pearson, Spearman, KendallTau) and report whether the following two keywords have correlations: “Obesity”, “Cancer”.
