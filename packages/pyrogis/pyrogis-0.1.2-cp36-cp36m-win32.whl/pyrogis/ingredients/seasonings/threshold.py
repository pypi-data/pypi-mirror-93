import numpy as np

from rpierogis import recipes
from .seasoning import Seasoning


class Threshold(Seasoning):
    """
    A seasoning that compares the average value (intesity) of each pixel in the :param target pixel array.
    When used in a mix, the threshold will target the pixel array below it if it has not been initialized with target.

    As it is a subclass of seasoning, a Threshold instance can use season method and work with or without a target
    """

    LOWER_THRESHOLD = 64
    UPPER_THRESHOLD = 180

    def prep(self, lower_threshold: int = LOWER_THRESHOLD, upper_threshold: int = UPPER_THRESHOLD, **kwargs):
        """
        Set the threshold intensity levels
        Pixels lower than :param lower_threshold or higher that :param upper_threshold are true (include_pixel)
        """
        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold

        # set include/exclude_pixel and target, if provided
        super().prep(**kwargs)

    def cook(self, pixels: np.ndarray):
        """
        Pixels with brightness >= upper_threshold or <= lower_threshold are replaced by include pixel
        brightness = r * 0.299 + g * 0.587 + b * 0.114

        Parallel computation in rust is 10x speedup
        """

        if self.target is not None:
            pixels = self.target.pixels

        cooked_pixels = pixels.copy()

        # cook using the rust function
        cooked_pixels = recipes.threshold(
            cooked_pixels.astype(np.dtype('uint8')),
            self.lower_threshold, self.upper_threshold,
            self.include_pixel, self.exclude_pixel
        )

        return cooked_pixels

    def cook_np(self, pixels: np.ndarray):
        """
        Perform the same operation as cook, but only in numpy
        """

        include_pixels = np.resize(self.include_pixel, pixels.shape)
        exclude_pixels = np.resize(self.exclude_pixel, pixels.shape)

        # use target, if available
        target_pixels = pixels
        if self.target is not None:
            target_pixels = self.target.pixels

        # use exclude_pixels as the base
        cooked_pixels = exclude_pixels
        # get intensities from average of rgb
        intensities_array = np.sum(target_pixels * np.asarray([0.299, 0.587, 0.114]), axis=2)
        # if intensity <= lower or >= upper, True
        boolean_array = np.logical_or(intensities_array >= self.upper_threshold,
                                      intensities_array <= self.lower_threshold)

        # set True values in boolean_array to include_pixel
        cooked_pixels[boolean_array] = include_pixels[boolean_array]

        return cooked_pixels

    @classmethod
    def add_parser_arguments(cls, parser):
        parser.add_argument('-l', '--lower-threshold', default=Threshold.LOWER_THRESHOLD, type=int,
                            help='Pixels with lightness below this threshold will not get sorted')
        parser.add_argument('-u', '--upper-threshold', default=Threshold.UPPER_THRESHOLD, type=int,
                            help='Pixels with lightness above this threshold will not get sorted')
