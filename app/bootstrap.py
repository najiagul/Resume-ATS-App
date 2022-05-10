# Script to download MPNet Model from HuggingFace Hub

from transformers import (
   AutoModel, AutoTokenizer,
)
 
AutoModel.from_pretrained('sentence-transformers/all-mpnet-base-v2').save_pretrained('../model')
AutoTokenizer.from_pretrained('sentence-transformers/all-mpnet-base-v2', return_token_type_ids=True).save_pretrained('../model')