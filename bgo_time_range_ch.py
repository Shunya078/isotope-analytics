import pandas as pd
from decimal import Decimal, ROUND_HALF_UP
from clover_package import clover_package as clover

GAIN = 8192


def bgo_time_range_ch():
    # 使用ファイルなどの入力引受
    use_file = clover.input_use_file()
    list_num = clover.input_file_count()
    print("Write Start time.\n")
    start_time = input('>> ')
    print("Write End Time.\n")
    end_time = input('>> ')

    bgo_chs = clover.read_bgo_ch()

    # 使用csvファイルをforにて開く
    for i in list_num:
        file_name = '{}00000{}'.format(use_file, str(int(i)))
        df = clover.import_csv(file_name)

        print(f'{file_name}.csv is open...\n')

        # chが変わったときにtの情報の初期化
        ch_df = []

        t1 = df.t1.values
        t2 = df.t2.values
        t3 = df.t3.values
        ts = df.ts.values
        ch_data = df.ch.values

        for j in range(df.shape[0]):
            if str(df.adc.values[j]) in bgo_chs:
                t_base = (t1[j] + t2[j] + t3[j]) * 10 + ts[j] * 0.0390625
                try:
                    for k in range(10):
                        if str(df.adc.values[j - k]) in bgo_chs:
                            continue
                        else:
                            t_before = (t1[j - k] + t2[j - k] + t3[j - k]) * 10 + ts[j - k] * 0.0390625

                            t_lag_before = (t_base - t_before)

                            # 四捨五入してint変換
                            t_before_int = Decimal(t_lag_before).quantize(Decimal('0'), rounding=ROUND_HALF_UP)
                            if float(start_time) < t_before_int < float(end_time):
                                ch_df.append(ch_data[j - k])
                            break
                except IndexError as error:
                    print("Error: {0}. \n".format(error))
                    break

        time_df = pd.Series(ch_df)
        clover.export_txt(time_df.value_counts(), '_', file_name, '/data/[bgo]time_range_ch_txt')
        clover.export_csv(time_df.value_counts(), '_', file_name, '/data/[bgo]time_range_ch_csv')

    print("Finished Reading List Data.\n")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    bgo_time_range_ch()
