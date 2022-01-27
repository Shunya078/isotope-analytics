import pandas as pd
from clover_package import clover_package as clover

GAIN = 8192


def ch_diff():
    # 使用ファイルなどの入力引受
    print("Write Sum File Name. (ex. [19990708_Eu000001.bin] -> 19990708_Eu)\n")
    sum_file = input('>> ')
    print("Write Simultaneous File Name. (ex. [19990708_Eu000001.bin] -> 19990708_Eu)\n")
    sim_file = input('>> ')
    list_num = clover.input_file_count()

    # 使用csvファイルをforにて開く
    for i in list_num:
        sum_file_name = 'data/add_back_csv/{}00000{}'.format(sum_file, str(int(i)))
        sim_file_name = 'data/simultaneous_csv/{}00000{}'.format(sim_file, str(int(i)))
        sum_df = pd.read_csv(f'./{sum_file_name}.csv', names=["ch", "sum_count"], sep=',')
        sim_df = pd.read_csv(f'./{sim_file_name}.csv', names=["ch", "sim_count"], sep=',')

        print(f'{sum_file_name}.csv and {sim_file_name} is open...\n')

        df = pd.merge(sum_df, sim_df, on='ch', how="left").fillna(0)
        df['count'] = df['sum_count'] - df['sim_count']
        df = df.loc[:, ['ch', 'count']]

        clover.make_dir('./data/ch_diff')
        df.to_csv(
            f'./data/ch_diff/{sum_file}00000{str(int(i))}.txt', encoding='utf-8',
            header=False, sep=' ', index=False)

    print("Finished Reading List Data.\n")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ch_diff()
