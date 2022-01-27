import pandas as pd
from decimal import Decimal, ROUND_HALF_UP
from clover_package import clover_package as clover

GAIN = 8192


def time_result():
    # 使用ファイルなどの入力引受
    use_file = clover.input_use_file()
    list_num = clover.input_file_count()

    # 使用csvファイルをforにて開く
    for i in list_num:
        file_name = '{}00000{}'.format(use_file, str(int(i)))
        df = clover.import_csv(file_name)

        print(f'{file_name}.csv is open...\n')
        # chが変わったときにtの情報の初期化
        time_array = []

        # パフォーマンス上pandas.DataframeではなくList処理
        t1 = df.t1.values
        t2 = df.t2.values
        t3 = df.t3.values
        ts = df.ts.values

        # chごとに取り出したデータを繰り返し1行ずつ取り出して処理
        for index in range(df.shape[0]):
            t_result = (t1[index] + t2[index] + t3[index]) * 10 + ts[index] * 0.0390625

            # 四捨五入してint変換
            t_result_int = Decimal(t_result.item()).quantize(Decimal('0'), rounding=ROUND_HALF_UP)

            # 正のみ追加
            if t_result_int > 0:
                time_array.append(t_result_int)

        df['t_result'] = time_array
        clover.make_dir('./data/time_result_csv')
        df.to_csv(f'./data/time_result_csv/{file_name}.csv', encoding='utf-8',
                                          header=True, sep=',')
        clover.make_dir('./data/experiment_data')
        df.to_csv(f'./data/experiment_data/[t_result]{file_name}.csv', encoding='utf-8',
                                          header=True, sep=',')

    print("Finished Reading List Data.\n")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    time_result()
