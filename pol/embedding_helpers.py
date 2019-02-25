from gensim.models import KeyedVectors, Word2Vec

from .preprocessing import to_sentences

def fine_tune(load_path, documents):
  sentences = to_sentences(documents)
  model = Word2Vec(sentences, size=100, window=5, min_count=1, workers=4)
  model.train()
  return model.wv
