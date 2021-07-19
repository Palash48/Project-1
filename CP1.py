#!/usr/bin/env python
# coding: utf-8

# ## The Play Store apps data has enormous potential to drive app-making businesses to success. Actionable insights can be drawn for developers to work on and capture the Android market. 
# ## Each app (row) has values for catergory, rating, size, and more. Another dataset contains customer reviews of the android apps. 
# ## Explore and analyze the data to discover key factors responsible for app engagement and success.

# In[520]:


import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

os.chdir(r"C:\Users\asus\Desktop\Almabetter\datasets\capstone projects")


# In[521]:


df1 = pd.read_csv("Play Store Data.csv")
df2 = pd.read_csv("User Reviews.csv")


# In[522]:


df1.head()


# In[523]:


df2.head()


# In[524]:


df1[["date","year"]] = df1["Last Updated"].str.split(",",expand=True)
df1.drop("Last Updated", axis=1, inplace=True)


# In[525]:


df1.info()


# In[526]:


df2.info()


# # Data Cleaning

# In[527]:


# Data type of installs column is string and we have to convert this string data type into int and removing unwanted strings(+,)

# here rstrip function is used to remove the right most string('+') from the string

df1["Installs"] = df1["Installs"].map(lambda x: x.rstrip("+"))

# here split method is used to remove "," between the numbers and then join method is joining the splitted string.

df1["Installs"] = df1["Installs"].map(lambda x: ''.join(x.split(",")))


# In[528]:


df1["Size"] = df1["Size"].map(lambda x: x.rstrip("M"))


df1["Size"] = df1["Size"].map(lambda x: str(round((float(x.rstrip("k"))/1024),2)) if x[-1] == "k" else x)


# In[529]:


df1["Price"] = df1["Price"].map(lambda x: x.lstrip("$") if x.startswith("$") else x)


# In[530]:


df1.isna().sum()


# In[531]:


df2.isna().sum()


# In[532]:


df1["Rating"].fillna(df1["Rating"].mean(), inplace = True)


# In[533]:


df1.dropna(axis=0,inplace=True)

df1 = df1.drop(df1[df1["Size"] =="Varies with device"].index,axis=0)

df1.reset_index(drop=True, inplace=True)


# In[534]:


df2[df2["Translated_Review"].isna()].head(100)


# * ### It is assumed that if there is reviews then there is no sentimental observations also so, droping out these null values will be a good option. 

# In[535]:


df2.dropna(axis=0,inplace=True)
df2.reset_index(drop=True, inplace=True)


# In[536]:


df2.head()


# # Changing the Data Types of columns

# In[537]:


df1["Reviews"] = df1["Reviews"].apply(lambda x: x).astype(int)
df1["Size"] = df1["Size"].apply(lambda x: float(x) if x != "Varies with device" else str(x))
df1["Installs"] = df1["Installs"].apply(lambda x: x).astype(int)
df1["Price"] = df1["Price"].apply(lambda x: x).astype(float)
df1["year"] = df1["year"].apply(lambda x: x).astype(int)


# In[538]:


# Converting number of installs into percentage.

count_of_values = df1["Installs"].value_counts()
total_count = count_of_values.sum()
percent_of_each_values = round(count_of_values/total_count,2)*100
print(percent_of_each_values)


# In[539]:


def calculate_percentage(dataframe: pd.DataFrame):
    column_names = list(dataframe.columns)
    new_dataframe = dataframe.copy()
    total_values = {}
    valid_values_count = {}
    for index, each_row in new_dataframe.iterrows():
        total_values[index] = 0
        valid_values_count[index] = 0
        for each_column in column_names:
            if (not np.isnan(each_row[each_column])) and (each_row[each_column] > 0.0):
                total_values[index] = total_values[index] + each_row[each_column]
                valid_values_count[index] = valid_values_count[index] + 1

    for index, each_row in new_dataframe.iterrows():
        for target_column in column_names:
            if np.isnan(each_row[target_column]) or (each_row[target_column] == 0.0):
                each_row[target_column] = 0
            else:
                each_row[target_column] = each_row[target_column] / total_values[index] if total_values[index] > 0 else 0
            each_row[target_column] = each_row[target_column] * 100

    return new_dataframe


# # Assuming apps having ratings 1 to 2.5 having negative reviews

# In[540]:


ratings = (df1.Rating >= 0) & (df1.Rating < 2.5)
col_df1 = ['App', 'Rating', 'Reviews']
rating_df = df1[ratings][col_df1]
rating_df


# In[541]:


col_df2 = ['App', 'Translated_Review', 'Sentiment']
df2[col_df2]


# In[542]:


reviews_df = rating_df.merge(df2[col_df2], on='App')
reviews_df


# * ### from here we can assume that for low rating apps people didn't any reviews 

# # Assuming apps having ratings 2.5 to 3.5 having neutral reviews

# In[543]:


ratings = (df1.Rating >= 2.5) & (df1.Rating < 3.5)
col_df1 = ['App', 'Rating', 'Reviews']
rating_df = df1[ratings][col_df1]
rating_df


# In[544]:


col_df2 = ['App', 'Translated_Review', 'Sentiment']
df2[col_df2]


# In[545]:


reviews_df = rating_df.merge(df2[col_df2], on='App')
reviews_df_pivot = reviews_df.pivot_table('Rating',columns='Sentiment', index='App', aggfunc='count')
col = ['Positive', 'Neutral', 'Negative']
reviews_df_pivot = reviews_df_pivot[col]
reviews_df_pivot = calculate_percentage(reviews_df_pivot)
reviews_df_pivot = reviews_df_pivot.sort_values(by=['Neutral', 'Positive', 'Negative'], ascending=False)
zero_counts_filter = (reviews_df_pivot.Positive != 0.0) & (reviews_df_pivot.Neutral != 0.0) & (reviews_df_pivot.Negative != 0.0)
reviews_df_pivot = reviews_df_pivot[zero_counts_filter]
reviews_df_pivot


# In[546]:


plt.rcParams['figure.figsize'] = [20.0, 15.0]
reviews_df_pivot.plot(kind='barh', stacked=True)
plt.savefig('apps having ratings 2.5 to 3.5.jpg')
plt.show()


# In[547]:


print(f'{len(reviews_df_pivot)} Apps with rating between 2.5 and 3.5, many without reviews')
print(f'Positive sentiments: {round(reviews_df_pivot["Positive"].mean(), 3)}%')
print(f'Neutral sentiments: {round(reviews_df_pivot["Neutral"].mean(), 3)}%')
print(f'Negative sentiments: {round(reviews_df_pivot["Negative"].mean(), 3)}%')


# * ### From above analysis we can see that out of 603 apps only 15 apps are there whose reviews are mentioned and our hypothesis is not true because more than neutral reviews there are postive and negative review almost 80%. It is may be because reviews are not translated properly and less number of apps are there which reviews are there it may be possible if we have more apps reviews our hypothesis can be satisfied

# # Assuming apps having ratings 3.5 to 5 having postive reviews

# In[548]:


ratings = (df1.Rating >= 3.5) & (df1.Rating < 5)
col_df1 = ['App', 'Rating', 'Reviews']
rating_df = df1[ratings][col_df1]
rating_df


# In[549]:


col_df2 = ['App', 'Translated_Review', 'Sentiment']
df2[col_df2]


# In[550]:


reviews_df = rating_df.merge(df2[col_df2], on='App')
reviews_df_pivot = reviews_df.pivot_table('Rating',columns='Sentiment', index='App', aggfunc='count')
col = ['Positive', 'Neutral', 'Negative']
reviews_df_pivot = reviews_df_pivot[col]
reviews_df_pivot = calculate_percentage(reviews_df_pivot)
reviews_df_pivot = reviews_df_pivot.sort_values(by=['Neutral', 'Positive', 'Negative'], ascending=False)
zero_counts_filter = (reviews_df_pivot.Positive != 0.0) & (reviews_df_pivot.Neutral != 0.0) & (reviews_df_pivot.Negative != 0.0)
reviews_df_pivot = reviews_df_pivot[zero_counts_filter]
reviews_df_pivot


# In[551]:


plt.rcParams['figure.figsize'] = [20.0, 15.0]
reviews_df_pivot[0:70].plot(kind='barh', stacked=True)
plt.title("App rating f0r 70 apps")
plt.savefig("apps having ratings 2.5 to 3.5 first 70 app.jpg")
plt.show()


# In[553]:


plt.rcParams['figure.figsize'] = [20.0, 15.0]
reviews_df_pivot[70:140].plot(kind='barh', stacked=True)
plt.title("App rating f0r 70 apps")
plt.savefig("apps having ratings 2.5 to 3.5 70 to  140 app.jpg")
plt.show()


# In[554]:


plt.rcParams['figure.figsize'] = [20.0, 15.0]
reviews_df_pivot[140:210].plot(kind='barh', stacked=True)
plt.title("App rating f0r 70 apps")
plt.savefig("apps having ratings 2.5 to 3.5 140 to 210 app.jpg")
plt.show()


# In[555]:


print(f'{len(reviews_df_pivot)} Apps with rating between 2.5 and 3.5, many without reviews')
print(f'Positive sentiments: {round(reviews_df_pivot["Positive"].mean(), 3)}%')
print(f'Neutral sentiments: {round(reviews_df_pivot["Neutral"].mean(), 3)}%')
print(f'Negative sentiments: {round(reviews_df_pivot["Negative"].mean(), 3)}%')


# * ### Out of 9823 apps only 634 reviews are mentioned. But we see from these many reviews only that almost 63% are postivie reviews so our hypothesis is valid. 

# # Factors affecting the ratings of the App

# In[556]:


org_df = df1.copy()
org_df.head()


# In[557]:


df1["Rating"] = df1["Rating"].apply(lambda x: "Bad" if 0 <= x <2.5 else ("Average" if 2.5 <= x <3.5 else "Good"))


# In[558]:


df1["Size"] = df1["Size"].apply(lambda x: "Small" if 1 <= x <10 else ("Medium" if 10 <= x <30 else "Large"))


# In[559]:


df1.head()


# In[560]:


rating_install = df1.groupby("Rating")["Installs"].sum().sort_values(ascending = False).reset_index()
rating_install


# In[561]:


plt.figure(figsize=(10,8))
sns.set(font_scale=1.5)
plt.xticks(fontsize=15, rotation = 90)
plt.yticks(fontsize=15)
sns.barplot(data=rating_install, x = "Rating", y = "Installs")

plt.xlabel("Rating")
plt.title("Ratings Vs Number of installs")
plt.savefig("Taing Vs installs.jpg")
plt.show()


# * ### From here we can see clearly that if ratings are Good then a person wants to install an app.

# In[562]:


plt.figure(figsize=(15,7))
sns.set(font_scale=1.5)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
sns.countplot(data = df1, x = "Category", hue="Rating")
plt.xticks(rotation=90)
plt.title("Countplot of categories")
plt.savefig("Categories Countplot.jpg")
plt.show()


# * ### From here we can see that for game and family categories ratings are Good so we can assume that reviews are also postive. 

# In[563]:


plt.figure(figsize = (10,6))
sns.countplot(data = df1, x = "Size", hue = "Rating", palette = "rocket")
plt.xlabel("App size")
plt.title("Countplot for app size")
plt.savefig("App size Vs Rating.jpg")
plt.show()


# * ### from here we can assume that people prefer small size apps thats why there ratings are goods and because ratings are good it can also assume that people will post positive review if the size of the app is small.

# In[565]:


plt.figure(figsize = (10,6))
sns.countplot(data = df1, x = "Type", hue = "Rating", palette = "rocket")
plt.xlabel("Type of App")
plt.title("Countplot for app Type")
plt.savefig("App Type Vs Rating.jpg")
plt.show()


# * ### from here we can assume that people prefer Free apps thats why there ratings are goods and because ratings are good it can also assume that people will post positive review if the app is free.

# In[566]:


plt.figure(figsize = (10,6))
sns.countplot(data = df1, x = "Content Rating", hue = "Rating", palette = "rocket")
plt.xticks(rotation=90)
plt.xlabel("Content Rating of App")
plt.title("Countplot for Content Rating of App")
plt.savefig("Content Rating Vs Rating.jpg")
plt.show()


# * ### from here we can assume that people prefer the apps which can use by all thats why there ratings are goods and because ratings are good it can also assume that people will post positive review if the app is useful for everone.

# In[567]:


plt.figure(figsize=(10,8))
sns.heatmap(org_df.corr(), annot=True, cmap="BuPu")
plt.title("Correlation Matrix")
plt.savefig("Corr.jpg")
plt.show()


# ## From the above all analysis we can conclude that the apps will get postive reviews only when there ratings are good. And ratings are majorily depends on the size of the app, content rating of the app, category of the app, type of the app.

# In[ ]:




