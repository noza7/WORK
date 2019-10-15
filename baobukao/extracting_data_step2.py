import xlrd

from baobukao.lib.func import del_exits_file

path = 'temp/补考汇总表.xlsx'
sheet_name = '专'
# sheet_name = '本'

'''
提取学号列表和对应信息列表
参数path：文件路径
参数sheet_name：文件名
'''


def get_student_info(path, sheet_name):
    '''
    获取学生信息
    :param path: 文件路径
    :param sheet_name: 表名
    :return: 学号列表，数据字典列表
    '''
    student_nums = []
    # 提取对应信息
    data_dict_ls = []
    wb = xlrd.open_workbook(path)
    sheet = wb.sheet_by_name(sheet_name)
    data_len = sheet.nrows
    for i in range(1, data_len):
        student_num = str(sheet.cell(i, 1).value)
        data = []
        data.append(sheet.cell(i, 1).value)
        data.append(sheet.cell(i, 2).value)
        data.append(sheet.cell(i, 0).value)
        data.append(sheet.cell(i, 4).value)
        student_nums.append(student_num)
        data_dict_ls.append(data)
    return student_nums, data_dict_ls


# 提取学号列表
student_nums = get_student_info(path, sheet_name)[0]
# 提取信息列表
ls = get_student_info(path, sheet_name)[1]


def get_unique_student_nums(student_nums):
    '''
    按顺序列表去重，获取唯一学号列表
    :param student_nums: 学号列表
    :return: 唯一学号列表
    '''
    unique_student_nums = []
    for i in student_nums:
        if i not in unique_student_nums:
            unique_student_nums.append(i)
    return unique_student_nums


# 获取唯一学号列表
unique_student_nums = get_unique_student_nums(student_nums)


def get_data(unique_student_nums, ls):
    '''
    获取数据结构
    :param unique_student_nums: 学号去重后的唯一值列表，顺序与原顺序相同
    :param ls: 所有数据信息
    :return:
    '''
    dict_ls = []
    for student_num in unique_student_nums:
        # 创建一个空列表，用来存储相同学号的所有课程信息
        ls_i = []
        # 查询所有数据，如果学号相同，就汇总，并以列表形式存入ls_i
        for i in range(len(ls)):
            if student_num == ls[i][0]:
                ls_i.append(ls[i][1:])

        # 创建一个空列表，用于转换学号值为列表
        ls_x = []
        # 把学号填入列表中
        ls_x.append(student_num)

        # 创建空列表，把ls_i作为整体加进去
        ls_y = []
        ls_y.append(ls_i)

        # 转换为字典
        get_dict = dict(zip(ls_x, ls_y))
        # 写入结果列表
        dict_ls.append(get_dict)
    return dict_ls


# 获取需要的字典结构
dict_ls = get_data(unique_student_nums, ls)

# todo 写入文件
# 删除已有文件
del_exits_file('temp/data.py')


# 写入路径并输出
def output_data(ls):
    with open('temp/data.py', 'a+', encoding="utf-8") as f:
        # f.write('# -*- coding: utf-8 -*-\n')
        # f.write('# coding=gbk\n\n')
        f.write('dict_ls = [')
        for i in ls:
            # print(i)
            f.write(str(i) + ', ')
        f.write(']')
        f.write('\n\n')
        f.write('student_nums = [')
        for j in ls:
            key = str(list(j.keys())[0])
            print(key)
            f.write('\'' + key + '\'' + ', ')
        f.write(']')
        # for j in


print(dict_ls)
# print(ls[0][0])
output_data(dict_ls)
