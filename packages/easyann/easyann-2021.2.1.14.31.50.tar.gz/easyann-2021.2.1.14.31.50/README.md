<h1 align = "center">:rocket: ANN :facepunch:</h1>

---

# Install
`pip install fast-ann`

# Usage
```python
from ann import ANN
import numpy as np

data = np.random.random((1000, 128)).astype('float32')

ann = ANN()
ann.train(data, index_factory='IVF4000, Flat', noramlize=True)

dis, idx = ann.search(data[:10])

print(dis)
print(idx)
```
---
- faiss不同量级对应的训练时间及内存测试
- 压缩方式测试
- 四种组合：默认是查向量返回 distance与index
    - id => id/vector
    - vector => id/vector
    - push场景需要 docid => title_vector => docid
    
- 线上服务
    - id2word
    - id2vector