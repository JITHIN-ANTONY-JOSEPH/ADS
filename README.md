This repo contains the entire codebase used during the SDK Finance ADS P07 project.
This project aims to develop a pipeline for e-wallet fraudulent transactions detections for an industry partner, based on relational data with a given data schema. Which goes as follows:
Data exploration and visualisation
Anomaly detection with an unsupervised learning model
Anomaly prediction with a supervised learning model
Automation of the pipeline
The pipeline was applied to an example data given by ‘name’, which is 4.0GB worth of synthetic data with 16636702 transactions which was partitioned in 1664 segments. We conducted data analysis on different combinations of segments of the data and the entire data, to evaluate the loss of information comparing the analysis of segments and the data itself to simulate, as examining samples of a large data set can be much more efficient for a pipeline that runs frequently. The details of each Jupyter Notebook file are given below. 

The Python notebooks inside Models show the code for the respective models and its performances. They are named are per their respective model for easy identification.
 
 **unsupervised:**
    Application of the unsupervised learning models Isolation Forest, one-class SVM from the sklearn package on a sample of the data formed from the ‘total data’ file, and calculate the accuracy, precision, recall, F1-score of their predictions based on the flagged variable.
  
  **supervised:**
    Application of the supervised learning models RPCA, KNN, Adaboost,  LightGBM from the sklearn package on a sample of the data formed from the ‘total data’ file, and calculate the accuracy, precision, recall, F1-score of their predictions based on the flagged variable.

Under the Analyiss folder you would find 2 notebooks : Full_Data_Analysis which holds the visualisation and Feature Engineering for the whole of the data and then Segment_Analysis that holds the analsis only for a selected segment of the data.

![image](https://github.com/JITHIN-ANTONY-JOSEPH/ADS/assets/49895934/4f6212db-bb9b-48b4-bc5a-6c647ae663f9)



