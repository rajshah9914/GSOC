# GSoC 

GSoC 2018 project: Deep learning modeling to discover the regulatory sequence motifs that predict the cancer drug responses.

### Project summary

The products of this project including two parts

- The detailed process of data collection and model training is illustrated in the Jupyter notebook. You could follow the instructions and run through the notebooks by yourself.   
- A web tool is also developed and it could be used for exploring cancer related eQTL and drug target information, building and testing machine learning model for drug response prediction, and also predicting IC50 values for the given patient's  genomic profiles with the DNN model.   [[DEMO](http://xxmen.pythonanywhere.com/gene/)]

The web tool  is built with python django framework, and the predicting models are built with scikit-learn and keras with tensorflow backend.  This repository containing three folders, `data/` is for the csv files and other used data,  `notebook/` folder contains the Jupyter notebook that provide instruction for building and evaluating deep learning model. and the `web_tool/` folder contains the source code of the django web project.

### Getting started

The Jupyter notebooks and the web tool can be used easily. Python 3 is used in this project, and the latest Anaconda environment(https://www.anaconda.com/download/) is recommended to install. Before running the notebooks or starting the website on your server, following required packages should be installed, you could install them with `conda install` or `pip install` in command line.

- numpy (http://www.numpy.org/)
- pandas (https://pandas.pydata.org/)
- scikit-learn (http://scikit-learn.org/stable/)
- keras (https://keras.io/)
- tensorflow (https://www.tensorflow.org)
- matplotlib (https://matplotlib.org/)
- django (https://www.djangoproject.com/)

For the notebook, you could run it directly if you have Jupyter notebook installed(already packed in Anaconda).

As for the web tool, it is developed with django framework and MySQL database, so you need to install both of them before running the django server. You could follow the instructions below to set up the server. First you need to clone this repository to your local folder.

`git clone xxx` 

Then you should go the `web_tool/` folder which contains `manage.py`, and run

`python3 manage.py makemigrations`

`python3 manage.py migrate`

And then we should insert the data into MySQL database. The data is packed in `SQL_data.zip`, you should unzip them and  then run following instructions in the MySQL command line

`use django;` 

`source path/to/file.sql;` 

In the `settings.py` , you could change the configuration of database to ensure that django to connect to the database properly. 

If every thing goes fine, you could start our local server by 

`python3 manage.py runserver`

Now the website is up and running at localhost  (http://127.0.0.1:8000).

You could go to the home page of the web tool at http://127.0.0.1:8000/gene/ .

#### Cancer Cis-eQTLs query

Go to the link http://127.0.0.1:8000/gene/ and you could search for Cis-eQTLs data for selected cancer type and gene. You could 

- Enter a SNP ID for detailed information of eQTL-gene pair.
- Enter a gene symbol(with specific cancer type) to find the corresponding eQTLs.

#### Drug information search

You could search for cancer drug information in http://127.0.0.1:8000/gene/drug/ .

The whole drug list included in this project (from GDSC) will be provided. And you could

- Enter a name of drug for detailed information.
- Enter a target gene to find the corresponding drugs.

#### Machine learning model

You could build machine learning model for drug response prediction with uploaded training data and label  on the web page http://127.0.0.1:8000/model/upload/. You could find the instructions below as well as on the website.

1. Upload training data matrix in csv format or use example files (First column of the data matrix should be the cell-line index, First row of the data matrix should be header.
   See example data files for more details).
2. Choose an algorithm with the number of dimension to perform dimension reduction(Must perform once).
3. Choose a machine learning model to train and evaluate with selected metric, cross-validation will be performed.

#### Drug response prediction 

You could upload the genomic profiles (mutation data), select one drug and get the predicted IC50 values based on the trained deep learning model. The link is http://127.0.0.1:8000/DNN/predict/. You could find the instructions here as well as on the website.

1. Upload individual mutation profile in csv format or use example files (The gene mutation status order should be the same as example. See example data file for more details).
2. Select a drug click the predict button to get predicted IC50 value.

### Deployment

You could deploy the django website on a remote server if you want. You could find more information about how to config django settings when you deploy them on remote server in the django official documents.

### Future work

The web tool only contain parts of the cancer eQTL data for now, more data can be added in the future. As for the deep learning model, there is still room for improvement.  The best model is built with cell line mutation data only, further model tuning is needed to incorporate other genomic profiles like gene expression data to make better prediction. Further biological analysis could be made to provide insight for precision medicine. 

### Acknowledgments

This project is supported by Google Summer Of Code and mentored by Prof.Daifeng Wang of Stony Brook University. 



