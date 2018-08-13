from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import pandas as pd
import numpy as np

def DNN_predict(request):
    df = pd.read_csv(settings.MEDIA_ROOT + '\\' + 'drug_fingerprint_complete.csv')
    drugs = list(set(df.loc[:, 'DRUG_NAME']))
    drugs.sort()
    if request.method == 'POST':
        fs = FileSystemStorage()
        if 'mutation' in request.FILES and request.FILES['mutation']:
            settings.EXP_FLAG_PREDICT = False
            mutation = request.FILES['mutation']
            settings.MUT_FILE_NAME_PREDICT = fs.save(mutation.name, mutation)
            return render(request, 'DNN_model_predict.html', {
                'uploaded_status': 1, 'drugs': drugs})
    if request.method == 'GET' and 'file' in request.GET and request.GET['file'] == 'example':
        settings.EXP_FLAG_PREDICT = True
        settings.MUT_FILE_NAME_PREDICT = 'mutation_sample.csv'
        example_mut_file_url = settings.MEDIA_ROOT + '\\' + settings.MUT_FILE_NAME_PREDICT
        return render(request, 'DNN_model_predict.html', {
            'example_mut_file_url': example_mut_file_url, 'drugs': drugs})
    if request.method == 'GET' and 'drug' in request.GET and request.GET['drug']:
        IC50 = make_prediction(settings.MEDIA_ROOT + '\\' + settings.MUT_FILE_NAME_PREDICT, request.GET['drug'])
        return render(request, 'DNN_model_predict.html', {
            'IC50': IC50, 'drugs': drugs, 'selected_drug': request.GET['drug']})
    return render(request, 'DNN_model_predict.html', {'drugs': drugs})

def make_prediction(filename, drugname):
    cell_matrix = pd.read_csv(filename)
    #print(cell_matrix)
    #print("------------------------")

    drug = pd.read_csv(settings.MEDIA_ROOT + '/' + 'drug_fingerprint_complete.csv')
    #print('Drug fingerprint matrix')
    #print(drug.head())

    cell_matrix = cell_matrix.iloc[0:1, :]
    selected_drug = drug.loc[drug['DRUG_NAME'] == drugname].iloc[:, 2:]

    #print(selected_drug)

    y_pre = settings.DL_MODEL.predict([np.atleast_3d(cell_matrix), np.atleast_3d(selected_drug)])
    print('IC50:', y_pre[0][0])

    return y_pre[0][0]


