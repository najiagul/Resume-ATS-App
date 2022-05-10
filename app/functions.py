import json
from numpy import sort
import sortedcontainers
from app.preprocess import *
from app.utils import *
from app import app

def sort_resumes(model, files, job):
    
    resumes_text, job_text = batch_preprocess(files = files , job_file = job)
    
    # get embeddings for resumes
    resume_embeds = {}
    for key, resume in resumes_text.items():
        encoded = model.encode(resume)
        embeds = model.get_embeddings(encoded)
        resume_embeds[key] = embeds

    # read job path and get embeddings
    job_encoded = model.encode(job_text)
    job_embeds = model.get_embeddings(job_encoded)

    sorted_resumes = weighted_cosine_sim(resume_embeds, job_embeds)
    return sorted_resumes
