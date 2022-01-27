## 概要
クローバー検出器の解析に使うファイルです。

## 実行順序
1. 検出器からエクスポートしたbinファイルをトップルートのフォルダ内に入れる

2. binファイルからcsvにデータの書き出し
```
> cl bin_to_csv_APV8016.cpp
Microsoft(R) C/C++ Optimizing Compiler Version 19.28.29914 for x64
Copyright (C) Microsoft Corporation.  All rights reserved.

bin_to_csv_APV8016.cpp
Microsoft (R) Incremental Linker Version 14.28.29914.0
Copyright (C) Microsoft Corporation.  All rights reserved.

/out:bin_to_csv_APV8016.exe
bin_to_csv_APV8016.obj

> bin_to_csv_APV8016.exe
Write File Name. (ex. [19990708_Eu000001.bin] -> 19990708_Eu)
>> 20210528_Cs
Write File Counts. (ex. [19990708_Eu000003.bin] -> 3)
>> 1
20210528_Cs000001.bin is open...
Finished Reading List Data.
```

3. `GeCalibration.txt` にて使用chを入力
```
// 規則は：のあとに「,」区切りで入力 & BGO_Numberはなしなら「BGO_Number:」で良い
Ge_Number: 0, 1, 2, 14
BGO_Number: 4, 5
...
```
4. `data/experiment_data` フォルダを作成し、その中に2.で生成したcsvファイルを入れる

5. APV8016_calibrate.py にてClover4結晶のchをエネルギー較正式から補正

6. main.py を実行すると順に全ファイル回る

## 各ファイル実行要素

- add_back.py
    -> 時間差以内のchを足し合わせる / BGO_Numberは除く
    - 該当生成フォルダ：./data/add_back_csv

- APV8016_calibrate.py
    -> 上記にて生成されたcsvファイルから、エネルギー較正を行い、GeCalibrate.txt に入力された `ax^2 + bx + c` それぞれの係数を使用し、4つの結晶が検出事象を補正
    - なお、頻繁にコンソールへ入力するため、experiment_dataにも出力する
    - 該当生成フォルダ：./data/calibration_csv & ./data/experiment_data
    - `calib_ch` 行を追加

- beta_gamma_ch_diff.py
    -> BGOとGeの事象の時間差を取り、同時事象とみなすものは落としたGeのみのデータと、落とすスペクトルの2つを出力
    - 該当生成フォルダ：./data/[beta-gamma]ch_diff_txt/{指定時間}ns_{ファイル名} & ./data/coincidence_ch_diff_txt/{指定時間}ns_{ファイル名}
    - time_sort したCSVを指定する必要アリ

- beta_gamma_time_diff.py
    -> 上記にて生成されたcsvファイルから、BGOの事象とその1つ前の事象を比べ、時間差を算出
    - 該当生成フォルダ：./data/[beta-gamma]time_diff_csv & ./data/[beta-gamma]time_diff_txt
    - time_sort したCSVを指定する必要アリ

- ch_diff.py
    -> 2つのスペクトルを差し引いたスペクトルを算出
    - 該当生成フォルダ：./data/ch_diff
    - `./data/sum_csv` 内のファイルと `./data/simultaneous_csv` 内のファイルを指定

- simultaneous.py
    -> すべての入力ch同士の、同時事象を1つのスペクトルとして算出
    - 該当生成フォルダ：./data/simultaneous

- single_analysis.py
    -> 上記にて生成されたcsvファイルから、それぞれの結晶が検出したスペクトルを算出
    - 該当生成フォルダ：./data/single_analysis_txt/{ファイル名}/{それぞれのchごとのスペクトル}.txt

- single_sum.py
    -> 上記にて生成されたcsvファイルから、それぞれの結晶が検出したスペクトルを1つのデータに算出
    - 該当生成フォルダ： ./data/sum_txt

- time_difference.py
    -> 上記にて生成されたcsvファイルから、全事象のうち2要素ずつ取り出して、差分をcountに出す
    - 該当生成フォルダ：./data/time_diff
    - time_sort したCSVを指定する必要アリ

- time_sort.py
    -> 上記にて生成されたcsvファイルから、時間[ns]を算出し、昇順に並び替え
    - なお、頻繁にコンソールへ入力するため、experiment_dataにも出力する
    - 該当生成フォルダ：./data/time_sort
    - `t_result` 列を追加

## ファイル実行方法
1. PyCharmにて作業フォルダを開く
2. Edit Configureを設定したのちにRun(実行)
3. (a) Fileがdataフォルダ内にある場合は以下のように指定
```
Write File Name. (ex. [19990708_Eu000001.bin] -> 19990708_Eu)

>> 20210617_Cs
Write File Counts. (ex. [19990708_Eu000003.bin] -> 3)

>> 1
```

3. (b) Fileがdataフォルダ内にある場合は以下のように指定
```
Write File Name. (ex. [19990708_Eu000001.bin] -> 19990708_Eu)

>> data/time_sort_csv/20210617_Cs
Write File Counts. (ex. [19990708_Eu000003.bin] -> 3)

>> 1
```


## フォルダ階層
```
.
├── data
│   ├── [beta-gamma]ch_diff_txt
│   │   ├── {指定時間}ns_{ファイル名}
│   │   └── ...
│   │
│   ├── [beta-gamma]time_diff_csv
│   ├── [beta-gamma]time_diff_txt
│   ├── calibration_csv
│   ├── ch_diff
│   ├── experiment_data
│   │   ├── ※ 実験データを入れる
│   │   └── ...
│   │
│   ├── simultaneous_csv
│   ├── simultaneous_txt
│   ├── single_analysis_txt
│   │   ├── {ファイル名}
│   │   └── ...
│   │
│   ├── sum_csv
│   ├── sum_txt
│   ├── time_diff_txt
│   └── time_sort_csv
│ 
├── clover_package
│   └── clover_package.py
│ 
├── export_data.bin
├── export_data.csv
├── GeCalibration.txt
│ 
├── bin_to_csv...
│ 
├── add_back.py
├── APV8016_calib.py
├── beta_gamma_ch_diff.py
├── beta_gamma_time_diff.py
├── ch_diff.py
├── main.py
├── simultaneous.py
├── single_analysis.py
├── single_sum.py
├── time_difference.py
└── time_sort.py
...

```