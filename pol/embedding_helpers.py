from gensim.models import KeyedVectors, Word2Vec

from .preprocessing import to_sentences

def fine_tune(nlp, load_path, documents):
  sentences = to_sentences(nlp, documents)
  model = Word2Vec(sentences, size=100, window=5, min_count=1, workers=4)
  model.train()
  return model.wv

def train(nlp, documents):
  sentences = to_sentences(nlp, documents)
  model = Word2Vec(sentences, size=100, window=5, min_count=1, workers=4)
  model.train()
  return model.wv
