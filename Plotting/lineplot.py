import matplotlib.pyplot as plt
import numpy as np

from imports import *


def plot_line(refs, sams, point_value="rel_p2p", freq_sum_range=(1.5, 2.0), label=""):
    x_positions = [meas.position[0] for meas in sams]

    refs = sorted(refs, key=lambda ref: ref.meas_time)
    sams = sorted(sams, key=lambda sam: sam.meas_time)

    plt.figure("Linescanplot")

    y_vals = []
    for i in range(len(sams)):
        matched_ref_idx = np.argmin([np.abs(sams[i].meas_time - ref_i.meas_time) for ref_i in refs])
        matched_ref = refs[matched_ref_idx]

        sam_fd, ref_fd = sams[i].get_data_fd(), matched_ref.get_data_fd()
        sam_td_data, ref_td_data = sams[i].get_data_td(), matched_ref.get_data_td()

        if "rel_p2p" in point_value:
            plt.title("Sam / ref peak to peak value")
            plt.ylabel(r"p2p($y_{sam}$) / p2p($y_{ref}$)")

            p2p_val_sam = np.abs(np.max(sam_td_data[:, 1]) - np.min(sam_td_data[:, 1]))
            p2p_val_ref = np.abs(np.max(ref_td_data[:, 1]) - np.min(ref_td_data[:, 1]))
            val = p2p_val_sam / p2p_val_ref
            y_vals.append(val)
        elif "integrated_intensity" in point_value:
            plt.title(f"Integrated spectra ({freq_sum_range[0]} THz - {freq_sum_range[1]} THz)")
            plt.ylabel(r"$\sum |FFT(y_{sam})| $ / $\sum |FFT(y_{ref})|$")

            freq_slice = slice(int(freq_sum_range[0] * 100), int(freq_sum_range[1] * 100))
            val = np.sum(np.abs(sam_fd[freq_slice])) / np.sum(np.abs(ref_fd[freq_slice]))
            y_vals.append(val)
        elif "pulse_position" in point_value:
            ax_title = "Pulse position"
            cbar_label = ""

            argmax_sam = np.argmax(np.abs(sam_td_data[:, 1]))
            val = sam_td_data[argmax_sam, 0]
            y_vals.append(val)

    y_vals.reverse()
    y_vals = np.array(y_vals)

    #y_vals /= np.max(y_vals)

    plt.plot(x_positions, y_vals, label=label)
    plt.xlabel("Horizontal stage pos. x (mm)")
    plt.legend()

