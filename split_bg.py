import pandas as pd
from decimal import Decimal, ROUND_HALF_UP
from clover_package import clover_package as clover

GAIN = 8192


def split_bg():
    # 使用ファイルなどの入力引受
    print("Write BG File Name. (ex. [19990708_Eu000001.bin] -> 19990708_Eu)\n")
    bg_file = input('>> ')
    print("Write Experiment File Name. \n")
    experiment_file = input('>> ')
    list_num = clover.input_file_count()

    bgo_chs = clover.read_bgo_ch()

    # 使用csvファイルをforにて開く
    for i in list_num:
        bg_file_name = 'data/bg_csv/{}00000{}'.format(bg_file, str(int(i)))
        experiment_file_name = 'data/experiment_data/{}00000{}'.format(experiment_file, str(int(i)))

        df = clover.import_csv(experiment_file_name)
        print(f'{experiment_file_name}.csv is open...\n')

        ch_data = df.ch.values
        adc_data = df.adc.values

        experiment_event_counts = 0
        # chごとに取り出したデータを繰り返し1行ずつ取り出して処理
        for index in range(df.shape[0]):
            if adc_data[index] is None:
                continue

            if str(adc_data[index]) in bgo_chs:
                continue

            # K のイベント数管理
            if 2911 <= ch_data[index] <= 2931:
                experiment_event_counts += 1
            # Ti のイベント数管理
            if 5218 <= ch_data[index] <= 5238:
                experiment_event_counts += 1

        print(f'{experiment_file_name}.csv is finished. \n')

        bg_df = clover.import_csv(bg_file_name)
        print(f'{bg_file_name}.csv is open...\n')

        bg_ch_data = bg_df.ch.values
        bg_adc_data = bg_df.adc.values
        bg_index = bg_df.index.values

        bg_event_counts = 0
        finish_index = 0

        bgo_index_stack = []
        bgo_index_stack_append = bgo_index_stack.append
        # chごとに取り出したデータを繰り返し1行ずつ取り出して処理
        for index in range(bg_df.shape[0]):
            if bg_adc_data[index] is None:
                continue

            if str(bg_adc_data[index]) in bgo_chs:
                bgo_index_stack_append(bg_index[index])
                continue

            # K のイベント数管理
            if 2911 <= bg_ch_data[index] <= 2931:
                bg_event_counts += 1
            # Ti のイベント数管理
            if 5218 <= bg_ch_data[index] <= 5238:
                bg_event_counts += 1
            # event 数が超えたらその時の行番号を記録する
            if bg_event_counts >= experiment_event_counts:
                finish_index = bg_index[index]
                break

        split_df = bg_df[:finish_index]
        split_df.drop(index=bgo_index_stack, inplace=True)
        clover.make_dir('./data/split_bg_csv')
        split_df.to_csv(f'./data/split_bg_csv/split_{bg_file_name}.csv', encoding='utf-8',
                        header=True, sep=',')
        clover.make_dir('./data/experiment_data')
        split_df.to_csv(f'./data/experiment_data/split_{bg_file_name}.csv', encoding='utf-8',
                        header=True, sep=',')

    print("Finished Reading List Data.\n")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    split_bg()
