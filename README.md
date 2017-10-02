# GPU Accelerated K-means

## 既存のkmeansは遅すぎる
CPUでやった場合のkmeansはscikit-learnなどを使えるのですが、いかんせん遅すぎるのと、kmeansの多くは距離の定義がEuclidであって、word2vecなどのベクトル情報をクラスタリングする際には、あまり速度が出ません  
また、実際に、kmeansの学習ステップを見るとほとんどのクラスが安定しているのに、更新が止まるまで繰り返してしまうので、かなり遅いです。　　

十分な精度やイテレーションを繰り返した上で、停止できるように設計します  

## Cupy
Cupyはchainerのバックエンドで用いられているnumpyの一部語感ライブラリであり、cupyはこの行列の計算をGPUで行うことができます。　　
numpyの機能で高機能のものは、まだ使えない面も多いですが、最初にnumpy, cupy双方コンパチブルに動作させるようなことができる場合、CPUで計算させたほうがいい場合、
GPUで計算させたほうがいい場合、双方の最適なコードを記述することができます　

四則演算と、ノルムと、dot積などよく使う系のオペレーションを入れてみました  
```python
import numpy as np
import cupy as cp

xp = np
if '--gpu' in sys.argv:
  xp = cp
  
xp.random.randn((10000, 10000))
```
### CPU(Ryzen 1700X)で実行
numpyもマルチプロセスで動作するので、Ryzenのような多コアで計算すると、高速に計算することが期待できます　　

```cosnole
$ python3 bench.py --cpu
now iter 0
now iter 1
now iter 2
now iter 3
now iter 4
now iter 5
now iter 6
now iter 7
now iter 8
now iter 9
elapsed 304.03318667411804
```
