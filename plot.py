import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import AutoMinorLocator


def plot_ecg(
    ecg: np.ndarray,
    sample_rate: int,
    title: str = '',
    bw: bool = True,
    columns: int = 2,
    row_height: int = 3,
    show_lead_name: bool = True,
    show_grid: bool = True,
    separate_columns: bool = False,
) -> None:
    """
    Plot a standard 12-lead ECG layout similar to a printed ECG:
    Left column: I, II, III, aVR, aVL, aVF
    Right column: V1, V2, V3, V4, V5, V6
    Scales: 25 mm/s horizontally, 1 cm/mV vertically.
    Each large square: 0.4 s horizontally, 1 mV vertically.

    Args:
        ecg: [12, n] ECG signal data (12 leads, n samples each)
        sample_rate: Sampling frequency (Hz)
        title: Chart title
        bw: If True, black and white grid. Otherwise red grid lines and blue ECG traces.
        show_lead_name: If True, display lead labels
        show_grid: If True, show ECG grid
    """

    # Standard 12-lead ECG labeling
    lead_names = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
    # Order leads: limb leads in first column, precordial in second
    # First column (6 leads): I (0), II (1), III (2), aVR(3), aVL(4), aVF(5)
    # Second column (6 leads): V1(6), V2(7), V3(8), V4(9), V5(10), V6(11)
    # We'll arrange in 2 columns, 6 rows each
    columns = 2
    rows = 6

    # Compute total duration in seconds
    secs = len(ecg[0]) / sample_rate

    # Figure size: Adjust as you like, here width ~ seconds * columns
    # and height ~ some factor of rows
    display_factor = 1
    fig, ax = plt.subplots(figsize=(secs * columns * display_factor, rows * 2 * display_factor - 2))
    fig.subplots_adjust(hspace=0, wspace=0, left=0, right=1, bottom=0, top=0.95)
    fig.suptitle(title)

    # Vertical positioning:
    # We'll stack 6 leads in each column. Each lead separated by a certain vertical distance.
    # Let's say each row_height = 10 units (arbitrary), each lead gets its own slot.
    row_height = 4  # Adjust this as needed
    y_min = - (rows * row_height) + (row_height / 4)
    y_max = row_height / 4
    # With 6 rows, the top lead sits near y_max, the bottom lead near y_min.

    # Colors
    if bw:
        color_major = (0.4, 0.4, 0.4)
        color_minor = (0.75, 0.75, 0.75)
        color_line = (0, 0, 0)
    else:
        color_major = (1, 0, 0)       # Red major lines
        color_minor = (1, 0.7, 0.7)   # Light red minor lines
        color_line = (0, 0, 0.7)      # Blue ECG line

    # Scales:
    # Horizontal: 25 mm/s = 1 large square (10 mm) = 0.4 s
    # We'll place major vertical lines at every 0.4 s
    major_x_interval = 0.4
    # Vertically: 10 mm per mV = 1 mV per large square
    major_y_interval = 1.0

    x_min = 0
    x_max = columns * secs

    if show_grid:
        ax.set_xticks(np.arange(x_min, x_max, major_x_interval))
        ax.set_yticks(np.arange(y_min, y_max, major_y_interval))
        ax.xaxis.set_minor_locator(AutoMinorLocator(5))
        ax.yaxis.set_minor_locator(AutoMinorLocator(5))
        ax.grid(which='major', linestyle='-', linewidth=0.5 * display_factor, color=color_major)
        ax.grid(which='minor', linestyle='-', linewidth=0.5 * display_factor, color=color_minor)

    # Remove axis numbers
    # ax.set_xticklabels([])
    # ax.set_yticklabels([])
    ax.set_ylim(y_min, y_max)
    ax.set_xlim(x_min, x_max)

    line_width = 1

    # Plot the leads
    for c in range(columns):
        for r in range(rows):
            idx = c * rows + r
            if idx < len(ecg):
                # Vertical offset: top lead near y_max, each subsequent lead lower by row_height
                # Start from top going down:
                # Let's say row 0 is at y_offset = 0 (near top), row 1 = -row_height, etc.
                y_offset = -r * row_height

                # Horizontal offset for column
                x_offset = c * secs

                # Draw a vertical separating line between columns
                if c == 1 and separate_columns:
                    # Draw a thick line between the two columns, but only once
                    # Let's place it at x_offset of the second column
                    sep_x = secs  # end of first column
                    ax.plot([sep_x, sep_x], [y_min, y_max],
                            color='black', linewidth=line_width * 2)

                # Plot lead name
                if show_lead_name:
                    ax.text(x_offset + 0.1, y_offset + 0.5, lead_names[idx], fontsize=18 * display_factor)

                step = 1.0 / sample_rate
                time_axis = np.arange(0, len(ecg[idx]) * step, step) + x_offset

                # Plot the ECG signal
                ax.plot(
                    time_axis,
                    ecg[idx] + y_offset,
                    linewidth=line_width * display_factor,
                    color=color_line
                )


def save_as_png(path: str, dpi=200, layout='tight'):
    plt.ioff()
    plt.savefig(path + '.png', dpi=dpi, bbox_inches=layout)
    plt.close()
