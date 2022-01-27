import pandas as pd
from clover_package import clover_package as clover

GAIN = 8192


def deducted():
    # 使用ファイルなどの入力引受
    print("Write AddBack File Name. (ex. [19990708_Eu000001.bin] -> 19990708_Eu)\n")
    add_back_file = input('>> ')
    print("Write Simultaneous File Name. (ex. [19990708_Eu000001.bin] -> 19990708_Eu)\n")
    sim_file = input('>> ')
    list_num = clover.input_file_count()

    # 使用csvファイルをforにて開く
    for i in list_num:
        add_back_file_name = 'data/add_back_csv/{}00000{}'.format(add_back_file, str(int(i)))
        sim_file_name = 'data/simultaneous_csv/{}00000{}'.format(sim_file, str(int(i)))
        add_back_df = pd.read_csv(f'./{add_back_file_name}.csv', names=["ch", "add_back_count"], sep=',')
        sim_df = pd.read_csv(f'./{sim_file_name}.csv', names=["ch", "sim_count"], sep=',')

        print(f'{add_back_file_name}.csv and {sim_file_name} is open...\n')

        df = pd.merge(add_back_df, sim_df, on='ch', how="left").fillna(0)
        df['count'] = df['add_back_count'] - (df['sim_count'] * 1.0)
        df = df.loc[:, ['ch', 'count']]

        clover.make_dir('./data/100_deducted')
        df.to_csv(
            f'./data/100_deducted/{add_back_file}00000{str(int(i))}.txt', encoding='utf-8',
            header=False, sep=' ', index=False)

    print("Finished Reading List Data.\n")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    deducted()
