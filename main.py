# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import APV8016_calib
import time_sort as t_sort
import single_analysis as analysis
import single_sum
import bgo_time_diff as b_g_t_diff
import beta_gamma_ch_diff as b_g_ch_diff
import time_difference as t_diff
import simultaneous
import deducted


def main():
    print('Start APV8016_calib.py (ex. Input File Name："data/calibration_csv/calib_20210617_Cs")')
    APV8016_calib.calibrate()

    print('Start time_sort.py (ex. Input File Name："data/time_sort_csv/calib_20210617_Cs")')
    t_sort.time_sort()

    print('Start single_analysis.py \n'
          '(ex. Input File Name："data/single_analysis_txt/calib_20210617_Cs/calib_20210617_Cs_0")')
    analysis.single_analysis()

    print('Start single_sum.py (ex. Input File Name："data/single_sum/calib_20210617_Cs")')
    single_sum.single_sum()

    print(
        'Start bgo_time_diff.py -> \n '
        '※ Need time_sort File (ex. Input File Name："data/[beta-gamma]time_diff_csv/calib_20210617_Cs")')
    b_g_t_diff.bgo_time_diff()

    print('Start beta_gamma_ch_diff.py -> \n'
          '※Need time_sort File (ex. Input File Name："data/[beta-gamma]ch_diff_csv/calib_20210617_Cs")')
    b_g_ch_diff.beta_gamma_ch_diff()

    print(
        'Start time_difference.py ->※ Need time_sort File (ex. Input File Name："data/time_diff_csv/calib_20210617_Cs")')
    t_diff.time_difference()

    print(
        'Start simultaneous.py ->※ Need time_sort File (ex. Input File Name："data/simultaneous/calib_20210617_Cs")')
    simultaneous.simultaneous()

    print(
        'Start deducted.py ->※ Need time_sort File (ex. Input File Name："data/ch_diff/calib_20210617_Cs")')
    deducted.deducted()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
