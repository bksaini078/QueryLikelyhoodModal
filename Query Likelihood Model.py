#!/usr/bin/env python
# coding: utf-8

# • D1: click go the shears boys click click click
# • D2: click click
# • D3: metal here
# • D4: metal shears click here

# In[1]:


D1="click go the shears boys click click click"
D2="click click"
D3="metal here"
D4="metal shears click here"
Q= "click shears";


# In[2]:


import pandas as pd 
import collections
from collections import Counter 
lam= 0.5;# lambda for linear interpolation
def wordFreqDictionary(List):#frequency of word calculation
    List.sort();
    freq=[];
    total_length=0;
    for w in List:
     freq.append(List.count(w))
     total_length+=1;
    return dict(zip(List,freq)),total_length
#The probability of producing the query given the language model of document d:
def langModelDoc(corpus,doc_dic,totallength):
    D_tMd=[];   
    for key in corpus:
        if(doc_dic.get(key)):
            value= doc_dic.get(key);
            D_tMd.append(value/totallength)
        else:
            doc_dic[key]=0;
            D_tMd.append(0);
    return D_tMd,sorted(doc_dic.items())
#collecting each word in the list .
D1_Ls= D1.split(" ");
D2_Ls= D2.split(" ");
D3_Ls= D3.split(" ");
D4_Ls= D4.split(" ");
Q_Ls= Q.split(" ");

Corpus= sorted(D1_Ls+D2_Ls+D3_Ls+D4_Ls);#creating collections of the word

#dictionary word and frequency
D1_Dic,L_D1=wordFreqDictionary(D1_Ls);
D2_Dic,L_D2=wordFreqDictionary(D2_Ls);
D3_Dic,L_D3=wordFreqDictionary(D3_Ls);
D4_Dic,L_D4=wordFreqDictionary(D4_Ls);
Corpus_Dic,L_C=wordFreqDictionary(Corpus);

#keys, values = D1_Dic.keys(), D1_Dic.values();
forLoopList = ["D1","D2","D3","D4"];
#calling language model
D1_Mtd,D1_DicU=langModelDoc(Corpus_Dic,D1_Dic,L_D1)
D2_Mtd,D2_DicU=langModelDoc(Corpus_Dic,D2_Dic,L_D2)
D3_Mtd,D3_DicU=langModelDoc(Corpus_Dic,D3_Dic,L_D3)
D4_Mtd,D4_DicU=langModelDoc(Corpus_Dic,D4_Dic,L_D4)
Corpus_Mtc,Corpus_DicU=langModelDoc(Corpus_Dic,Corpus_Dic,L_C)
#printing updated document frequency , here I have included terms that are not present in the 
#document add as zero frequency.
print(D1_DicU)
print(D2_DicU)
print(D3_DicU)
print(D4_DicU)
print(Corpus_DicU)

#[ print(key , " :: " , value) for (key, value) in sorted(D1_DicU.items()) ]


# In[9]:


# adding to dataframe 
df_prob=pd.DataFrame(D1_Mtd,Corpus_Dic,columns=['Pmd1(t)'])
df_prob['Pmd2(t)']=D2_Mtd;
df_prob['Pmd3(t)']=D3_Mtd;
df_prob['Pmd4(t)']=D4_Mtd;
df_prob['Pmdc(t)']=Corpus_Mtc;
df_prob.index.name='Terms';
df_prob


# In[14]:


df_NoPmdc= df_prob.drop('Pmdc(t)',axis=1);
#print(columnsData)
columnsData=[];
#calculating ranked result of unsmoothed
for items in Q_Ls:
    if len(columnsData)==0:
        columnsData=df_NoPmdc.loc[items ,:];
    else:
        columnsData =columnsData*df_NoPmdc.loc[items ,:];
P_uni_QD=columnsData;#ranked result without smoothing 

rankedResult= pd.DataFrame(forLoopList,P_uni_QD,columns=[' Doc_no.'])#.sort_values(ascending=False));
rankedResult.index.name='Relevance';
ranked_Sorted=rankedResult.sort_index(ascending=0);
print("Ranked result set according to the un-smoothed, uniform model 𝑃𝑢𝑛𝑖(𝑞 ∣ 𝑑).")


ranked_Sorted


# In[5]:


Pmdc= df_prob['Pmdc(t)'];# dropping as it is not required in unsmoothed data
Pmdc=Pmdc.loc[Q_Ls];# Pmdc as per query 
rankedResult_linear=df_NoPmdc.loc[Q_Ls] # Pmdt as per ranked query 
rankedResult_linear.reset_index(inplace=False)


# In[13]:


# this function will return the addition of Probability of document and collection to avoid zero 
#zero probability 
def linear_interpolated(row):
    sumofPtMd=0; #sum of document probability 
    sumofPtMc=0;# sum of corpus probability
    for items in Q_Ls:
        sumofPtMdPtmc = row[items]+Pmdc[items];
        print(sumofPtMdPtmc)
    return sumofPtMdPtmc
#multiplying document probability with lambda of query terms 
rankedResult_linear1=rankedResult_linear*lam;
#multiplying 1-lambda with corpus probility of query terms 
Pmdc1=(1-lam)*Pmdc;
#adding as per the formula 
Final_rankedResult=(rankedResult_linear1.loc['click']+Pmdc1['click']) *(rankedResult_linear1.loc['shears']+Pmdc1['shears']);
#Final_rankedResult
#adding column
testing=pd.DataFrame(forLoopList,Final_rankedResult,columns=[' Doc_no.'])
testing.reset_index(inplace=False)
testing.index.name='Relevance';#adding relevance to column 1
Finaltest_Sorted=testing.sort_index(ascending=0);
#sorted list after smoothing 
Finaltest_Sorted

