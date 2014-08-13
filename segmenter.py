#!/usr/bin/env python

__author__ = "Oriol Nieto"
__copyright__ = "Copyright 2014, Music and Audio Research Lab (MARL)"
__license__ = "GPL"
__version__ = "1.0"
__email__ = "oriol@nyu.edu"

import argparse
import logging
import numpy as np
import time
import features
import pylab as plt
import utils


def process(audio_path, output_path):
    """Main process to segment the audio file and save the results in the
        specified output."""

    # Get features and stack them
    feats = features.compute_all_features(audio_path, audio_beats)
    F = np.hstack((feats["hpcp"], feats["mfcc"], feats["tonnetz"]))
    F = utils.median_filter(F, M=4)

    #plt.imshow(feats["mfcc"].T, interpolation="nearest", aspect="auto")
    #plt.imshow(feats["hpcp"].T, interpolation="nearest", aspect="auto")
    #plt.show()

    S = utils.compute_ssm(F)
    #S = utils.compute_ssm(feats["tonnetz"])
    plt.imshow(S, interpolation="nearest")
    plt.show()


def main():
    """Main function to parse the arguments and call the main process."""
    parser = argparse.ArgumentParser(description=
        "Segments the given audio file sampled at 44100, 16 bits, mono.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("audio_path",
                        action="store",
                        help="Path to the input audio file")
    parser.add_argument("-o",
                        action="store",
                        dest="output_path",
                        help="Path to the output results file",
                        default="output.txt")
    args = parser.parse_args()
    start_time = time.time()

    # Setup the logger
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s',
        level=logging.INFO)

    # Run the algorithm
    process(args.audio_path, args.output_path)

    # Done!
    logging.info("Done! Took %.2f seconds." % (time.time() - start_time))

if __name__ == '__main__':
    main()
