#!/usr/bin/env python
# coding: utf-8

# ## The Play Store apps data has enormous potential to drive app-making businesses to success. Actionable insights can be drawn for developers to work on and capture the Android market. 
# ## Each app (row) has values for catergory, rating, size, and more. Another dataset contains customer reviews of the android apps. 
# ## Explore and analyze the data to discover key factors responsible for app engagement and success.

# In[576]:


import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

os.chdir(r"C:\Users\asus\Desktop\Almabetter\datasets\capstone projects")


# In[577]:


df = pd.read_csv("Play Store Data.csv")


# In[578]:


df.head()


# In[579]:


df[["date","year"]] = df["Last Updated"].str.split(",",expand=True)
df.drop("Last Updated", axis=1, inplace=True)


# In[580]:


print("df shape is",df.shape)


# In[581]:


df.info()


# # 1. Data Cleaning
# 

# In[582]:


# Data type of installs column is string and we have to convert this string data type into int and removing unwanted strings(+,)

# here rstrip function is used to remove the right most string('+') from the string

df["Installs"] = df["Installs"].map(lambda x: x.rstrip("+"))

# here split method is used to remove "," between the numbers and then join method is joining the splitted string.

df["Installs"] = df["Installs"].map(lambda x: ''.join(x.split(",")))


# In[583]:


df["Size"] = df["Size"].map(lambda x: x.rstrip("M"))

df["Size"] = df["Size"].map(lambda x: str(round((float(x.rstrip("k"))/1024),2)) if x[-1] == "k" else x)


# In[584]:


df[df["Price"] != "0"].head()


# In[585]:


df["Price"] = df["Price"].map(lambda x: x.lstrip("$") if x.startswith("$") else x)
df[df["Price"] != "0"].head()


# In[586]:


df.info()


# ### Handling null Values

# In[587]:


df["Rating"].fillna(df["Rating"].mean(), inplace = True)


# In[588]:


df.dropna(axis=0,inplace=True)


# In[589]:


df.isnull().sum()


# In[590]:


df.shape


# ## Changing the Data Types of columns
# 

# In[591]:


df["Reviews"] = df["Reviews"].apply(lambda x: x).astype(int)
df["Size"] = df["Size"].apply(lambda x: float(x) if x != "Varies with device" else str(x))
df["Installs"] = df["Installs"].apply(lambda x: x).astype(int)
df["Price"] = df["Price"].apply(lambda x: x).astype(float)
df["year"] = df["year"].apply(lambda x: x).astype(int)


# In[592]:


df.info()


# In[593]:


# Converting number of installs into percentage.

count_of_values = df["Installs"].value_counts()
total_count = count_of_values.sum()
percent_of_each_values = round(count_of_values/total_count,2)*100
print(percent_of_each_values)


# # DATA VISULAISATION

# #### 1. Plotting a count plot for Category  

# In[594]:


plt.figure(figsize=(15,7))
sns.set(font_scale=1.5)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
sns.countplot(df["Category"])
plt.xticks(rotation=90)


# From the count plot one can see that the top most category in this dataset is Family of count 1968, followed by Game-1144, Tools-841, Medical-463, Budiness-460

# In[595]:


top_cat=df.groupby("Category").size().reset_index(name='Count').nlargest(5,'Count')
top_cat


# #### 2. Plotting a graph of showing total number of installation for each category 

# In[596]:


# Grouping Category column with the installs column

no_of_installs = df.groupby("Category")["Installs"].sum().reset_index()
no_of_installs.head()


# In[597]:


plt.figure(figsize=(15,7))
sns.set(font_scale=1.5)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
sns.barplot(data=no_of_installs,x="Category",y="Installs")
plt.xticks(rotation=90)
plt.title("Total number of installation for every category")


# Communication is the category in which highest number of installation happend, followed by Game, Productivity, Social and Tools

# #### 3. Plotting a graph of showing total number of installation for each Content Ratings 

# In[598]:


content_rat = df.groupby("Content Rating")["Installs"].sum().reset_index()
content_rat


# In[599]:


app_conntent = df.groupby("Content Rating")["Installs"].size().reset_index(name = "number of apps")
app_conntent 


# In[600]:


plt.figure(figsize=(15,7))
sns.set(font_scale=1.5)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
sns.barplot(data=content_rat,x="Content Rating",y="Installs")
plt.title("Total number of installation for every Content ratings")


# In[601]:


plt.figure(figsize=(15,7))
sns.set(font_scale=1.5)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

sns.barplot(data=app_conntent,x="Content Rating",y="number of apps")
plt.title("Total number of apps for every Content ratings")


# In[602]:


Type_of_app = df.groupby("Type")["Installs"].sum().reset_index()
Type_of_app


# In[603]:


plt.figure(figsize =(15, 7))
mycolors = ["black"]
plt.pie(Type_of_app["Installs"], labels = Type_of_app["Type"], colors = mycolors)


# From this pie chart anyone can see that peoples prefers the app which is free

# In[604]:


plt.figure(figsize=(20,15))
sns.set(font_scale=1.5)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
app_install= df.groupby("App")["Installs"].sum().sort_values(ascending= False).head(20)
sns.barplot(app_install.values,app_install.index)
plt.xlabel("Total installation of each app")


# In[605]:


plt.figure(figsize=(20,15))
sns.set(font_scale=1.5)
plt.xticks(fontsize=15, rotation = 90)
plt.yticks(fontsize=15)
size_install= df.groupby("Size")["Installs"].sum().sort_values().head(50)

sns.barplot(size_install.index, size_install.values)

plt.xlabel("Total installation of each app")


# In[606]:


plt.figure(figsize=(20,15))
sns.set(font_scale=1.5)
plt.xticks(fontsize=15, rotation = 90)
plt.yticks(fontsize=15)
size_install= df.groupby("Size")["Installs"].sum().sort_values(ascending = False).head(50)

sns.barplot(size_install.index, size_install.values)

plt.xlabel("Total installation of each app")


# From the above two plots it is clear that if the app size is small then number of installation is more.

# In[607]:


df.head()


# In[608]:


rating_install = df.groupby("Rating")["Installs"].sum().sort_values(ascending = False).reset_index()


# In[609]:


plt.figure(figsize=(20,15))
sns.set(font_scale=1.5)
plt.xticks(fontsize=15, rotation = 90)
plt.yticks(fontsize=15)
sns.barplot(data=rating_install, y = "Rating", x = "Installs")

plt.xlabel("Total installation of each app")


# This plot is showing if the ratings are high then installions are also high.

# In[610]:


plt.figure(figsize=(10,8))
sns.heatmap(df.corr(), annot=True, cmap="BuPu")


# In[612]:


df = df.drop(["Genres","Current Ver",  "Android Ver", "date", "year", "Price"], axis=1)
df


# ###  The key factors responsible for app engagement and success are :-
# #### 1. App	
# #### 2.Category	
# #### 3.Rating	
# #### 4.Reviews	
# #### 5.Size	
# #### 6.Installs	
# #### 7.Type	
# #### 8.Content Rating

# In[ ]:




