import os
import sys
import math
import cupy as cp
import numpy as np
import pickle

# here is defines 
vector_size = 100
cluster_num = 200
max_iter = 12
input_file = './make_word_vector/index_meta.pkl'

index_meta = pickle.loads( open(input_file, 'rb').read() )

arrays = []
word_index = {}
index_word = {}
for index, meta in sorted(index_meta.items(), key=lambda x:x[0]):
  #print( index )
  arrays.append( meta['vec'] )
  word = meta['word']
  word_index[word] = index
  index_word[index] = word

x_all = cp.array(arrays) 
x_allnorm = cp.linalg.norm(x_all, axis=(1,) )

clusters = [cp.random.randn(vector_size) for n in range(cluster_num)] 
print( 'initial', clusters )

rams = None
for it in range(max_iter):
  cossimsall = []
  for e, cluster in enumerate(clusters):
    cluster_norm = cp.linalg.norm(cluster) 
    cluster_all = cluster * x_all
    norm = cluster_norm * x_allnorm
    invnorm = norm**-1 
    x_wa = (cluster * x_all).sum(axis=1) 
    cossims = x_wa * invnorm
    cossimsall.append( cossims )

  cossimsall = [ c.tolist() for c in cossimsall ]
  cc = np.array( cossimsall )
  ams = np.argmax(cc.T, axis=1)
  if rams is not None and np.array_equal(rams,ams):
    print( ams )
    break

  if rams is not None:
    print('differ', it, (ams - rams).tolist()[:200]) 
  print('now iter', it,  ams )
  print('old ams', it, rams )

  rams = ams

  # 重心の再計算
  am_vs = {}
  for e, am in enumerate(ams):
    #print(e, am) 
    if am_vs.get(am) is None:
      am_vs[am] = []
    am_vs[am].append( arrays[e] ) 

  means = []
  for am, vs in sorted(am_vs.items(), key=lambda x:x[0]):
    means.append( cp.mean(cp.array(vs), axis=0) )
  clusters = means

ams = [ (index, category) for index, category in enumerate(ams.tolist()) ]
import json
import copy

index_result = copy.copy( index_meta )
for index, category in ams:
  index_result[index]['category'] = category
  del index_result[index]['vec']

open('index_result.json', 'w').write( json.dumps( index_result, indent=2, ensure_ascii=False ) )
