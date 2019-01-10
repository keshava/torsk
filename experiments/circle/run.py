import sys
import logging
import numpy as np
import matplotlib.pyplot as plt

import torsk
from torsk.data.utils import gauss2d_sequence, mackey_sequence
from torsk.visualize import animate_double_imshow



def update_params(params,args):
    for i in range(0,len(args),2):
        key,value = args[i],args[i+1];
        params.dict[key] = eval(value)


params = torsk.Params()
params.input_map_specs = [
    # {"type": "pixels", "size": [20, 20], "input_scale": 4.},
    # {"type": "conv", "size": [10, 10], "kernel_type":"random", "input_scale": 1.},
    # {"type": "conv", "size": [10, 10], "kernel_type":"random", "input_scale": 1.},
    # {"type": "conv", "size": [10, 10], "kernel_type":"random", "input_scale": 1.},
    # {"type": "conv", "size": [10, 10], "kernel_type":"random", "input_scale": 1.},
    # {"type": "conv", "size": [10, 10], "kernel_type":"random", "input_scale": 1.},
    # {"type": "conv", "size": [10, 10], "kernel_type":"random", "input_scale": 1.},
    # {"type": "conv", "size": [10, 10], "kernel_type":"random", "input_scale": 1.},
    # {"type": "conv", "size": [10, 10], "kernel_type":"random", "input_scale": 1.},
    # {"type": "conv", "size": [5, 5], "kernel_type":"gauss", "input_scale": 9.},
    # {"type": "conv", "size": [5, 5], "kernel_type":"mean", "input_scale": 9.},
    # {"type": "dct", "size": [20, 20], "input_scale": 1.},
    {"type": "random_weights", "size": [1000], "weight_scale": 0.125}
]

params.spectral_radius = 2.0
params.density = 0.01
params.input_shape = [30, 30]
params.train_length = 2000
params.pred_length = 300
params.transient_length = 200
params.dtype = "float64"
params.reservoir_representation = "sparse"
params.backend = "numpy"
params.train_method = "pinv"
params.tikhonov_beta = 0.01
params.debug = True

update_params(params,sys.argv[1:]);

logger = logging.getLogger(__file__)
level = "DEBUG" if params.debug else "INFO"
logging.basicConfig(level=level)
logging.getLogger("matplotlib").setLevel("INFO")

if params.backend == "numpy":
    logger.info("Running with NUMPY backend")
    from torsk.data.numpy_dataset import NumpyImageDataset as ImageDataset
    from torsk.models.numpy_esn import NumpyESN as ESN
else:
    logger.info("Running with TORCH backend")
    from torsk.data.torch_dataset import TorchImageDataset as ImageDataset
    from torsk.models.torch_esn import TorchESN as ESN

logger.info(params)

logger.info("Creating circle dataset ...")
t = np.arange(0, 200*np.pi, 0.1)
# x, y = np.sin(0.3 * t), np.cos(t)
x, y = np.sin(t), np.cos(0.3 * t)
# y = mackey_sequence(N=t.shape[0]) * 2 - 1
center = np.array([y, x]).T
images = gauss2d_sequence(center, sigma=0.5, size=params.input_shape)
dataset = ImageDataset(images, params)

logger.info("Building model ...")
model = ESN(params)

# features = model.esn_cell.input_map(images[0])
# dim = int(features.shape[0]**.5)
# shape = [dim, dim]
# plt.imshow(features.reshape(shape))
# plt.show()

logger.info("Training + predicting ...")
model, outputs, pred_labels = torsk.train_predict_esn(model, dataset)

logger.info("Visualizing results ...")

# weight = model.esn_cell.weight_hh._values().numpy()
# hist, bins = np.histogram(weight, bins=100)
# plt.plot(bins[1:], hist)
# plt.show()

# real_pixels      = dataset.to_images(pred_labels)
# predicted_pixels = dataset.to_images(outputs)
if params.backend == "torch":
    real_pixels = pred_labels.squeeze().numpy()
    predicted_pixels = outputs.squeeze().numpy()
else:
    real_pixels = pred_labels
    predicted_pixels = outputs

y, x = 5, 5
plt.plot(real_pixels[:, y, x])
plt.plot(predicted_pixels[:, y, x])
plt.show()

anim = animate_double_imshow(real_pixels,predicted_pixels)
plt.show()

