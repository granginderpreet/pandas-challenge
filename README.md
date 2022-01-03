# pandas-challenge

#Jupyter notebook has comments whereever necessary. 
#Assignent uses the read_csv function in pandas to read data from excel. Then it merged the two data sets together by using merge function in pandas
#Then uses unique and mean functions in dataframes to get to summary
#also uses the conditional in data frames 

#For school summary, it uses numpy library to create new colujmns in data frame that is based on values in another column using conditionals
#Then we use the groupby() fuxntion to group the frame by school name and we then calculate mean for each school using the mean() function
#Average budget per student for each school is calculcated in a new column using total budget/size
#Some formatting is done to display the necessary columns. Note that I tried to format the values to show it nicely but I see problems with latter questions.
#So I had to comment some of the formatting


#Sort_values() was used to sort values by passign overall score

#per grade math and english reading scores were based on calulating series mean and combining pd.series and combining into a dataFrame  with each column representing one grade
#binning was done for lst part of the assignment using the pd.cut() function and then groupby().mean() to get the mean values for each of the bins.

plot() function was used to plot some of the plots and analysis was provided in the word document
