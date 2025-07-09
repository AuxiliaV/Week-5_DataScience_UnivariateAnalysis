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
        descriptive=pd.DataFrame(index=["Mean","Median","Mode","Q1:25%","Q2:50%","Q3:75%","99%","Q4:100%","IQR","1.5Rule","Lesser","Greater","Min","Max","Kurtosis","Skew","Variance","Std_Deviation"] ,columns=quan)
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
            descriptive[columnName]["Kurtosis"]=dataset[columnName].kurtosis()
            descriptive[columnName]["Skew"]=dataset[columnName].skew()
            descriptive[columnName]['Variance']=dataset[columnName].var()
            descriptive[columnName]['Std_Deviation']=dataset[columnName].std()
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
    def get_pdf_probability(df,start_range,end_range):
        from matplotlib import pyplot
        from scipy.stats import norm
        import seaborn as sns
        ax=sns.distplot(df,kde=True,kde_kws={'color':'blue'},color='Green')
        pyplot.axvline(start_range,color='Red')
        pyplot.axvline(end_range,color='Red')
        sample=df
        sample_mean=sample.mean()
        sample_std=sample.std()
        print('Mean=%.3f,Standard Deviation=%.3f',(sample_mean,sample_std))
        dist=norm(sample_mean,sample_std)
        values=[value for value in range(start_range,end_range)]
        probabilities=[dist.pdf(value) for value in values]
        prob=sum(probabilities)
        print('The area between range ({},{}):{}'.format(start_range,end_range,sum(probabilities)))
        return prob
