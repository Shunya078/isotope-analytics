import pandas as pd
import os

GAIN = 8192


def read_define_ch():
    # ch定義ファイル読み込み
    ch_txt = open("GeCalibration.txt", "r")
    ch_row = ch_txt.readlines()
    define_ch = ch_row[0].replace("\n", "").replace(" ", "").split(":")[1].split(",")
    bgo_ch = ch_row[1].replace("\n", "").replace(" ", "").split(":")[1].split(",")
    for i, ch in enumerate(bgo_ch):
        define_ch.append(ch)
    ch_txt.close()
    return define_ch


def read_clover_ch():
    # ch定義ファイル読み込み
    ch_txt = open("GeCalibration.txt", "r")
    ch_row = ch_txt.readlines()
    clover_ch = ch_row[0].replace("\n", "").replace(" ", "").split(":")[1].split(",")
    ch_txt.close()
    return list(map(int, clover_ch))


def read_bgo_ch():
    # ch定義ファイル読み込み
    ch_txt = open("GeCalibration.txt", "r")
    ch_row = ch_txt.readlines()
    bgo_ch = ch_row[1].replace("\n", "").replace(" ", "").split(":")[1].split(",")
    ch_txt.close()
    return bgo_ch


def read_define_equation():
    # 関数定義ファイル読み込み
    ge_txt = open("GeCalibration.txt", "r")
    equ_row = ge_txt.readlines()[2:]
    define_equation = []
    for i in range(5):
        define_equation.append(equ_row[i].replace("\n", "").replace(" ", "").split(":")[1].split(","))
    ge_txt.close()
    return define_equation


def input_use_file():
    print("Write File Name. (ex. [19990708_Eu000001.bin] -> 19990708_Eu)\n")
    use_file = input('>> ')
    return use_file


def input_file_count():
    print("Write File Counts. (ex. [19990708_Eu000003.bin] -> 3)\n")
    list_num = input('>> ')
    return list_num


def input_time_lag():
    print("Write Time Lag. (ex. [0~600 ns] -> 600)\n")
    time_lag = input('>> ')
    return time_lag


def import_csv(file_name):
    try:
        df = pd.read_csv(f'./data/experiment_data/{file_name}.csv', sep=',')
    except FileNotFoundError as error:
        print("Error: {0}".format(error))
        raise
    return df


def export_txt(data, file_number, file_name, path):
    make_dir(f'.{path}')
    if file_number == '_':
        file = file_name.replace('\n', '').split("/")
        data.sort_index().to_csv(f'.{path}/{file[-1]}.txt', encoding='utf-8',
                                 header=False, sep=' ')
    else:
        data.sort_index().to_csv(f'.{path}/{file_name}_{file_number}.txt', encoding='utf-8',
                                 header=False, sep=' ')


def export_csv(data, file_number, file_name, path):
    make_dir(f'.{path}')
    if file_number == '_':
        file = file_name.replace('\n', '').split("/")
        data.sort_index().to_csv(f'.{path}/{file[-1]}.csv', header=False)
    else:
        data.sort_index().to_csv(f'.{path}/{file_name}_{file_number}.csv', header=False)


def make_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('This is clover_package!')
