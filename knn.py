from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score

from sklearn import preprocessing
import numpy as np
from sklearn import metrics
import pandas as pd
import matplotlib.pyplot as plt
import shap
from IPython import display


def main():
    plt.style.use("ggplot")

    raw = pd.read_csv("./data/journeys.csv", index_col='id', parse_dates=True, na_values=['nan']) 

    df = raw[['age', 'language', 'journey', 'touchpoint','duration', 'conversion','email', 'facebook', 'house_ads', 'instagram', 'push']]

    categorical_vars = ['age','language'] 


    # creating one hot encoder object 
    label_encoder = preprocessing.LabelEncoder()
    for each in categorical_vars:
        df[each]= label_encoder.fit_transform(df[each]) 


    labels = df.conversion
    X = df.loc[:, df.columns != 'conversion']
    

    
    y = df.conversion

    accuracy = []
    error = []
    f_score = []
    cv = []
    X_train, X_test, y_train, y_test = train_test_split(df,labels, test_size=0.2, random_state=123)

    # Calculating error for K values
    k_min = 1
    k_max = 50
    for i in range(k_min, k_max):
        knn_cv = KNeighborsClassifier(n_neighbors=i)
        cv.append((cross_val_score(knn_cv, X, y, cv=5, scoring='f1')).mean())
        knn = KNeighborsClassifier(n_neighbors=i)
        knn.fit(X_train, y_train)
        pred_i = knn.predict(X_test)
        # error.append(np.mean(pred_i != y_test))
        # accuracy.append(np.mean(pred_i == y_test))
        f_score.append(metrics.f1_score(y_test, list(pred_i), average='macro'))
    plt.figure(figsize=(12, 6))
    # plt.plot(range(k_min, k_max), f_score, color='black', linestyle='dashed', marker='x',
    # markerfacecolor='green', markersize=10)
    plt.plot(range(k_min, k_max), cv, color='black', linestyle='dashed')
    plt.plot(range(k_min, k_max), f_score, color='green', linestyle='dashed')
    # plt.plot(range(k_min, k_max), accuracy, color='green', linestyle='dashed')
    plt.title('F1 Score by K Value')
    plt.xlabel('K Value')
    plt.ylabel('F1 Score')
    plt.savefig('knn.jpg')
    



    # reference https://machinelearningknowledge.ai/knn-classifier-in-sklearn-using-gridsearchcv-with-example/
    # defining parameter range
    # reference https://towardsdatascience.com/explain-any-models-with-the-shap-values-use-the-kernelexplainer-79de9464897a
    knn = KNeighborsClassifier()
    k_range = list(range(k_min, k_max))
    param_grid = dict(n_neighbors=k_range)
    grid = GridSearchCV(knn, param_grid, cv=10, scoring='f1', return_train_score=False,verbose=1)
    
    # fitting the model for grid search
    model = grid.fit(X_train, y_train)
    print(model.best_params_)

    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred) 
    print(confusion_matrix(y_test, y_pred))
    print(report)


    FP = X_test[(y_test == 0) & (y_pred == 1)]
    print(FP)




if __name__ == "__main__":  		  	   		   	 		  		  		    	 		 		   		 		  
    main()  