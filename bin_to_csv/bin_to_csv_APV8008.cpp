#include "math.h"
#include "stdio.h"
#include "stdlib.h"

int main(int argc, char *argv[]) {
    // 変数定義
    int det[4], Tape, adc, ch, unit, list_num;
    unsigned short B[5];
    double t1, t2, t3, ts;
    char list_name[256], pro_name[256], i_file[256];
    FILE *fcal, *fi, *fo;

    // 使用ファイルなどの入力引受
    printf("Write File Name. (ex. [19990708_Eu000001.bin] -> 19990708_Eu)\n");
    scanf("%s", &i_file);
    printf("Write File Counts. (ex. [19990708_Eu000003.bin] -> 3)\n");
    scanf("%d", &list_num);

    // ch定義ファイル読み込み
    fcal = fopen("GeCalibration.txt", "r");
    fscanf(fcal, "%d %d %d %d %d\n", &det[0], &det[1], &det[2], &det[3], &Tape);
    fclose(fcal);

    // 使用ファイルをforにて開く
    for(int i = 1; i <= list_num; i++) {
        sprintf(list_name, "%s%0.6d.bin", i_file, i);
        fi = fopen(list_name, "rb");

        if(fi == NULL) {
            printf("Error: Not Exist Such as File.\n");
            break;
        } else {
            printf("%s is open...\n", list_name);
        }

        sprintf(pro_name, "%s%0.6d.csv", i_file, i);
        fo = fopen(pro_name, "w");
        fprintf(fo, "t1,t2,t3,ts,ch,unit,adc\n");

        while((fread(B, sizeof(unsigned short), 5, fi)) == 5) {
            for(int j = 0; j < 5; j++) {
                B[j] = B[j] << 8 | B[j] >> 8;
            }

            t1 = B[0] << 28;
            t2 = B[1] << 12;
            t3 = B[2] >> 4;
            ts = B[2] & 0xf;
            ch = B[4];
            unit = B[4] >> 3;
            adc = B[3] & 0xf;

            fprintf(fo, "%lf,%lf,%lf,%lf,%d,%d,%d\n", t1, t2, t3, ts, ch, unit,
                    adc);
        }
        fclose(fo);
        fclose(fi);
    }

    printf("Finished Reading List Data.\n");

    return 0;
}