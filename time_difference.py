import pandas as pd
from decimal import Decimal, ROUND_HALF_UP
from clover_package import clover_package as clover

GAIN = 8192


def time_difference():
    # 使用ファイルなどの入力引受
    use_file = clover.input_use_file()
    list_num = clover.input_file_count()
    bgo_chs = clover.read_bgo_ch()

    # 使用csvファイルをforにて開く
    for i in list_num:
        file_name = '{}00000{}'.format(use_file, str(int(i)))
        df = clover.import_csv(file_name)

        print(f'{file_name}.csv is open...\n')
        # chが変わったときにtの情報の初期化
        t_begin = 0
        time_df = []

        # パフォーマンス上pandas.DataframeではなくList処理
        t1 = df.t1.values
        t2 = df.t2.values
        t3 = df.t3.values
        ts = df.ts.values
        adc_data = df.adc.values

        # chごとに取り出したデータを繰り返し1行ずつ取り出して処理
        for index in range(df.shape[0]):
            # tの初期値を代入
            if t_begin == 0:
                t_begin = (t1[index] + t2[index] + t3[index]) * 10 + ts[index] * 0.0390625
                continue

            if str(adc_data[index]) in bgo_chs:
                continue

            t_end = (t1[index] + t2[index] + t3[index]) * 10 + ts[index] * 0.0390625
            t_lag = (t_end - t_begin)

            # 四捨五入してint変換
            t_lag_int = Decimal(t_lag.item()).quantize(Decimal('0'), rounding=ROUND_HALF_UP)

            # 正のみ追加
            # if t_lag_int > 0:
            time_df.append(t_lag_int)

            # 1つ前に現在の行の値を代入
            t_begin = t_end

        time_df = pd.Series(time_df)
        clover.export_txt(time_df.value_counts(), '_', file_name, '/data/time_diff_txt')

    print("Finished Reading List Data.\n")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    time_difference()
