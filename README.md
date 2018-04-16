# Transliterator

## Requirements
``Python 2.7`` and ``PyTorch`` (http://pytorch.org/).

The model is implemented and tested on PyTorch version 0.3.1 (http://pytorch.org/docs/0.3.1/).

### Hardware Requirements
The model is fast on a GPU unit with CUDA + cuDNN deep learning libraries.

## Running Configurations
All configurations are manually set via the ``config.py`` file.

## Training Instructions
```python tl.py train <path to save model>```

### Example:
```sh
> mkdir ./saved_models
> python tl.py train ./saved_models/
```

## Testing Instructions
```python tl.py test <path to restore model> <input file path> <output file path>```

### Example:
```sh
> python tl.py test ./saved_models/ ./data/dev.raw ./saved_models/dev.predicted
> python tl.py test ./saved_models/ ./data/test.raw ./saved_models/test.predicted
```

## License
MIT license.
