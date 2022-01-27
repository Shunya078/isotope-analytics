import pandas as pd
from decimal import Decimal, ROUND_HALF_UP
from clover_package import clover_package as clover

GAIN = 8192


def calibrate():
    # 使用ファイルなどの入力引受
    use_file = clover.input_use_file()
    list_num = clover.input_file_count()

    clover_ch = clover.read_clover_ch()
    input_equ = clover.read_define_equation()

    # 使用csvファイルをforにて開く
    for i in list_num:
        file_name = '{}00000{}'.format(use_file, str(int(i)))
        df = clover.import_csv(file_name)

        print(f'{file_name}.csv is open...\n')

        before_ch = df.ch.values
        adc_data = df.adc.values

        ch_results = []
        for k, before_ch in enumerate(before_ch):
            if adc_data[k] in clover_ch:
                correct_equ = input_equ[int(clover_ch.index(adc_data[k]) + 1)]
                float_ch = float(before_ch)
                result = float(correct_equ[0]) * float_ch * float_ch + float(correct_equ[1]) * float_ch + float(
                    correct_equ[2])
                after_ch = (result - float(input_equ[0][2])) / float(input_equ[0][1])
                ch_results.append(Decimal(after_ch).quantize(Decimal('0'), rounding=ROUND_HALF_UP))
            else:
                ch_results.append(before_ch)

        df['calib_ch'] = ch_results
        clover.make_dir('./data/calibration_csv')
        df.to_csv(f'./data/calibration_csv/calib_{file_name}.csv', encoding='utf-8',
                  header=True, sep=',')
        clover.make_dir('./data/experiment_data')
        df.to_csv(f'./data/experiment_data/calib_{file_name}.csv', encoding='utf-8',
                  header=True, sep=',')

    print("Finished Reading List Data.\n")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    calibrate()
