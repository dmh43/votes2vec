import pandas as pd
import pydash as _
from itertools import count
from collections import defaultdict

from typing import List, Dict, Set, Tuple
import json

def get_votes_by_bill(state_votes_path='./data/statehvotes.json') -> Dict[str, Dict[str, Set[int]]]:
  def _split_for_against_abstain(bill_info):
    leg_ids_to_votes = bill_info['votes']
    vote_for, vote_against, vote_abstain = set(), set(), set()
    for leg_id, vote in leg_ids_to_votes.items():
      if vote == 'yes': vote_for.add(leg_id)
      elif vote == 'no': vote_against.add(leg_id)
      elif vote == 'other': vote_abstain.add(leg_id)
    return {'for': vote_for, 'against': vote_against, 'abstain': vote_abstain}
  votes = json.load(state_votes_path)
  return _.map_values(votes, _split_for_against_abstain)

def extract_documents(article_dir_path='data/article_jsons/') -> Tuple[List[str], Dict[int, List[int]]]:
  documents: List[str] = []
  doc_ids_by_pol_id: Dict[int, List[int]] = defaultdict(list)
  for pol_id in count(1):
    try:
      with open(article_dir_path + f'pol{pol_id}.json') as fh:
        doc_infos = json.load(fh)
        doc_ids_by_pol_id[pol_id].extend(len(documents) + i for i in range(len(doc_infos)))
        documents.extend(doc_info['title'] + ' ' + doc_info['text'] for doc_info in doc_infos)
    except FileNotFoundError:
      break
  return documents, dict(doc_ids_by_pol_id)

def get_leg_id_to_pol_id(lookup_path='comp_ling_politicians_sorted_with_globals_and_meta.csv') -> Dict[str, int]:
  return dict(pd.read_csv(lookup_path)[['leg_id', 'pol_id']].tolist())

def get_pol_names(lookup_path='comp_ling_politicians_sorted_with_globals_and_meta.csv') -> List[str]:
  return pd.read_csv(lookup_path).names.tolist()
