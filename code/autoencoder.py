# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from image_process import SplitImage
from image_statistics import *
from network_testing import *
from network_training import NetworkTraining
from configurations import *
import convert_to_png

def autoencoder(network_type, train, test, statistics):
    # convert_to_png.raw_to_png(paths.pngDir, paths.pngOutDir, 1280, 720)
    network_config = NetworkConfig(train=train, test=test, statistics=statistics, network_type=network_type)
    train_config = TrainConfig(network_config)
    test_config = TestConfig(network_config)
    statistics_config = StatisticsConfig(network_config)

    image_processing = SplitImage(network_config, train_config, test_config)
    network_train = NetworkTraining(train_config, image_processing)
    network_test = NetworkTesting(test_config, image_processing)
    statistics = Statistics(statistics_config, image_processing)

    if network_config.MASK_PURE_DATA:
        image_processing.mask_pure_images(train_config.get_mask_pure_inputs())
        network_config.imgdir_pure = network_config.masked_pure

    if network_config.CROP_DATA:
        print('Cropping training data ..')
        image_processing.get_split_img(train_config.get_train_data_inputs("ir"), True)
        image_processing.get_split_img(train_config.get_train_data_inputs("pure"), False)
        image_processing.get_split_img(train_config.get_train_data_inputs("noisy"), False)


    if network_config.TRAIN_DATA:
        network_train.train()

    if network_config.TEST_DATA:
        network_test.test()

    if network_config.DIFF_DATA:
        statistics.calc_diff()


if __name__ == '__main__':
    BASIC = 0
    UNET = 1
    CCGAN = 2

    train = 1
    test = 0
    statistics = 0

    autoencoder(UNET, train, test, statistics)

