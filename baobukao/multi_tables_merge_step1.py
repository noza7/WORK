import pandas as pd

from baobukao.lib.func import get_file_name, del_exits_file, writer_branch_table

# 删除已存在的文件
del_exits_file('补考汇总表.xlsx')


def output_data(path):
    '''
    获取汇总数据存入excel表格
    :param path: 传入多表路径
    :return:
    '''
    # todo 获取表名
    file_ls_ = get_file_name(path)
    file_ls = []
    for i in file_ls_:
        j = path + '/' + i
        file_ls.append(j)
    # todo 多表拼接
    # 表名列表
    df_ls = []
    for i in range(len(file_ls)):
        df_ls.append('df{}'.format(i))
    # 读取所有表
    for i in range(len(file_ls)):
        df_ls[i] = pd.read_excel(io=file_ls[i], sheet_name=0)
    # 表格拼接
    df = pd.concat(df_ls, ignore_index=True)
    df = df.astype(str)
    # todo ID补零
    # df['ID'] = df['ID'].str.center(5, fillchar='0')
    df['ID'] = df['ID'].str.rjust(5, fillchar='0')
    # print(df['ID'])
    # 创建新表的路径文件名
    path_result = 'temp/补考汇总表.xlsx'
    # 写入数据
    writer = pd.ExcelWriter(path_result)
    df.to_excel(writer, '汇总', index=False)
    writer.save()
    writer_branch_table(table_path=path_result, sheetname='专')
    writer_branch_table(table_path=path_result, sheetname='本')


path = 'temp/2019秋补考报名表'  # 文件夹路径
output_data(path)
