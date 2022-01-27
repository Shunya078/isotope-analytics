import pandas as pd
from clover_package import clover_package as clover

GAIN = 8192


def deducted_bg():
    # 使用ファイルなどの入力引受
    print("Write BG File Name. (ex. [19990708_Eu000001.bin] -> 19990708_Eu)\n")
    bg_file = input('>> ')
    print("Write Experiment File Name. (ex. [19990708_Eu000001.bin] -> 19990708_Eu)\n")
    experiment_file = input('>> ')
    list_num = clover.input_file_count()
    bgo_chs = clover.read_bgo_ch()

    # 使用csvファイルをforにて開く
    for i in list_num:
        bg_file_name = 'data/experiment_data/{}00000{}'.format(bg_file, str(int(i)))
        experiment_file_name = 'data/experiment_data/{}00000{}'.format(experiment_file, str(int(i)))
        bg_df = pd.read_csv(f'./{bg_file_name}.csv', sep=',')
        experiment_df = pd.read_csv(f'./{experiment_file_name}.csv', sep=',')

        print(f'{bg_file_name}.csv and {experiment_file_name} is open...\n')

        ge_index = bg_df.index.values
        ch_data = bg_df.calib_ch.values
        ex_ge_index = experiment_df.index.values
        ex_ch_data = experiment_df.calib_ch.values
        ex_adc_data = experiment_df.adc.values

        bg_index_stack = set()
        bg_stack_add = bg_index_stack.add
        ex_index_stack = []
        ex_stack_append = ex_index_stack.append

        for ex_index in range(experiment_df.shape[0]):
            if str(ex_adc_data[ex_index]) in bgo_chs:
                continue

            for index in range(bg_df.shape[0]):
                if int(ge_index[index]) in bg_index_stack:
                    continue
                if ch_data[index] == ex_ch_data[ex_index]:
                    bg_stack_add(int(ge_index[index]))
                    ex_stack_append(ex_ge_index[ex_index])
                    break

        df = experiment_df.drop(index=ex_ge_index)

        clover.make_dir('./data/deducted')
        df.to_csv(
            f'./data/deducted/bg_{bg_file_name}00000{str(int(i))}.csv', encoding='utf-8',
            header=False, sep=' ', index=False)

    print("Finished Reading List Data.\n")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    deducted_bg()
