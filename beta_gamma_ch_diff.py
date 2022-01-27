import pandas as pd
from decimal import Decimal, ROUND_HALF_UP
from clover_package import clover_package as clover

GAIN = 8192


def beta_gamma_ch_diff():
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
        t_data = df.t_result.values
        ch_data = df.calib_ch.values
        adc_data = df.adc.values

        # chごとに取り出したデータを繰り返し1行ずつ取り出して処理
        for index in range(df.shape[0]):
            if str(adc_data[index]) in bgo_chs:
                try:
                    before_index = index - 1
                except IndexError as error:
                    print("Error: {0}".format(error))
                    continue

                if str(adc_data[index]) == str(adc_data[before_index]):
                    continue

                # BGOとの時間差を取り、同時係数とみなせるなら1つ前のchのデータを削除 -> 残るものがGeのみ
                if int(t_data[index] - t_data[before_index]) <= int(time_lag):
                    if len(ch_results) != 0:
                        del ch_results[-1]
                    continue
                else:
                    continue
            else:
                ch_results.append(ch_data[index])

        lag_df = pd.Series(ch_results)
        clover.export_txt(lag_df.value_counts(), '_', file_name,
                          f'/data/[beta-gamma]ch_diff_txt/{time_lag}ns_{file_name}')

    print("Finished Reading List Data.\n")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    beta_gamma_ch_diff()
