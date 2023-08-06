import numpy as np
import tensorflow as tf
from tensorflow.python.client import device_lib

from montblanc.impl.rime.tensorflow import load_tf_lib
mod = load_tf_lib()

stokes = np.broadcast_to(np.float64([0, 1, 1, 0]), (1, 1, 1, 4))
tf_stokes = tf.Variable(stokes)
result = mod.b_sqrt(tf_stokes, CT=np.complex128,
                    polarisation_type='circular')


init_op = tf.global_variables_initializer()

with tf.Session() as S:
    S.run(init_op)

    chol, sgn = S.run(result)

    chol = chol.reshape(2, 2)

    B = sgn*np.dot(chol, chol)

    print("Stokes", stokes)
    print("brightness", B)
