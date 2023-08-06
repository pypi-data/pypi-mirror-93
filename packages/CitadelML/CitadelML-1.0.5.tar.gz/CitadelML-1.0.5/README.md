# CitadelML

Upload and train machine learning models on a remote server.


## Setup
```
pip install citadelml
```

## Quick use

Create a tensorflow model, and then send it to the server.

```python
from citadelml import upload_model
import tensorflow as tf

model = tf.keras.models.Sequential([
    tf.keras.layers.experimental.preprocessing.Rescaling(1./255),
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10)
])

upload_model(
    server='http://localhost:5000',
    dataset='example_dataset',
    username='usernameGoesHere',
    password='passwordGoesHere',
    model=model,
    loss_function='tf.keras.losses.SparseCategoricalCrossentropy',
    optimizer='adam',
    n_epochs=5,
    seed=12345,
    split=0.2,
    batch_size=32,
    save_training_results=False
)
```
