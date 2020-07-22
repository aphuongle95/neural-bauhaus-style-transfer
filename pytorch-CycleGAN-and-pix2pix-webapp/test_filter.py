from options.test_options import TestOptions
from data import create_dataset
from models import create_model
from util.visualizer import save_images
from util import html
import sys
import os
import torch
import numpy as np
from util import util
import cv2
import base64
from PIL import Image 

class Makeup_artist(object):
    def __init__(self, dataset):
        self.opt = TestOptions().parse()  # get test self.options
        # hard-code some parameters for test
        self.opt.num_threads = 0   # test code only supports num_threads = 1
        self.opt.batch_size = 1    # test code only supports batch_size = 1
        self.opt.serial_batches = True  # disable data shuffling; comment self line if results on randomly chosen images are needed.
        self.opt.no_flip = True    # no flip; comment self line if results on flipped images are needed.
        self.opt.display_id = -1   # no visdom display; the test code saves the results to a HTML file.
        # added by Annie    
        self.opt.dataroot = "datasets/" + dataset
        self.opt.name = dataset
        self.opt.model = "test"
        self.opt.no_dropout = True
        print(self.opt)
        self.dataset = create_dataset(self.opt)  # create a dataset given self.opt.dataset_mode and other self.options
        self.model = create_model(self.opt)      # create a model given self.opt.model and other self.options
        self.model.setup(self.opt)               # regular setup: load and print networks; create schedulers
        
        if self.opt.eval:
            model.eval()
        print("here1")
        # self.data = next(iter(dataset), None)
        self.data = {
            "A": None,
            "A_paths": None
        }

        # webcam = VideoCapture(self.opt.videosource)
        # namedWindow("cam-input")
        # namedWindow("cam-output")

    def apply_makeup(self, input_image):

        print("here3")
        print("hello", self.data['A'])

        # input is pil image
        input_image1 = input_image.convert('RGB')
        # input_image2 = self.dataset.dataset.transform(input_image1)
        input_image2 = np.array(input_image1)
        input_image3 = np.asarray([input_image2])
        input_image4 = np.transpose(input_image3, (0, 3, 1, 2))
        self.data['A'] = torch.FloatTensor(input_image4)

        self.model.set_input(self.data)  # unpack data from data loader
        self.model.test()  # run inference

        # get output image
        im_data = self.model.fake.data 
        im = util.tensor2im(im_data)
        result_image = Image.fromarray(im)

        
        print("here2")  

        # k = cv2.waitKey(1)
        # if k == 27:
        #     break
          
        return result_image

        
    




    