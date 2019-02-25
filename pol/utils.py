import torch
import torch.nn as nn
import random
from difflib import SequenceMatcher

import pydash as _

def append_at(obj, key, val):
  if key in obj:
    obj[key].append(val)
  else:
    obj[key] = [val]

def dont_update(module):
  for p in module.parameters():
    p.requires_grad = False

def name(path, notes):
  ext = '.json' if '.json' in path else '.pkl'
  if len(notes) == 0: return path
  path_segs = path.split(ext)
  return '_'.join([path_segs[0]] + notes) + ext

def do_update(module):
  for p in module.parameters():
    p.requires_grad = True

class Identity(nn.Module):
  def forward(self, x): return x

def at_least_one_dim(tensor):
  if len(tensor.shape) == 0:
    return tensor.unsqueeze(0)
  else:
    return tensor

def to_list(coll):
  if isinstance(coll, torch.Tensor):
    return coll.tolist()
  else:
    return list(coll)

def maybe(val, default): return val if val is not None else default

def sim(str1, str2): return SequenceMatcher(None, str1, str2).ratio()
