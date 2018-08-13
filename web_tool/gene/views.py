from django.shortcuts import render
from django.shortcuts import render_to_response
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from gene.models import CisEqtl, DrugList
from django.db.models import Q

def home(request):
    return render(request, 'home.html')

def eqtl_search(request):
    if ('gene' in request.GET and request.GET['gene']) or ('snpid' in request.GET and request.GET['snpid']):
        cancertype = request.GET['cancertype']
        eqtls = CisEqtl.objects.all()
        if cancertype != 'ALL':
            eqtls = eqtls.filter(cancer_type=cancertype)
        if 'snpid' in request.GET and request.GET['snpid']:
            id = request.GET['snpid']
            eqtls = eqtls.filter(eqtls=id)
        if 'gene' in request.GET and request.GET['gene']:
            gene = request.GET['gene']
            eqtls = eqtls.filter(egenes__icontains=gene)
        gene = request.GET['gene']
        if eqtls:
            limit = 50
            paginator = Paginator(eqtls.values(), limit)
            page = request.GET.get('page', '1')
            res = paginator.page(page)
            return render(request, 'eqtl_result.html', {'cancertype': cancertype, 'gene': gene, 'eqtls': res})
        else:
            return HttpResponseRedirect("/gene/")
    else:
        return HttpResponseRedirect("/gene/")

def drug(request):
    list = DrugList.objects.all()
    limit = 20
    paginator = Paginator(list.values(), limit)
    page = request.GET.get('page', '1')
    res = paginator.page(page)
    return render(request, 'drug.html', {'list': res})

def drug_search(request):
    if ('gene' in request.GET and request.GET['gene']) or ('name' in request.GET and request.GET['name']):
        drug = DrugList.objects.all()
        if 'name' in request.GET and request.GET['name']:
            name = request.GET['name']
            drug = drug.filter(Q(name__icontains=name) | Q(synonyms__icontains=name))
        if 'gene' in request.GET and request.GET['gene']:
            gene = request.GET['gene']
            drug = drug.filter(targets__icontains=gene)
        if drug:
            return render(request, 'drug_result.html', {'drugs': drug})
        else:
            return HttpResponseRedirect("/gene/drug/")
    else:
        return HttpResponseRedirect("/gene/drug/")

def show_gene_list(request):
    gene = CisEqtl.objects.only("egenes")
    gene_list = []
    for i in gene:
        gene_list.append(i)
    gene_list = list(set(gene_list))
    print(len(gene_list))
    return render(request, 'gene_list.html', {'gene': gene})


