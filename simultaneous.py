import pandas as pd
from clover_package import clover_package as clover

GAIN = 8192


def simultaneous():
    # 使用ファイルなどの入力引受
    use_file = clover.input_use_file()
    list_num = clover.input_file_count()

    print(f'--- simultaneous diff ---.')
    time_lag = clover.input_time_lag()

    print(f'--- add-back diff ---.')
    add_back_lag = clover.input_time_lag()

    bgo_chs = clover.read_bgo_ch()

    # 使用csvファイルをforにて開く
    for i in list_num:
        file_name = '{}00000{}'.format(use_file, str(int(i)))
        df = clover.import_csv(file_name)

        print(f'{file_name}.csv is open...\n')

        ch_results = []
        decomposed_ch_results = []
        ge_ch_stack = set()
        # 速度リファクタのため
        ch_results_append = ch_results.append
        ge_ch_stack_add = ge_ch_stack.add
        de_ch_results_append = decomposed_ch_results.append

        # パフォーマンス上pandas.DataframeではなくList処理
        t1 = df.t1.values
        t2 = df.t2.values
        t3 = df.t3.values
        ts = df.ts.values
        ge_index = df.index.values
        ch_data = df.calib_ch.values
        adc_data = df.adc.values

        # chごとに取り出したデータを繰り返し1行ずつ取り出して処理
        for index in range(df.shape[0]):
            if adc_data[index] is None:
                continue

            if str(adc_data[index]) in bgo_chs:
                if ch_data[index] <= 100:
                    continue

                for j in reversed(range(300)):
                    if j == 0:
                        continue
                    diff_count = index + (150 - j)
                    try:
                        adc_sample = adc_data[diff_count]
                    except IndexError:
                        break
                    if str(adc_data[diff_count]) in bgo_chs:
                        continue
                    if ch_data[diff_count] <= 100:
                        continue

                    t_base = (t1[index] + t2[index] + t3[index]) * 10 + ts[index] * 0.0390625
                    t_before = (t1[diff_count] + t2[diff_count] + t3[diff_count]) * 10 + ts[diff_count] * 0.0390625

                    if -1000 <= float(t_base - t_before) <= float(time_lag):
                        if int(ge_index[diff_count]) in ge_ch_stack:
                            continue
                        ch_stack = ch_data[diff_count]
                        ge_ch_stack_add(int(ge_index[diff_count]))
                        if 3680 <= ch_stack <= 5460:
                            de_ch_results_append([ch_stack])

                        for k in range(300):
                            if k == 0:
                                continue
                            if str(adc_data[diff_count - k]) is None:
                                continue
                            if str(adc_data[diff_count - k]) in bgo_chs:
                                continue
                            if ch_data[diff_count - k] <= 100:
                                continue

                            t_before_add_back \
                                = (t1[diff_count - k] + t2[diff_count - k] + t3[diff_count - k]) * 10 + \
                                  ts[diff_count - k] * 0.0390625

                            if -500 <= float(t_before - t_before_add_back) <= float(add_back_lag):
                                # if int(ge_index[diff_count - k]) in ge_ch_stack:
                                #     continue
                                ch_stack += ch_data[diff_count - k]
                                # ge_ch_stack_add(int(ge_index[diff_count - k]))
                                if 3680 <= ch_stack <= 5460:
                                    de_ch_results_append([ch_data[diff_count - k]])

                        ch_results_append(ch_stack)

        lag_df = pd.Series(ch_results)
        de_lag_df = pd.Series(decomposed_ch_results)
        clover.export_csv(lag_df.value_counts(), '_', file_name, '/data/mac_simultaneous_csv')
        clover.export_txt(lag_df.value_counts(), '_', file_name, '/data/mac_simultaneous_txt')
        clover.export_csv(de_lag_df.value_counts(), '_', file_name, '/data/de_simultaneous_csv')
        clover.export_txt(de_lag_df.value_counts(), '_', file_name, '/data/de_simultaneous_txt')

    print("Finished Reading List Data.\n")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    simultaneous()
