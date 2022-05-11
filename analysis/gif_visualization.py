import matplotlib.pyplot as plt
import numpy as np
from continuous_data_handling import config_general as cfg

trace1 = np.load(r'F:/Research/DAS/kmeans_numpy/UTC190426070723_0-2sec.npy')
trace2 = np.load(r'F:/Research/DAS/kmeans_numpy/UTC190426070723_2-4sec.npy')
trace3 = np.load(r'F:/Research/DAS/kmeans_numpy/UTC190426070723_4-6sec.npy')
trace4 = np.load(r'F:/Research/DAS/kmeans_numpy/UTC190426070723_6-8sec.npy')
trace5 = np.load(r'F:/Research/DAS/kmeans_numpy/UTC190426070723_8-10sec.npy')
trace6 = np.load(r'F:/Research/DAS/kmeans_numpy/UTC190426070723_10-12sec.npy')
trace7 = np.load(r'F:/Research/DAS/kmeans_numpy/UTC190426070723_12-14sec_event12.4055sec.npy')
trace8 = np.load(r'F:/Research/DAS/kmeans_numpy/UTC190426070723_14-16sec.npy')


def plot_data(data, dx, dt):
    nch, nt = data.shape
    plt.figure(figsize=(8, 5))
    plt.imshow(data, aspect='auto', cmap='seismic', extent=(0, (nt - 1) * dt, (nch - 1) * dx, 0), vmin=-21, vmax=21)
    plt.ylabel('Depth (m)')
    plt.xlabel('Time (s)')


i = 1
sec = 0
for ex in [trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8]:
    plot_data(ex, cfg.d_chan, cfg.dt * cfg.dt_decim_fac)
    plt.colorbar()
    plt.title(f"UTC190426070723 -- Seconds {sec} through {min([sec + 2, 15])}")
    plt.savefig(f'C:/Users/Peter/Downloads/{i}_orig.pdf')
    sec += 2
    i += 1
    plt.show()
