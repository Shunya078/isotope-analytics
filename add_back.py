import pandas as pd
import itertools
from clover_package import clover_package as clover

GAIN = 8192


def add_back():
    # 使用ファイルなどの入力引受
    use_file = clover.input_use_file()
    list_num = clover.input_file_count()
    time_lag = clover.input_time_lag()

    bgo_chs = clover.read_bgo_ch()

    # 使用csvファイルをforにて開く
    for i in list_num:
        file_name = '{}00000{}'.format(use_file, str(int(i)))
        df = clover.import_csv(file_name)

        print(f'{file_name}.csv is open...\n')

        ch_results = []
        # パフォーマンス上pandas.DataframeではなくList処理
        t1 = df.t1.values
        t2 = df.t2.values
        t3 = df.t3.values
        ts = df.ts.values
        ch_data = df.calib_ch.values
        adc_data = df.adc.values

        current_row = 0

        # chごとに取り出したデータを繰り返し1行ずつ取り出して処理
        for index in range(df.shape[0]):
            if adc_data[index] is None:
                continue

            if str(adc_data[index]) in bgo_chs:
                current_row = index + 1
                continue
            if current_row < index:
                current_row = index + 1

            if str(current_row) != str(index):
                continue

            if ch_data[index] <= 100:
                continue

            ch_stack = ch_data[index]
            for j in range(300):
                if j == 0:
                    continue

                try:
                    if adc_data[index + j] is None:
                        break
                except IndexError:
                    break

                if str(adc_data[index + j]) in bgo_chs:
                    continue

                t_base = (t1[index] + t2[index] + t3[index]) * 10 + ts[index] * 0.0390625
                t_after = (t1[index + j] + t2[index + j] + t3[index + j]) * 10 + ts[index + j] * 0.0390625
                if -500 <= int(t_after - t_base) <= int(time_lag):
                    ch_stack += ch_data[index + j]
                else:
                    current_row = index + j
                    break
            ch_results.append(ch_stack)

        lag_df = pd.Series(ch_results)
        clover.export_csv(lag_df.value_counts(), '_', file_name, '/data/add_back_csv')
        clover.export_txt(lag_df.value_counts(), '_', file_name, '/data/add_back_txt')

    print("Finished Reading List Data.\n")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    add_back()
