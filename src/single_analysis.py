import pandas as pd
from clover_package import clover_package as clover

GAIN = 8192


def single_analysis():
    # 使用ファイルなどの入力引受
    use_file = clover.input_use_file()
    list_num = clover.input_file_count()
    input_ch = clover.read_define_ch()

    # 使用csvファイルをforにて開く
    for i in list_num:
        file_name = '{}00000{}'.format(use_file, str(int(i)))
        df = clover.import_csv(file_name)

        print(f'{file_name}.csv is open...\n')

        ch_data = []
        for j, input_ch in enumerate(input_ch):
            ch_data.append(df[['adc', 'ch']].query(f'adc == {input_ch} and ch < {GAIN}'))
            ch_data[j] = ch_data[j]['ch'].value_counts()
            clover.export_txt(ch_data[j], input_ch, file_name, f'/data/single_analysis_txt/{file_name}')

    print("Finished Reading List Data.\n")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    single_analysis()
