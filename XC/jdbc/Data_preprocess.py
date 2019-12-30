import pandas as pd
import time
import datetime


def time12to24(time_string):
    ins = time_string.strip()

    is_pm = ins[-2:] == '下午'
    time_list = list(map(int, ins[:-2].split(':')))

    if is_pm and time_list[0] < 12:
        time_list[0] += 12

    if not is_pm and time_list[0] == 12:
        time_list[0] = 0

    return ':'.join(map(lambda x: str(x).rjust(2, '0'), time_list))


# print(time12to24('12:02:58上午'))


def date_drop_hanzi(JGSJ_date):
    str_list = JGSJ_date.split(sep='-')
    str_new = '20' + str_list[2] + '-' + str_list[1][:-1] + '-' + str_list[0]
    return str_new


print(date_drop_hanzi('20-12月-19'))


def time_drop_hanzi(JGSJ_time):
    str_list = JGSJ_time.split(sep='.')
    str_new = str_list[0] + ':' + str_list[1] + ':' + str_list[2] + str_list[3][-2:]
    return str_new


print(time_drop_hanzi('12.02.58.158000 上午'))
path = 'D:\\宣城二小\\二小数据\\3481东往西（12月20日及往后）.csv'   # 改文件路径名称
df = pd.read_csv(path,
                 usecols=['LANE_NO', 'PLATE_NO', 'PASS_TIME', 'PLATE_COLOR'],
                 encoding="utf-8")
df.rename(columns={
    'LANE_NO': 'CDBH',
    'PLATE_NO': 'HPHM',
    'PASS_TIME': 'JGSJ',
    'PLATE_COLOR': 'HPZL'
},
          inplace=True)
df = df[df['HPHM'] != '车牌'].reset_index(drop=True)
df['JGSJ_date'], df['JGSJ_time'] = df['JGSJ'].str.split(' ', 1).str
df['JGSJ_date'] = df['JGSJ_date'].apply(date_drop_hanzi)
df['JGSJ_time'] = df['JGSJ_time'].apply(time_drop_hanzi)
df['JGSJ_time'] = df['JGSJ_time'].apply(time12to24)
df['JGSJ'] = df['JGSJ_date'] + ' ' + df['JGSJ_time']
df['JGSJ'] = pd.to_datetime(df['JGSJ'], format='%Y-%m-%d %H:%M:%S')
df['SSID'] = 'F022'     # 新的数据改这一行
df = df[['SSID', 'HPHM', 'HPZL', 'JGSJ', 'CDBH']]
print(df.head(10))
print(df.dtypes)
df.to_csv('D:\\宣城二小\\二小数据\\F022_12.csv', sep=',', encoding="utf_8_sig",index=False) # 改这一行的输出文件名称
