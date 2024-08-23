"""
Utilities:
    range_validator
    AverageMatterPlots
"""
import numpy as np
import matplotlib.pyplot as plt

def range_validator(variable, variable_name, lower_lim, upper_lim):
    """
    Validates if a variable is within a specified range.

    Args:
        variable: the variable object.
        variable_name (string) : name of the variable
        lower_lim (double) : the lower limit of the variable's range
        lower_lim (double) : the lower limit of the variable's range
    Raises:
        A Value error if the input is out of range
    Returns:
        None
    """
    if (variable < lower_lim or variable > upper_lim) :
        # later use isclose for such comparisons
        raise ValueError(variable_name +
                         " should be in the range [" +
                         str(lower_lim) +
                         ", " +
                         str(upper_lim) + "]"
                         )

class AverageMatterPlots:
    """
    A class for plotting averaged matter images

    Attributes:
        matter (qmf) : a quantum matter object
        imaging_type (string) : imaging type IN_TRAP or TIME_OF_FLIGHT
        extent_x (int) : +/- extent from center x of image to plot, rest is cropped
        extent_y (int) : +/- extent from center y of image to plot, rest is cropped
        title (string) : title for the plot
    """
    def __init__(self, matters, imaging_type, extent_x, extent_y, title):
        self.matters = matters
        self.imaging_type = imaging_type
        self.title = title
        self.extent_x = extent_x
        self.extent_y = extent_y

    def __average_matter_images__(self):
        """
        Averages the matter images input

        """
        if self.imaging_type == "IN_TRAP":
            rows = self.matters[0].output.it_plot.rows
            columns = self.matters[0].output.it_plot.columns
        else:
            rows = self.matters[0].output.tof_image.rows
            columns = self.matters[0].output.tof_image.columns
        pixcal = self.matters[0].output.get_image_pixcal(image=self.imaging_type)
        avg_pixels = np.zeros((rows, columns))
        avg_slice = np.zeros(columns)
        for matter in self.matters:
            avg_pixels += matter.output.get_image_data(image=self.imaging_type)
            avg_slice += matter.output.get_image_data(image=self.imaging_type)[int(rows / 2)]
        num_runs = len(self.matters)
        avg_pixels /= num_runs
        avg_slice /= num_runs
        x_pos = np.arange(-columns / 2 * pixcal, columns / 2 * pixcal, pixcal)
        y_pos = np.arange(-rows / 2 * pixcal, rows / 2 * pixcal, pixcal)

        return avg_pixels, avg_slice, pixcal, x_pos, y_pos

    def plot(self):
        """
        Plots the average image and its slice

        """
        avg_pixels, avg_slice, pixcal, x_pos, y_pos = self.__average_matter_images__()
        fig, axs = plt.subplots(nrows=2, sharex=True)
        fig.suptitle(self.title)
        lox = int(len(x_pos)/2-(self.extent_x/pixcal))
        hix = int(len(x_pos)/2+(self.extent_x/pixcal))
        loy = int(len(y_pos)/2-(self.extent_y/pixcal))
        hiy = int(len(y_pos)/2+(self.extent_y/pixcal))
        im = axs[0].imshow(avg_pixels[loy:hiy, lox:hix],
                            extent=[x_pos[lox], x_pos[hix],
                                    y_pos[loy], y_pos[hiy]],
                    )
        cbaxes = fig.add_axes([1., 0.65, 0.01, 0.16])
        plt.colorbar(im, cax=cbaxes, ticks=[0.0, 1], orientation="vertical")
        cbaxes.tick_params(color="black", labelcolor="black")
        axs[1].plot(x_pos[lox:hix], avg_slice[lox:hix], label="Slice @ Y=0")
        axs[1].set_ylabel("Optical Depth")
        axs[1].set_yticks([0, 0.5, 1])
        axs[1].set_xlabel("X position ($\mu$m)")
        axs[1].legend()
        axs[0].set_ylabel("Y position ($\mu$m)")
        plt.subplots_adjust(hspace=0)
        plt.show()
