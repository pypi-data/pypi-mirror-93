# EasyTensorBoard

```py
import tensorflow as tf
from easytensorboard import EasyTensorBoard

a = tf.constant(5.0, name="a")
b = tf.constant(6.0, name="b")
c = tf.add(a, b, name='c')

tb = EasyTensorBoard()
with tf.Session() as sess:
    tb.save(sess.graph)
tb.board()
```
