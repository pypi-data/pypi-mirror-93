# Researcher

"I walk slowly, but I never walk backward."
    - Abraham Lincon

Researcher makes it easier for data science practitioners to record and reproduce the results of their data science experiments. Conceptually `researcher` breaks the data science process into distinct **experiments**. Each experiment has **parameters** (number of training epochs, dataset used, model architecture, etc.) which differentiate it from other experiments, and **results** (final validation loss, lowest training accuracy, etc.) which are the observations made when an experiment was run. 

The idea behind researcher is that for every experiment you run, you should record both the parameters involved and the results they achieved. This will make it easier to analyse complex interactions between different parameters and re-create experimental conditions at a later date.

## Usage

To see an example of how `researcher` in action, check out `mnist_demo.ipynb` on the [github repo](https://github.com/Lewington-pitsos/researcher), but essentially usage has 3 stages:

### 1. Define Experiment Parameters

In geneal for any data science project you will spend a great deal of your time choosing parameters for experiments. These parameters might include which activation functions to use, how many epochs to train for or which data augmentation procedures to use. Ideally every time you conduct an experiment, you should record the parameters which are involved in that experiment and those parameters should be sufficient for someone else to replicate that exact experiment at a later date. The approach favoured by `researcher` is to have a helper function which takes a dictionary of parameters, runs an experiment under those parameters, and returns the experiment results. Something like the following incomplete code snippet:

```python
import researcher as rs
import tensorflow as tf

def run_experiment(params):
    model = tf.keras.models.Sequential([
      tf.keras.layers.Flatten(input_shape=(28, 28, 1)),
      tf.keras.layers.Dense(params["depth"],activation=params["activation_function"]),
      tf.keras.layers.Dense(10, activation=params["final_activation"])
    ])
    model.compile(
        loss='sparse_categorical_crossentropy',
        optimizer=tf.keras.optimizers.Adam(params["lr"]),
        metrics=['accuracy'],
    )
    model.fit(
        SOME_DATASET,
        epochs=params["epochs"],
        validation_data=SOME_OTHER_DATASET, 
    )
    
    return model.history

params = {
    "activation_function": "relu",
    "final_activation": "softmax",
    "depth": 256,
    "epochs": 8,
    "lr": 0.001
}

results = run_experiment(params)
```
By varying `params` you can perform multiple experiments under different conditions. Good practice is to give each `params` dictionary a `"title"` key which summarizes the experiment and makes it easier to quickly identify experiments in future.

```python
params = {
    "title": "deep-adam-relu",
    "activation_function": "relu",
    "final_activation": "softmax",
    "depth": 256,
    "epochs": 8,
    "lr": 0.001
}

results = run_experiment(params)
```
### 2. Save Experiment Results

Data science experiments become much more useful when you record their results in a consistent format. Then if you discover anything important, you can easily share your discovery with others and keep track of it in a quantifiable form for your own future benefit. This is what `researcher` helps with. First create an empty directory to save all your experiment data:

`mkdir records`

Then, each time you run an experiment, simply pack the results into a dictionary and use `researcher` to save it in that directory, along with the experimental parameters.

```python
final_results = {}

for key, values in results.history.items():
    final_results[key] = values

rs.record_experiment(params, "records/", observations=final_results)
```

The parameters and results will be saved into a `.json` file in the `records/` directory and given a unique experiment hash that can later be used to identify it (though a `"title"` key is also helpful).

**Note**: because `researcher` serializes experiments using JSON, you cannot include any non json-serializable objects in `params` when using `researcher`.

### 3. Load and View Experiment Results

`researcher` also helps you load and visualize saved experiments:

```python
experiments = rs.all_experiments("records/")
```

Experiments are loaded into a `researcher.experiment.Experiment` instance, which is a light wrapper around the raw parameters and results that were saved initially:


```python
experiments[0].data

# {
# 'title': 'deep-adam-relu',
# 'activation_function': 'relu',
# 'final_activation': 'softmax',
# 'depth': 256,
# 'epochs': 8,
# 'lr': 0.001,
# 'hash': 'eebb49b9d1487396dd6c0e5271cc3083',
# 'timestamp': '2020-12-10_00:01:04',
# 'observations': {'loss': [0.35920432209968567,
#     0.16782893240451813,
#     0.12179006636142731,
#     0.09385494887828827,
#     0.07634902000427246],
# 'accuracy': [0.9017833471298218,
#     0.9524166584014893,
#     0.9652500152587891,
#     0.972683310508728,
#     0.9780666828155518],
# 'val_loss': [0.1982543170452118,
#     0.1372576504945755,
#     0.11536946892738342,
#     0.1035531759262085,
#     0.08903338760137558],
# 'val_accuracy': [0.9441999793052673,
#     0.9607999920845032,
#     0.9675999879837036,
#     0.9672999978065491,
#     0.9717000126838684]},
# }
```

You can also use some pre-built plotting functions to visualize these experimental results (see `researcher/dashboard.py`), but depending on what kinds of experiments you're running, you'll probably want to define your own.

```python
import matplotlib.pyplot as plt

def plot_metric(e, metric):
    plt.plot(e.data["observations"][metric])

plot_metric(experiments[0], "loss")
plot_metric(experiments[0], "val_loss")
```