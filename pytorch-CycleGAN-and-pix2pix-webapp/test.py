import os
from options.test_options import TestOptions
from data import create_dataset
from models import create_model
from util.visualizer import save_images
from util import html
import sys

def main(dataset):
    print(dataset)
    opt = TestOptions().parse()  # get test options
    # hard-code some parameters for test
    opt.num_threads = 0   # test code only supports num_threads = 1
    opt.batch_size = 1    # test code only supports batch_size = 1
    opt.serial_batches = True  # disable data shuffling; comment this line if results on randomly chosen images are needed.
    opt.no_flip = True    # no flip; comment this line if results on flipped images are needed.
    opt.display_id = -1   # no visdom display; the test code saves the results to a HTML file.
    # added by Annie    
    opt.dataroot = "datasets/" + dataset
    opt.name = dataset
    opt.model = "test"
    opt.no_dropout = True
    if dataset=="demo_architecture2bau_1":
        opt.model = "cycle_gan"
        opt.direction = "AtoB" 
        opt.batch_size = 1 
        opt.norm = "batch"
    if dataset=="demo_architecture2bau_2":
        opt.model = "cycle_gan"
        opt.direction = "AtoB" 
        opt.norm = "batch"
    if dataset=="demo_architecture2bau_4":
        opt.model = "change"
        opt.direction = "BtoA" 
        opt.no_flip = False
        opt.no_dropout = False
        opt.norm = "batch"
    if dataset in ["demo_gothic2bau", "demo_bau2photo", "demo_romanic2bau"]:
        opt.no_flip = False
        opt.norm = "batch"
    if dataset in ["demo_renaissance2bau"]:
        opt.no_flip = False
    
    dataset = create_dataset(opt)  # create a dataset given opt.dataset_mode and other options
    model = create_model(opt)      # create a model given opt.model and other options
    model.setup(opt)               # regular setup: load and print networks; create schedulers
    # create a website
    web_dir = os.path.join("/media/project/adf39e9c-fcfe-4e8b-bcfc-5c33283d4bce/pytorch-CycleGAN-and-pix2pix/", opt.results_dir, opt.name, '{}_{}'.format(opt.phase, opt.epoch))  # define the website directory
    if opt.load_iter > 0:  # load_iter is 0 by default
        web_dir = '{:s}_iter{:d}'.format(web_dir, opt.load_iter)
    print('creating web directory', web_dir)
    webpage = html.HTML(web_dir, 'Experiment = %s, Phase = %s, Epoch = %s' % (opt.name, opt.phase, opt.epoch))
    # test with eval mode. This only affects layers like batchnorm and dropout.
    # For [pix2pix]: we use batchnorm and dropout in the original pix2pix. You can experiment it with and without eval() mode.
    # For [CycleGAN]: It should not affect CycleGAN as CycleGAN uses instancenorm without dropout.
    if opt.eval:
        model.eval()
    for i, data in enumerate(dataset):
        if i >= opt.num_test:  # only apply our model to opt.num_test images.
            break
        model.set_input(data)  # unpack data from data loader
        model.test()           # run inference
        visuals = model.get_current_visuals()  # get image results
        img_path = model.get_image_paths()     # get image paths
        if i % 5 == 0:  # save images to an HTML file
            print('processing (%04d)-th image... %s' % (i, img_path))
        save_images(webpage, visuals, img_path, aspect_ratio=opt.aspect_ratio, width=opt.display_winsize)
    webpage.save()  # save the HTML

if __name__ == '__main__':
    main(sys.argv[1:])
