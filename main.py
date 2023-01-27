from Measurements.measurements import select_measurements
from Plotting.plot_data import plot_field, plot_absorbance
from Plotting.p2p_image import p2p_image
from Plotting.lineplot import plot_line
from Plotting.misc_plot_functions import plot_system_stability
import matplotlib.pyplot as plt
import numpy as np


def find_point(meas_lst, x, y):
    best_match, min_match_rating = None, np.inf
    for meas in meas_lst:
        match_rating = np.abs(meas.position[1] - y) + np.abs(meas.position[0] - x)
        if match_rating < min_match_rating:
            best_match = meas
            min_match_rating = match_rating

    if best_match is None:
        print("No match found")
        return meas_lst[0]
    else:
        print(f"Found: {best_match.filepath.stem}")
        return best_match


def all_plots(point, refs):
    matched_ref_idx = np.argmin([np.abs(point.meas_time - ref_i.meas_time) for ref_i in refs])
    matched_ref = refs[matched_ref_idx]
    sam_fd, ref_fd = point.get_data_fd(), matched_ref.get_data_fd()

    sam_label, ref_label = "sample ", "ref "
    sam_label += f"X={round(point.position[0], 1)} mm, Y={round(point.position[1], 1)} mm"
    ref_label += f"X={round(matched_ref.position[0], 1)} mm, Y={round(matched_ref.position[1], 1)} mm"

    plot_field(ref_fd, label=ref_label, freq_range=(0, 6))
    plot_field(sam_fd, label=sam_label, freq_range=(0, 6))

    plot_system_stability(refs)

    plot_absorbance(sam_fd, ref_fd, freq_range=(0.25, 3), label=sam_label)


def main():
    keywords = ["PencilPainted"]
    refs, sams = select_measurements(keywords, case_sensitive=True, match_exact=True)
    sams = [sam for sam in sams if (sam.position[0] < 50)]
    #sams = [sam for sam in sams if sam.position[1] > 1]

    p2p_image(refs, sams, point_value="rel_p2p")
    #plot_line(refs, sams, point_value="integrated_intensity", label="No paint")
    plt.show()

    point_H = find_point(sams, x=45, y=21)
    point_paint = find_point(sams, x=36, y=12)

    plot_field(refs[0].get_data_fd(), label="ref", freq_range=(0, 6))
    plot_field(point_H.get_data_fd(), label=str(point_H.position), freq_range=(0, 6))
    plot_field(point_paint.get_data_fd(), label=str(point_paint.position), freq_range=(0, 6))

    """
    keywords = ["TestPoints"]
    refs, sams = select_measurements(keywords, case_sensitive=True)
    for sam in sams:
        print(sam)

    coal_field = [sam for sam in sams if "coal_field" in str(sam.filepath)][0]
    paint_coal_field = [sam for sam in sams if "paint_coal_field" in str(sam.filepath)][0]
    paint_pencil_field = [sam for sam in sams if "paint_pencil_field" in str(sam.filepath)][0]
    pencil_field = [sam for sam in sams if "pencil_field" in str(sam.filepath)][0]
    paper = [sam for sam in sams if "paper" in str(sam.filepath)][0]

    plot_field(refs[0].get_data_fd(), label="ref", freq_range=(0, 6))
    plot_field(coal_field.get_data_fd(), label="coal", freq_range=(0, 6))
    plot_field(paint_coal_field.get_data_fd(), label="paint_coal", freq_range=(0, 6))
    plot_field(paint_pencil_field.get_data_fd(), label="paint_pencil", freq_range=(0, 6))
    plot_field(pencil_field.get_data_fd(), label="pencil", freq_range=(0, 6))
    plot_field(paper.get_data_fd(), label="paper", freq_range=(0, 6))
    """


if __name__ == '__main__':
    main()
    plt.show()
