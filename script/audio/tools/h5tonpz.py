import os
import numpy as np
import h5py
from tempfile import TemporaryFile


if __name__ == "__main__":
    layers = (
        'conv1_1', 'relu1_1', 'conv1_2', 'relu1_2', 'pool1',

        'conv2_1', 'relu2_1', 'conv2_2', 'relu2_2', 'pool2',

        'conv3_1', 'relu3_1', 'conv3_2', 'relu3_2', 'conv3_3',
        'relu3_3', 'conv3_4', 'relu3_4', 'pool3',

        'conv4_1', 'relu4_1', 'conv4_2', 'relu4_2', 'conv4_3',
        'relu4_3', 'pool4',

        'conv5_1', 'relu5_1', 'conv5_2', 'relu5_2', 'conv5_3',
        'relu5_3', 'pool5',
        'fc6', 'fc7', 'fc8'
    )
    f = h5py.File('cifar10-vgg16_model.h5', mode='r')
    print(f.keys())
    weights = f['model_weights']
    weights_dict = {}
    print(weights.keys())
    if hasattr(weights, 'keys'):
        weights_keys = weights.keys()
        # print("weights_keys", weights_keys)
        for curr_layer in weights_keys:
            if hasattr(weights[curr_layer], 'keys'):
                curr_layer_keys = weights[curr_layer].keys()
                # print("curr_layer_keys", curr_layer_keys)
                for layer_data in curr_layer_keys:
                    if hasattr(weights[curr_layer][layer_data], 'keys'):
                        print(layer_data)
                    else:
                        weights_dict[curr_layer+layer_data] = weights[curr_layer][layer_data][:]
                        print(curr_layer+layer_data, weights[curr_layer][layer_data][:].shape)
            else:
                weights_dict[curr_layer] = weights[curr_layer][:]
                # print(curr_layer, weights[curr_layer][:].shape)
    else:
        print('weights has no key')
    print(weights_dict.keys())
    result_dict = {}
    result_dict['fc6_W'] = weights_dict['dense_1dense_1_W:0']
    result_dict['fc6_b'] = weights_dict['dense_1dense_1_b:0']
    result_dict['fc7_W'] = weights_dict['dense_2dense_2_W:0']
    result_dict['fc7_b'] = weights_dict['dense_2dense_2_b:0']
    np.save('fc.npz', result_dict)
    # weights = np.load('fc.npz')
    keys = sorted(result_dict.keys())
    for i, k in enumerate(keys):
        print(result_dict[k].shape)