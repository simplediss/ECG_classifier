import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import AutoMinorLocator
from math import ceil


def plot_ecg(
        ecg, 
        sample_rate    = 500, 
        title          = '', 
        lead_index     = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6'], 
        lead_order     = None,
        style          = 'bw',
        columns        = 2,
        row_height     = 3,
        show_lead_name = True,
        show_grid      = True,
        show_separate_line  = False,
        ):
    """Plot multi lead ECG chart.

    Modified from https://github.com/dy1901/ecg_plot/
    # Arguments
        ecg        : m x n ECG signal data, which m is number of leads and n is length of signal.
        sample_rate: Sample rate of the signal.
        title      : Title which will be shown on top off chart
        lead_index : Lead name array in the same order of ecg, will be shown on 
            left of signal plot, defaults to ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
        lead_order : Lead display order 
        columns    : display columns, defaults to 2
        style      : display style, defaults to None, can be 'bw' which means black white
        row_height :   how many grid should a lead signal have,
        show_lead_name : show lead name
        show_grid      : show grid
        show_separate_line  : show separate line
    """

    if not lead_order:
        lead_order = list(range(0,len(ecg)))
    secs  = len(ecg[0])/sample_rate
    leads = len(lead_order)
    rows  = int(ceil(leads/columns))
    # display_factor = 2.5
    display_factor = 2.5
    line_width = 0.5
    fig, ax = plt.subplots(figsize=(secs*columns * display_factor, rows * row_height / 5 * display_factor))
    display_factor = display_factor ** 0.5
    fig.subplots_adjust(
        hspace = 0, 
        wspace = 0,
        left   = 0,  # the left side of the subplots of the figure
        right  = 1,  # the right side of the subplots of the figure
        bottom = 0,  # the bottom of the subplots of the figure
        top    = 1
        )

    fig.suptitle(title)

    x_min = 0
    x_max = columns*secs
    y_min = row_height/4 - (rows/2)*row_height
    y_max = row_height/4

    if (style == 'bw'):
        color_major = (0.4,0.4,0.4)
        color_minor = (0.75, 0.75, 0.75)
        color_line  = (0,0,0)
    else:
        color_major = (1,0,0)
        color_minor = (1, 0.7, 0.7)
        color_line  = (0,0,0.7)

    plt.xlabel("25mm/s")
    plt.ylabel("1cm/mV")
    # plt.text(x_min + 0.1, y_min + 0.5, '\n', fontsize=9 * display_factor)

    if(show_grid):
        ax.set_xticks(np.arange(x_min,x_max,0.2))    
        ax.set_yticks(np.arange(y_min,y_max,0.5))

        ax.minorticks_on()
        
        ax.xaxis.set_minor_locator(AutoMinorLocator(5))

        ax.grid(which='major', linestyle='-', linewidth=0.5 * display_factor, color=color_major)
        ax.grid(which='minor', linestyle='-', linewidth=0.5 * display_factor, color=color_minor)

    ax.set_ylim(y_min,y_max)
    ax.set_xlim(x_min,x_max)


    # Remove axis numbers
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_ylim(y_min, y_max)
    ax.set_xlim(x_min, x_max)

    line_width = 1

    # Secondary x-axis for 1-second intervals (placed at the bottom)
    sec_ax = ax.twiny()  # Create a secondary x-axis sharing the y-axis

    # Configure the secondary axis
    sec_ax.set_xlim(x_min, x_max)  # Match the primary x-axis limits
    sec_ax.set_xticks(np.arange(x_min, x_max + 1, 1))  # Major ticks at 1-second intervals
    sec_ax.set_xticklabels([f"{int(t % secs)} s" for t in np.arange(x_min, x_max + 1, 1)])  # Label ticks with seconds
    sec_ax.tick_params(axis='x', direction='in', length=secs, width=1, labelsize=10)  # Style the ticks

    # Move the secondary x-axis to the bottom of the plot
    sec_ax.spines['top'].set_visible(False)  # Hide the top spine (default position for twiny)
    sec_ax.spines['bottom'].set_position(('axes', -0.0))  # Position the axis below the plot
    sec_ax.xaxis.set_label_position('bottom')
    sec_ax.xaxis.tick_bottom()

    for c in range(0, columns):
        for i in range(0, rows):
            if (c * rows + i < leads):
                y_offset = -(row_height/2) * ceil(i%rows)
                # if (y_offset < -5):
                #     y_offset = y_offset + 0.25

                x_offset = 0
                if(c > 0):
                    x_offset = secs * c
                    if(show_separate_line):
                        ax.plot([x_offset, x_offset], [ecg[t_lead][0] + y_offset - 0.3, ecg[t_lead][0] + y_offset + 0.3], linewidth=line_width * display_factor, color=color_line)

         
                t_lead = lead_order[c * rows + i]
         
                step = 1.0/sample_rate
                if(show_lead_name):
                    ax.text(x_offset + 0.07, y_offset - 0.5, lead_index[t_lead], fontsize=9 * display_factor)
                ax.plot(
                    np.arange(0, len(ecg[t_lead])*step, step) + x_offset, 
                    ecg[t_lead] + y_offset,
                    linewidth=line_width * display_factor, 
                    color=color_line
                    )
        

def save_as_png(path: str, dpi=200, layout='tight'):
    plt.ioff()
    plt.savefig(path + '.png', dpi=dpi, bbox_inches=layout)
    plt.close()
