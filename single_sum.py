import pandas as pd
from clover_package import clover_package as clover

GAIN = 8192


def single_sum():
    # 使用ファイルなどの入力引受
    use_file = clover.input_use_file()
    list_num = clover.input_file_count()
    clover_ch = clover.read_clover_ch()

    # 使用csvファイルをforにて開く
    for i in list_num:
        file_name = '{}00000{}'.format(use_file, str(int(i)))
        df = clover.import_csv(file_name)

        print(f'{file_name}.csv is open...\n')

        try:
            clover.export_txt(
                df[['adc', 'calib_ch']].query(f'adc in {clover_ch} and calib_ch < {GAIN}').value_counts('calib_ch'),
                '_',
                file_name,
                '/data/sum_txt')
            clover.export_csv(
                df[['adc', 'calib_ch']].query(f'adc in {clover_ch} and calib_ch < {GAIN}').value_counts('calib_ch'),
                '_',
                file_name,
                '/data/sum_csv')
        except KeyError as error:
            print("Error: {0}".format(error))
            print("Please move calib_data to experience_data. \n")

    print("Finished Reading List Data.\n")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    single_sum()
