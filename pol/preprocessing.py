from typing import List, Dict
from operator import itemgetter
from re import sub

from .utils import sim

from spacy.language import Language
import pydash as _

def _match(vals, query, score_fn):
  max_idx, max_score = max(((i, score_fn(query, val))
                            for i, val in enumerate(vals)),
                           key=itemgetter(1))
  return vals[max_idx]

def flag_docs(nlp: Language,
              documents: List[str],
              pol_name_to_flag: Dict[str, str],
              pol_names: List[str]):
  flagged_docs = []
  for doc in documents:
    flagged = ''
    so_far = 0
    for entity in nlp(doc).ents:
      if entity.label_ != 'PERSON': continue
      flagged += doc[so_far : entity.start_char]
      flagged += pol_name_to_flag[_match(pol_names, entity.text, sim)]
      so_far = entity.end_char + 1
    flagged_docs.append(flagged)
  return flagged_docs

def to_sentences(nlp: Language, documents: List[str]):
  return [list(nlp(doc).sents) for doc in documents]

def get_pol_name_to_flag(pol_names: List[str]):
  def _pol_flag(pol_name): return sub('[^a-zA-Z]', '_', _.to_upper(pol_name)) + '_FLAG'
  return {name: _pol_flag(name) for name in pol_names}
