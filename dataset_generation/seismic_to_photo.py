from continuous_data_handling import config_general as cfg
from continuous_data_handling import data_streaming as stream
import matplotlib.pyplot as plt
import time
import pandas as pd
import numpy as np
import os


save_plots = False
save_array = False
vmin_vmax = 15
cmap = "Greys"


catalog = pd.read_csv(r'../src/DAS_Catalog.csv')
catalog['photo'] = catalog['Filename'].apply(lambda x: x[-19:-4] + ".png")
catalog['time (s)'] = catalog['Sample in file (P-arrival)'] / 2000  # Hz


def plot_seismic_horiz(data, dx, dt):
    nch, nt = data.shape
    fig = plt.figure(figsize=(8, 5), frameon=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(data, aspect='auto', cmap=cmap, extent=(0, (nt - 1) * dt, (nch - 1) * dx, 0), vmin=-vmin_vmax,
              vmax=vmin_vmax)


def plot_data(data, dx, dt):
    nch, nt = data.shape
    #     plt.figure(figsize=(8,5))
    plt.imshow(data, aspect='auto', cmap='seismic', extent=(0, (nt - 1) * dt, (nch - 1) * dx, 0))
    plt.ylabel('Depth (m)')
    plt.xlabel('Time (s)')


def seismic_to_photo(crop=False):
    data_iter = stream.DataIterator(proc_steps=cfg.proc_steps, folder_name=cfg.data_path,
                                    db_name=cfg.events_db_name, output_overlap=cfg.overlap_samples)
    plt.close('all')
    count = 0
    start = time.time()

    for curr_chunk in data_iter:
        if curr_chunk.check_validity():
            # For each seismic section...
            print(
                f"Saving: {curr_chunk.filename[-19:-4]}, Count: {count}/180, Elapsed Time: {round((time.time() - start) / 60.0, 4)} minutes.")
            filename = curr_chunk.filename

            # If you want the photos segmented into smaller chunks (2 seconds time)
            if crop:
                photo = filename[-19:-4] + ".png"

                # Calculate where in the photo the event occurred and what type of event it was
                pixels_per_second = curr_chunk.data.shape[1] / 15.0  # seconds
                event_seconds = catalog['time (s)'][catalog['photo'] == photo].values[0]
                type = catalog['type'][catalog['photo'] == photo].values[0]
                event_pixel = event_seconds * pixels_per_second

                # Loop through the photo and plot the smaller chunk based on crop size (seconds
                crop_size = 2  # second
                step_size = int(pixels_per_second * crop_size)
                # array_index = 0
                for i in range(0, curr_chunk.data.shape[1], step_size):
                    arr = curr_chunk.data[:, i:i + int(pixels_per_second * crop_size)]
                    event = True if i < event_pixel < i + step_size else False

                    if save_array:
                        if event:
                            np.save(
                                f'F:/Research/DAS/kmeans_numpy/{photo[:-4]}_{int(i / 500)}-{int((i + step_size) / 500)}sec_event{round(event_seconds, 4)}sec.npy',
                                arr)

                        else:
                            np.save(
                                f"F:/Research/DAS/kmeans_numpy/{photo[:-4]}_{int(i / 500)}-{int((i + step_size) / 500)}sec.npy",
                                arr)

                    if save_plots:
                        plot_seismic_horiz(arr, cfg.d_chan, cfg.dt * cfg.dt_decim_fac)
                        if 'None' not in os.listdir("../src/photos/"):
                            os.mkdir('../src/photos/None/')
                            os.mkdir('../src/photos/EQ/')
                            os.mkdir('../src/photos/Micro/')

                        # If the chunk has an event in it, save the photo in the corresponding directory
                        if event:
                            plt.savefig(
                                f"../src/photos/{type}/{photo[:-4]}_{int(i / 500)}-{int((i + step_size) / 500)}sec_event{round(event_seconds, 4)}sec.png")

                        # If not, save it to the "None" photo directory
                        else:
                            plt.savefig(
                                f"../src/photos/None/{photo[:-4]}_{int(i / 500)}-{int((i + step_size) / 500)}sec.png")
                        plt.show()


            # If not, save the entire picture
            else:
                plot_seismic_horiz(curr_chunk.data, cfg.d_chan, cfg.dt * cfg.dt_decim_fac)
                plt.savefig(f'../src/photos/{curr_chunk.filename[-19:-4]}.png', dpi=300, bbox_inches='tight',
                            pad_inches=0)
                plt.show()

            count += 1

    print(f"Total time: {round((time.time() - start) / 60.0, 4)} minutes.")


if __name__ == "__main__":
    seismic_to_photo(crop=True)
