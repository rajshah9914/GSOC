from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import pandas as pd
from sklearn.decomposition import PCA
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn import tree, svm
from sklearn.ensemble import RandomForestClassifier

def upload_file(request):
    if request.method == 'POST':
        settings.MUT_FLAG = False
        settings.CNV_FLAG = False
        settings.EXP_FLAG = False
        uploaded_file_url = ''
        fs = FileSystemStorage()
        if 'label' not in request.FILES or (not request.FILES['label']):
            return render(request, 'upload_file.html', {
                'label_not_found': 1
            })
        if 'mutation' in request.FILES and request.FILES['mutation']:
            mutation = request.FILES['mutation']
            settings.MUT_FILE_NAME = fs.save(mutation.name, mutation)
            uploaded_file_url = fs.url(settings.MUT_FILE_NAME)
            settings.MUT_FLAG = True
        if 'cnv' in request.FILES and request.FILES['cnv']:
            cnv = request.FILES['cnv']
            settings.CNV_FILE_NAME = fs.save(cnv.name, cnv)
            uploaded_file_url += ' ' + fs.url(settings.CNV_FILE_NAME)
            settings.CNV_FLAG = True
        if 'expression' in request.FILES and request.FILES['expression']:
            expression = request.FILES['expression']
            settings.EXP_FILE_NAME = fs.save(expression.name, expression)
            uploaded_file_url += ' ' + fs.url(settings.EXP_FILE_NAME)
            settings.EXP_FLAG = True
        if 'label' in request.FILES and request.FILES['label']:
            label = request.FILES['label']
            settings.LABEL_FILE_NAME = fs.save(label.name, label)
            uploaded_file_url += ' ' + fs.url(settings.LABEL_FILE_NAME)
        return render(request, 'upload_file.html', {
            'uploaded_file_url': uploaded_file_url
        })
    if request.method == 'GET' and 'file' in request.GET and request.GET['file'] == 'example':
        settings.MUT_FLAG = True
        settings.CNV_FLAG = True
        settings.EXP_FLAG = True
        settings.MUT_FILE_NAME = 'mutation_data.csv'
        settings.CNV_FILE_NAME = 'cnv_data.csv'
        settings.EXP_FILE_NAME = 'expression_data.csv'
        settings.LABEL_FILE_NAME = 'label_data.csv'
        example_mut_file_url = settings.MEDIA_ROOT + '\\' + settings.MUT_FILE_NAME
        example_cnv_file_url = settings.MEDIA_ROOT + '\\' + settings.CNV_FILE_NAME
        example_exp_file_url = settings.MEDIA_ROOT + '\\' + settings.EXP_FILE_NAME
        example_label_file_url = settings.MEDIA_ROOT + '\\' + settings.LABEL_FILE_NAME
        return render(request, 'upload_file.html', {
            'example_mut_file_url': example_mut_file_url,
            'example_cnv_file_url': example_cnv_file_url,
            'example_exp_file_url': example_exp_file_url,
            'example_label_file_url': example_label_file_url
        })

    if request.method == 'GET' and 'dimension_reduction' in request.GET and request.GET['dimension_reduction']:
        dr = request.GET['dimension_reduction']
        num_of_dim = 100
        if 'num_of_dim' in request.GET and request.GET['num_of_dim']:
            num_of_dim = int(request.GET['num_of_dim'])
        reduce_dimension(dr, dims=num_of_dim)
        return render(request, 'upload_file.html', {
            'dr_status': 'Done!'
        })
    return render(request, 'upload_file.html')


def reduce_dimension(dr, dims):
    mutation = pd.read_csv(settings.MEDIA_ROOT + '\\' + settings.MUT_FILE_NAME)
    X = mutation.iloc[:, 1:]
    if settings.CNV_FLAG:
        cnv = pd.read_csv(settings.MEDIA_ROOT + '\\' + settings.CNV_FILE_NAME)
        cnv = cnv.iloc[:, 1:]
        X = pd.concat([X, cnv], axis=1)
    if settings.EXP_FLAG:
        expression = pd.read_csv(settings.MEDIA_ROOT + '\\' + settings.EXP_FILE_NAME)
        expression = expression.iloc[:, 1:]
        X = pd.concat([X, expression], axis=1)
    if dr == 'pca':
        pca = PCA(n_components=dims)
        df = pd.DataFrame(pca.fit_transform(X))
        df.to_csv(settings.MEDIA_ROOT + '\\input_data.csv')
        return
    elif dr == 'autoencoder':
        Autoencoder(X, dims)
        return
    else:
        mutation = pd.read_csv(settings.MEDIA_ROOT + '\\' + settings.MUT_FILE_NAME)
        X = mutation.iloc[:, 1:]
        if settings.CNV_FLAG:
            cnv = pd.read_csv(settings.MEDIA_ROOT + '\\' + settings.CNV_FILE_NAME)
            cnv = cnv.iloc[:, 1:]
            X = pd.concat([X, cnv], axis=1)
        if settings.EXP_FLAG:
            expression = pd.read_csv(settings.MEDIA_ROOT + '\\' + settings.EXP_FILE_NAME)
            expression = expression.iloc[:, 1:]
            X = pd.concat([X, expression], axis=1)
        X.to_csv(settings.MEDIA_ROOT + '\\input_data.csv')
        return


def Autoencoder(X, dims):
    from keras.layers import Input, Dense
    from keras.models import Model

    X_raw_shape = X.shape
    input_data = Input(shape=(X_raw_shape[1],))
    encoded = Dense(dims, activation='relu')(input_data)
    decoded = Dense(X_raw_shape[1], activation='sigmoid')(encoded)
    autoencoder = Model(input_data, decoded)
    encoder = Model(input_data, encoded)
    autoencoder.compile(optimizer='adam', loss='binary_crossentropy')
    X = np.array(X)
    autoencoder.fit(X, X, epochs=10, batch_size=128, shuffle=True)
    df = pd.DataFrame(encoder.predict(X))
    df.to_csv(settings.MEDIA_ROOT + '/input_data.csv', header=None)
    return

def predict(request):
    if request.method == 'GET':
        alg = ''
        metric = 'accuracy'
        if 'algorithm' in request.GET and request.GET['algorithm']:
            alg = request.GET['algorithm']
        if 'metric' in request.GET and request.GET['metric']:
            metric = request.GET['metric']
        cv_fold = 3
        if 'cv_fold' in request.GET and request.GET['cv_fold']:
            cv_fold = int(request.GET['cv_fold'])
        scores = predict_model(alg, metric, cv_fold)
        return render(request, 'upload_file.html', {
            'metric': metric,
            'scores': scores
        })
    return render(request, 'upload_file.html')

def predict_model(algorithm, metric, cv_fold):
    X = pd.read_csv(settings.MEDIA_ROOT + '/input_data.csv')
    X = X.iloc[:, 1:]
    Y = pd.read_csv(settings.MEDIA_ROOT + '\\' + settings.LABEL_FILE_NAME)
    Y = Y.iloc[:, 1:]
    X = X.astype('int32', copy=False)
    Y = Y.astype('int32', copy=False)
    if algorithm == 'decision_tree':
        clf = tree.DecisionTreeClassifier()
        scores = cross_val_score(clf, X, Y, cv=cv_fold, scoring=metric)
    if algorithm == 'random_forest':
        clf = RandomForestClassifier()
        scores = cross_val_score(clf, X, Y, cv=cv_fold, scoring=metric)
    if algorithm == 'SVM':
        clf = svm.SVC()
        scores = cross_val_score(clf, X, Y, cv=cv_fold, scoring=metric)
    if algorithm == 'DNN':
        scores = [0, 0, 0]
    return list(scores)

