import torch
import numpy as np
def cos_sim(a, b):
  """
  Computes the cosine similarity cos_sim(a[i], b[j]) for all i and j.
  :return: Matrix with res[i][j]  = cos_sim(a[i], b[j])
  """
  if not isinstance(a, torch.Tensor):
    a = torch.tensor(a)

  if not isinstance(b, torch.Tensor):
    b = torch.tensor(b)

  if len(a.shape) == 1:
    a = a.unsqueeze(0)

  if len(b.shape) == 1:
    b = b.unsqueeze(0)

  a_norm = torch.nn.functional.normalize(a, p=2, dim=1)
  b_norm = torch.nn.functional.normalize(b, p=2, dim=1)
  return torch.mm(a_norm, b_norm.transpose(0, 1))

def weighted_average(similarity):
  """
  Performs a weighted average over the cosine similarity of a higher dimentional matrix
  """
  internal_average = np.sort(np.average(similarity, axis = 1))
  external_weights = np.arange(1, len(internal_average)+1)
  return np.average(internal_average, weights = external_weights)


def weighted_cosine_sim(resume_embeds, job_embeds):
    resume_similarity = {}
    for key, embeds in resume_embeds.items():
      similarity = cos_sim(embeds, job_embeds)
      resume_similarity[key] = weighted_average(similarity)

    sorted_resumes = dict(sorted(resume_similarity.items(), key=lambda x: x[1], reverse =True))
    return sorted_resumes
