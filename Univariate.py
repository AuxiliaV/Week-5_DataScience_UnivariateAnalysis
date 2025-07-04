import pandas as pd
import numpy as np
class Univariate():
    def quanQual(dataset):
        quan=[]
        qual=[]
        for columnName in dataset:
            if (dataset[columnName].dtype=='O'):
                qual.append(columnName)
            else:
                quan.append(columnName)
        return quan,qual
    def MMM_IQR(dataset,quan):
        descriptive=pd.DataFrame(index=["Mean","Median","Mode","Q1:25%","Q2:50%","Q3:75%","99%","Q4:100%","IQR","1.5Rule","Lesser","Greater","Min","Max"] ,columns=quan)
        for columnName in quan:
            descriptive[columnName]["Mean"]=dataset[columnName].mean()
            descriptive[columnName]["Median"]=dataset[columnName].median()
            descriptive[columnName]["Mode"]=dataset[columnName].mode()[0]
            descriptive[columnName]["Q1:25%"]=dataset.describe()[columnName]["25%"]  
            descriptive[columnName]["Q2:50%"]=dataset.describe()[columnName]["50%"]
            descriptive[columnName]["Q3:75%"]=dataset.describe()[columnName]["75%"]
            descriptive[columnName]["99%"]=np.percentile(dataset[columnName],99)
            descriptive[columnName]["Q4:100%"]=dataset.describe()[columnName]["max"]
            descriptive[columnName]["IQR"]=descriptive[columnName]["Q3:75%"]-descriptive[columnName]["Q1:25%"]
            descriptive[columnName]["1.5Rule"]=1.5*descriptive[columnName]["IQR"]
            descriptive[columnName]["Lesser"]=descriptive[columnName]["Q1:25%"]-descriptive[columnName]["1.5Rule"]
            descriptive[columnName]["Greater"]=descriptive[columnName]["Q3:75%"]+descriptive[columnName]["1.5Rule"]
            descriptive[columnName]["Min"]=dataset[columnName].min()
            descriptive[columnName]["Max"]=dataset[columnName].max()
        return descriptive
    def Outliers(descriptive,quan):
        lesser=[]
        greater=[]
        for columnName in quan:
            if (descriptive[columnName]["Min"]<descriptive[columnName]['Lesser']):
                lesser.append(columnName)
            if (descriptive[columnName]["Max"]>descriptive[columnName]['Greater']):
                greater.append(columnName)
        return lesser,greater
    def replaceOutliers(dataset,descriptive,lesser,greater):
        for columnName in lesser:
            dataset[columnName][dataset[columnName]<descriptive[columnName]['Lesser']]=descriptive[columnName]['Lesser']
        for columnName in greater:
            dataset[columnName][dataset[columnName]>descriptive[columnName]['Greater']]=descriptive[columnName]['Greater']
        return dataset
    def frequency(dataset):
        freq_Table=pd.DataFrame(columns=['Unique_Values','Frequency','Relative_Frequency','Cumsum'])
        column=input("Enter the column name to find Freq, Relative Freq, Cumsum:")
        num=len(dataset[column].value_counts())
        freq_Table["Unique_Values"]=dataset[column].value_counts().index
        freq_Table["Frequency"]=dataset[column].value_counts().values
        freq_Table["Relative_Frequency"]=freq_Table["Frequency"]/num
        freq_Table["Cumsum"]=freq_Table["Relative_Frequency"].cumsum()
        return freq_Table
        
