# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template import loader

import os

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from au import getResponse, cylc_run_dir
from job import Job

def register(request):
    template = loader.get_template('register.html')
    return HttpResponse(template.render())

def suites(request):
    dirs_with_suite = list()
    dirs = os.listdir(cylc_run_dir())
    for direc in dirs:
        path = os.path.join(cylc_run_dir(),direc, "suite.rc")
        if os.path.isfile(path):
            dirs_with_suite.append(direc)
    context = {
        "suites": dirs_with_suite 
    }
    template = loader.get_template('suites.html')
    return HttpResponse(template.render(context, request))
    
def suite_view(request, suitename=''):
    data = getResponse(suitename)
    dataset = []
    dataOrder = ["name", "label", "latest_message","host","batch_sys_name","submit_method_id","submitted_time_string","started_time_string","finished_time_string","mean_elapsed_time"]
    if(data == None):
        template = loader.get_template('suite_view.html')
        return HttpResponse(template.render(request) )
    else:
        for job in data:
            job = job.as_dict()
        dataset = data
        
    context = {
        'dataOrderKey' : dataOrder,
        'data' : dataset,
        'suite' : suitename
    }
    template = loader.get_template('suite_view.html')
    return HttpResponse(template.render(context, request) )
