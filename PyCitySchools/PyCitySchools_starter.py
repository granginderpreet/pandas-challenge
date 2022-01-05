#!/usr/bin/env python
# coding: utf-8

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# ## District Summary
# 
# * Calculate the total number of schools
# 
# * Calculate the total number of students
# 
# * Calculate the total budget
# 
# * Calculate the average math score 
# 
# * Calculate the average reading score
# 
# * Calculate the percentage of students with a passing math score (70 or greater)
# 
# * Calculate the percentage of students with a passing reading score (70 or greater)
# 
# * Calculate the percentage of students who passed math **and** reading (% Overall Passing)
# 
# * Create a dataframe to hold the above results
# 
# * Optional: give the displayed data cleaner formatting

# In[1]:


# Dependencies and Setup
import pandas as pd
import numpy as np


# File to Load (Remember to Change These)
school_data_to_load = "Resources/schools_complete.csv"
student_data_to_load = "Resources/students_complete.csv"

# Read School and Student Data File and store into Pandas DataFrames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset.  
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])

#Find number of unique schools and students
totalSchools=len(school_data_complete["school_name"].unique())
totalStudents=len(school_data_complete["Student ID"].unique())
#Total budget
totalBudget=school_data["budget"].sum()

#Find mean scores
averageMathScore=school_data_complete["math_score"].mean()
averageReadingScore=school_data_complete["reading_score"].mean()

#Conditional to find the passing Math and reading by counting number of students with markes > 70 %. 
#For overall pass, Math and reading should each be >= 70%
percentPassingMath=100*school_data_complete[school_data_complete["math_score"]>= 70]["Student ID"].count()/len(school_data_complete["Student ID"].unique())
percentPassingReading=100*school_data_complete[school_data_complete["reading_score"]>= 70]["Student ID"].count()/len(school_data_complete["Student ID"].unique())
percentOverallPassing=100*school_data_complete[(school_data_complete["math_score"]>= 70) & (school_data_complete["reading_score"]>= 70)]["Student ID"].count()/len(school_data_complete["Student ID"].unique())

#Summary 
summary= {"Total Schools":[totalSchools],
          "Total Students":[totalStudents],
          "Total Budget":[totalBudget],
          "Average Math Score": [averageMathScore],
          "Average Reading Score": [averageReadingScore],
          "% Passing Math": [percentPassingMath],
          "% Passing Reading": [percentPassingReading],
          "% Overall Passing": [percentOverallPassing]}

#convert a dict to data frame
summary_df=pd.DataFrame(summary)
summary_df


# In[ ]:





# ## School Summary

# * Create an overview table that summarizes key metrics about each school, including:
#   * School Name
#   * School Type
#   * Total Students
#   * Total School Budget
#   * Per Student Budget
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * % Overall Passing (The percentage of students that passed math **and** reading.)
#   
# * Create a dataframe to hold the above results

# In[2]:


# Create pass fail conditions and columns that save the pass fail value as 0 or 100
grouped_schools_summary_final_df={}
math_conditions = [
    (school_data_complete['math_score'] < 70),
    (school_data_complete['math_score'] >=70) 
    ]
reading_conditions = [
    (school_data_complete['reading_score'] < 70),
    (school_data_complete['reading_score'] >=70) ]
overall_conditions = [
    (school_data_complete['reading_score'] < 70) | (school_data_complete['math_score'] < 70) ,
    (school_data_complete['reading_score'] >=70) &  (school_data_complete['math_score'] >= 70)]

values=[0, 100]

# Use numpy to generate the % pass math/reading and overall scores
school_data_complete["% Passing Math Score"]=np.select(math_conditions,values)
school_data_complete["% Passing Reading Score"]=np.select(reading_conditions,values)
school_data_complete["% Passing Overall Score"]=np.select(overall_conditions,values)

#group by school name
grouped_schools_df = school_data_complete.groupby("school_name")

#Find mean 
grouped_schools_summary=grouped_schools_df.mean()

#New data frame to save the necessary columns
grouped_schools_summary_final = grouped_schools_summary.loc[:,["School ID",
                                                                "size", 
                                                                "reading_score", 
                                                                "math_score",
                                                                "% Passing Math Score",
                                                                "% Passing Reading Score",
                                                                "% Passing Overall Score",
                                                                "budget"]]

grouped_schools_summary_final_df=pd.DataFrame(grouped_schools_summary_final)
#Budget per student
grouped_schools_summary_final_df["Budget per student"]=grouped_schools_summary_final_df["budget"]/grouped_schools_summary_final_df["size"]

grouped_schools_summary_final_df= grouped_schools_summary_final_df.sort_values("School ID")
grouped_schools_summary_final_df["School Type"]= school_data["type"].to_numpy()
#Rename columns
grouped_schools_summary_final_df.rename(columns={"size":"Total Students","budget":"Total School Budget","reading_score":"Average Reading Score","math_score":"Average Math Score"},inplace=True)
#Drop School ID
grouped_schools_summary_final_df.drop(["School ID"], axis=1,inplace=True)
#Selected the requested columns
grouped_schools_summary_final_df=grouped_schools_summary_final_df[["School Type","Total Students","Total School Budget","Budget per student","Average Reading Score","Average Math Score","% Passing Math Score","% Passing Reading Score","% Passing Overall Score"]]
#grouped_schools_summary_final_df

#Cleaner formatting. Note that the format is in string format and so we cant use this format for float calc later. 
#Hence created a new frame for this. Still not clear why cant use this format.
def format(x):
    return "${:.1f}K".format(x/1000)
def format1(x):
    return "${:.1f}".format(x)
def format2(x):
    return "{:.2f}%".format(x)
def format3(x):
    return "{:.0f}".format(x)

grouped_schools_summary_final_df1=pd.DataFrame({})
#grouped_schools_summary_final_df1=grouped_schools_summary_final_df
grouped_schools_summary_final_df1["Total School Budget"]=grouped_schools_summary_final_df["Total School Budget"].apply(format)
#grouped_schools_summary_final_df1["Budget per student"]=grouped_schools_summary_final_df["Budget per student"].apply(format1)
grouped_schools_summary_final_df1["Average Reading Score"]=grouped_schools_summary_final_df["Average Reading Score"].apply(format2)
grouped_schools_summary_final_df1["Average Math Score"]=grouped_schools_summary_final_df["Average Math Score"].apply(format2)
grouped_schools_summary_final_df1["% Passing Math Score"]=grouped_schools_summary_final_df["% Passing Math Score"].apply(format2)
grouped_schools_summary_final_df1["% Passing Reading Score"]=grouped_schools_summary_final_df["% Passing Reading Score"].apply(format2)
grouped_schools_summary_final_df1["% Passing Overall Score"]=grouped_schools_summary_final_df["% Passing Overall Score"].apply(format2)
grouped_schools_summary_final_df1["Total Students"]=grouped_schools_summary_final_df["Total Students"].apply(format3)
grouped_schools_summary_final_df1


# ## Top Performing Schools (By % Overall Passing)
# grouped_schools_summary_final_df
# 

# * Sort and display the top five performing schools by % overall passing.

# In[3]:


# Top 5 schools based on overall passing score
grouped_schools_summary_final_df1.sort_values("% Passing Overall Score",ascending=False)[0:5]


# ## Bottom Performing Schools (By % Overall Passing)

# * Sort and display the five worst-performing schools by % overall passing.

# In[4]:


grouped_schools_summary_final_df1.sort_values("% Passing Overall Score",ascending=True)[0:5]


# ## Math Scores by Grade

# * Create a table that lists the average Reading Score for students of each grade level (9th, 10th, 11th, 12th) at each school.
# 
#   * Create a pandas series for each grade. Hint: use a conditional statement.
#   
#   * Group each series by school
#   
#   * Combine the series into a dataframe
#   
#   * Optional: give the displayed data cleaner formatting

# In[5]:




#create series for each grade and calculate mean
Nineth_series=school_data_complete[school_data_complete['grade']=="9th"]
Tenth_series=school_data_complete[school_data_complete['grade']=="10th"]
Eleventh_series=school_data_complete[school_data_complete['grade']=="11th"]
Twelvth_series=school_data_complete[school_data_complete['grade']=="12th"]
Nineth_series = Nineth_series.groupby("school_name")
Tenth_series = Tenth_series.groupby("school_name")
Eleventh_series = Eleventh_series.groupby("school_name")
Twelvth_series = Twelvth_series.groupby("school_name")

Nineth_series = Nineth_series.mean()
Tenth_series = Tenth_series.mean()
Eleventh_series = Eleventh_series.mean()
Twelvth_series = Twelvth_series.mean()

#Select ,math score for each grade and then create a frame with each grade being a column
Nineth_math_series= pd.Series(Nineth_series["math_score"])
Tenth_math_series= pd.Series(Tenth_series["math_score"])
Eleventh_math_series= pd.Series(Eleventh_series["math_score"])
Twelvth_math_series= pd.Series(Twelvth_series["math_score"])
allGradesMath = pd.DataFrame(columns = ['9th', '10th', '11th', '12th'])
allGradesMath['9th'] = Nineth_math_series
allGradesMath['10th'] = Tenth_math_series
allGradesMath['11th'] = Eleventh_math_series
allGradesMath['12th'] = Twelvth_math_series
allGradesMath


# ## Reading Score by Grade 

# * Perform the same operations as above for reading scores

# In[6]:




#Select reading score for each grade and then create a frame with each grade being a column
Nineth_reading_series= pd.Series(Nineth_series["reading_score"])
Tenth_reading_series= pd.Series(Tenth_series["reading_score"])
Eleventh_reading_series= pd.Series(Eleventh_series["reading_score"])
Twelvth_reading_series= pd.Series(Twelvth_series["reading_score"])
allGradesReading = pd.DataFrame(columns = ['9th', '10th', '11th', '12th'])
allGradesReading['9th'] = Nineth_reading_series
allGradesReading['10th'] = Tenth_reading_series
allGradesReading['11th'] = Eleventh_reading_series
allGradesReading['12th'] = Twelvth_reading_series
allGradesReading

#Scores by Budget per student
# * Create a table that breaks down school performances based on average Spending Ranges (Per Student). Use 4 reasonable bins to group school spending. Include in the table each of the following:
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * Overall Passing Rate (Average of the above two)

# In[7]:


#Binning into ranges as requested
budget_bins = [0, 585, 630, 645, 680]
budget_labels = ["<=$585", "$585-$630", "$630-$645","$645-$680"]



# cut() returns a Pandas Series containing each of the binned column's values translated into their corresponding bins
grouped_schools_summary_final_df2=grouped_schools_summary_final_df
grouped_schools_summary_final_df2["Budget range"]=pd.cut(grouped_schools_summary_final_df["Budget per student"], budget_bins, labels=budget_labels)
groupedBudgetPerStudent_df2 = grouped_schools_summary_final_df2.groupby(["Budget range"]).mean()
groupedBudgetPerStudent_df2=groupedBudgetPerStudent_df2[["Average Reading Score","Average Math Score","% Passing Math Score","% Passing Reading Score","% Passing Overall Score"]]
groupedBudgetPerStudent_df2.plot()

#Update format
groupedBudgetPerStudent_df2["Average Reading Score"]=groupedBudgetPerStudent_df2["Average Reading Score"].apply(format2)
groupedBudgetPerStudent_df2["Average Math Score"]=groupedBudgetPerStudent_df2["Average Math Score"].apply(format2)
groupedBudgetPerStudent_df2["% Passing Math Score"]=groupedBudgetPerStudent_df2["% Passing Math Score"].apply(format2)
groupedBudgetPerStudent_df2["% Passing Reading Score"]=groupedBudgetPerStudent_df2["% Passing Reading Score"].apply(format2)
groupedBudgetPerStudent_df2["% Passing Overall Score"]=groupedBudgetPerStudent_df2["% Passing Overall Score"].apply(format2)
groupedBudgetPerStudent_df2


# ## Scores by School Size

# * Perform the same operations as above, based on school size.

# In[8]:


#Scores by school size


# In[9]:


#binning per thousand
student_bins = [0,1000,2000,3000,4000,5000]
student_labels = ["<=1000", "1000-2000", "2000-3000","3000-4000","4000-5000"]

# cut() returns a Pandas Series containing each of the binned column's values translated into their corresponding bins
grouped_schools_summary_final_df2=grouped_schools_summary_final_df
grouped_schools_summary_final_df2["School Size"]=pd.cut(grouped_schools_summary_final_df["Total Students"], student_bins, labels=student_labels)

groupedBudgetPerStudent_df2 = grouped_schools_summary_final_df2.groupby(["School Size"]).mean()

groupedBudgetPerStudent_df2=groupedBudgetPerStudent_df2[["Average Reading Score","Average Math Score","% Passing Math Score","% Passing Reading Score","% Passing Overall Score"]]

#update format
groupedBudgetPerStudent_df2["Average Reading Score"]=groupedBudgetPerStudent_df2["Average Reading Score"].apply(format2)
groupedBudgetPerStudent_df2["Average Math Score"]=groupedBudgetPerStudent_df2["Average Math Score"].apply(format2)
groupedBudgetPerStudent_df2["% Passing Math Score"]=groupedBudgetPerStudent_df2["% Passing Math Score"].apply(format2)
groupedBudgetPerStudent_df2["% Passing Reading Score"]=groupedBudgetPerStudent_df2["% Passing Reading Score"].apply(format2)
groupedBudgetPerStudent_df2["% Passing Overall Score"]=groupedBudgetPerStudent_df2["% Passing Overall Score"].apply(format2)
groupedBudgetPerStudent_df2


# ## Scores by School Type

# * Perform the same operations as above, based on school type

# In[10]:


# cut() returns a Pandas Series containing each of the binned column's values translated into their corresponding bins


groupedBudgetPerStudent_df2 = pd.DataFrame(grouped_schools_summary_final_df.groupby(["School Type"]).mean())
groupedBudgetPerStudent_df2=groupedBudgetPerStudent_df2[["Average Reading Score","Average Math Score","% Passing Math Score","% Passing Reading Score","% Passing Overall Score"]]

#update format
groupedBudgetPerStudent_df2["Average Reading Score"]=groupedBudgetPerStudent_df2["Average Reading Score"].apply(format2)
groupedBudgetPerStudent_df2["Average Math Score"]=groupedBudgetPerStudent_df2["Average Math Score"].apply(format2)
groupedBudgetPerStudent_df2["% Passing Math Score"]=groupedBudgetPerStudent_df2["% Passing Math Score"].apply(format2)
groupedBudgetPerStudent_df2["% Passing Reading Score"]=groupedBudgetPerStudent_df2["% Passing Reading Score"].apply(format2)
groupedBudgetPerStudent_df2["% Passing Overall Score"]=groupedBudgetPerStudent_df2["% Passing Overall Score"].apply(format2)
groupedBudgetPerStudent_df2


# In[11]:



#Additional investigation on why district schools have lower scores thn charter schools

groupedBudgetPerStudent_df2=pd.DataFrame(grouped_schools_summary_final_df.groupby(["School Type"]).mean())

groupedBudgetPerStudent_df2 = groupedBudgetPerStudent_df2[["Budget per student",
                                                            "Average Reading Score",
                                                            "Average Math Score",
                                                            "% Passing Math Score",
                                                            "% Passing Reading Score",
                                                            "% Passing Overall Score"]]

#Plot graphs
groupedBudgetPerStudent_df2[["Average Reading Score","Average Math Score",
                             "% Passing Math Score","% Passing Reading Score","% Passing Overall Score"]].plot()
groupedBudgetPerStudent_df2[["Budget per student"]].plot()

#Update format
grouped_schools_summary_final_df2["Budget per student"]=grouped_schools_summary_final_df2["Budget per student"].apply(format1)
groupedBudgetPerStudent_df2["Average Math Score"]=groupedBudgetPerStudent_df2["Average Math Score"].apply(format2)
groupedBudgetPerStudent_df2["Average Reading Score"]=groupedBudgetPerStudent_df2["Average Reading Score"].apply(format2)
groupedBudgetPerStudent_df2["% Passing Math Score"]=groupedBudgetPerStudent_df2["% Passing Math Score"].apply(format2)
groupedBudgetPerStudent_df2["% Passing Reading Score"]=groupedBudgetPerStudent_df2["% Passing Reading Score"].apply(format2)
groupedBudgetPerStudent_df2["% Passing Overall Score"]=groupedBudgetPerStudent_df2["% Passing Overall Score"].apply(format2)
groupedBudgetPerStudent_df2


# In[ ]:





# In[ ]:




