import spacy

from pol.cache_helpers import read_cache
from pol.fetchers import extract_documents, get_votes_by_bill, get_leg_id_to_pol_id, get_pol_names
from pol.preprocessing import flag_docs, to_sentences, get_pol_name_to_flag
from pol.embedding_helpers import train

def main():
  nlp: spacy.language.Language = spacy.load('en')
  documents, doc_ids_by_pol_id = read_cache('documents.json', extract_documents)
  leg_id_to_pol_id = get_leg_id_to_pol_id()
  votes_by_bill = get_votes_by_bill(leg_id_to_pol_id)
  pol_names = get_pol_names()
  pol_name_to_flag = get_pol_name_to_flag(pol_names)
  flagged_docs = read_cache('flagged_docs.json', lambda: flag_docs(nlp,
                                                                   documents,
                                                                   pol_name_to_flag,
                                                                   pol_names))
  flagged_sentences = read_cache('flagged_sentences.json', lambda: to_sentences(nlp, flagged_docs))
  embeddings = train(nlp, documents)
  embeddings.wv.save('caches/trained.kv')


if __name__ == "__main__":
  import ipdb
  import traceback
  import sys
  try:
    main()
  except: # pylint: disable=bare-except
    extype, value, tb = sys.exc_info()
    traceback.print_exc()
    ipdb.post_mortem(tb)
