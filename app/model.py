import torch
from app import app

class Model(object):
    def __init__(self, tokenizer, model):
       self.tokenizer = tokenizer
       self.model = model
    
    def encode(self, text):
        chunksize = 384

        # Tokenize sentences
        tokens = self.tokenizer.encode_plus(text, add_special_tokens=False, return_tensors='pt')

        '''#add bos_token (<sep>) token once at the beginning of sentence (<sep> = 0)
        tokens['input_ids'] = torch.unsqueeze(torch.cat([torch.tensor([0]), tokens['input_ids'][0]]), 0)
        tokens['attention_mask'] = torch.unsqueeze(torch.cat([torch.tensor([0]), tokens['attention_mask'][0]]), 0)
'''
        input_id_chunks = list(tokens['input_ids'][0].split(chunksize - 2))
        mask_chunks = list(tokens['attention_mask'][0].split(chunksize - 2))

      
        '''
        We add bos_token (<s>) token only once to indicate the start of the sequence.
        We add sep_token (</s>) which is used when building a sequence from multiple sequences. 
        The token is added as an input_id before and after the sentence has been tokenized. 
        MPNet tokenizer maps </s> token as </s> = 2 and <pad> token as <pad> = 1
        '''

        # loop through each chunk
        for i in range(len(input_id_chunks)):
          if i == 0:
            # add bos_token once at the beginning of sentence (<sep> = 0)
            input_id_chunks[i] = torch.cat([torch.tensor([0]), input_id_chunks[i], torch.tensor([2])])
            # add attention token to attention_mask
            mask_chunks[i] = torch.cat([torch.tensor([1]), mask_chunks[i], torch.tensor([1])])
          else:
            # add </sep> token to input IDs
            input_id_chunks[i] = torch.cat([torch.tensor([2]), input_id_chunks[i], torch.tensor([2])])
            # add attention tokens to attention mask
            mask_chunks[i] = torch.cat([torch.tensor([1]), mask_chunks[i], torch.tensor([1])])
          # get required padding length
          pad_len = chunksize - input_id_chunks[i].shape[0]
          # check if tensor length satisfies required chunk size
          if pad_len > 0:
              # if padding length is more than 0, we must add padding
              input_id_chunks[i] = torch.cat([input_id_chunks[i], torch.Tensor([1] * pad_len)])
              mask_chunks[i] = torch.cat([mask_chunks[i], torch.Tensor([0] * pad_len)])

        input_ids = torch.stack(input_id_chunks)
        attention_mask = torch.stack(mask_chunks)

        input_dict = {'input_ids': input_ids.long(), 'attention_mask': attention_mask.int()}
        return input_dict

    def get_embeddings(self, input_dict):

        with torch.no_grad():
            model_output = self.model(**input_dict)

            # Mean pooling - take attention mask into account for correct averaging

            # First element of model_output contains all token embeddings
            token_embeddings = model_output[0]

            input_mask_expanded = input_dict['attention_mask'].unsqueeze(-1).expand(token_embeddings.size()).float()
            sentence_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
            sentence_embeddings = torch.nn.functional.normalize(sentence_embeddings, p=2, dim=1)
            return sentence_embeddings