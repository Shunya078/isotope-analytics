import pandas as pd
from clover_package import clover_package as clover

GAIN = 8192


def time_sort():
    # 使用ファイルなどの入力引受
    use_file = clover.input_use_file()
    list_num = clover.input_file_count()

    for i in list_num:
        file_name = '{}00000{}'.format(use_file, str(int(i)))
        df = clover.import_csv(file_name)

        print(f'{file_name}.csv is open...\n')

        # chが変わったときにtの情報の初期化
        time_results = []
        time_results = df.t_result.values

        df['t_result'] = time_results
        clover.make_dir('./data/time_sort_csv')
        df.sort_values('t_result').to_csv(f'./data/time_sort_csv/{file_name}.csv', encoding='utf-8',
                                          header=True, sep=',')
        clover.make_dir('./data/experiment_data')
        df.sort_values('t_result').to_csv(f'./data/experiment_data/[sort]{file_name}.csv', encoding='utf-8',
                                          header=True, sep=',')

    print("Finished Reading List Data.\n")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    time_sort()
