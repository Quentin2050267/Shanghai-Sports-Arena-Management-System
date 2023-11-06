import pandas as pd
import re
import pymysql
from mylib.dbConfig import localSourceConfig as localConfig
import jieba
from datetime import datetime, timedelta
config = localConfig


df = pd.read_excel('上海市春节公共体育设施信息查询2022.xlsx')
print(df.columns)


# 连接数据库
db = pymysql.connect(
    host=config['host'],
    port=config['port'],
    user=config['user'],
    passwd=config['passwd'],
    db=config['db'],
    charset=config['charset'],
    cursorclass=config['cursorclass']
)
cursor = db.cursor()

# # 刷新表
# sql_file = '../SQL/create_tables.sql'
# with open(sql_file, 'r', encoding='utf-8') as f:
#     sql_script = f.read()
# print(sql_script)
# cursor.execute(sql_script)

# 填充gym表
for record in df.iloc:
    gym_district = record['区'].strip()
    gym_name = record['设施名称'].strip().replace(' ', '').strip('1')
    gym_address = record['地址'].strip()
    cursor.execute("SELECT COUNT(*) FROM gym WHERE gym_name = %s;", gym_name)
    result = cursor.fetchone()
    if not result['COUNT(*)']:
        try:
            cursor.execute("insert into gym (gym_district, gym_name, gym_address) values(%s,%s,%s)", (gym_district, gym_name, gym_address))
            db.commit()
        except Exception as e:
            print(e)
print('gym表填充完毕')


def standardize(item=str):
    item = re.sub(',\n', ',', item.replace('：', ':').replace('，', ',').replace('      ', '\n')).replace('（', '(').\
        replace('）', ')')
    item = item.replace(' ', '').replace('；', ';')
    item = item.split('\n')
    item = list(filter(lambda i: i != '', item))
    item = '\n'.join(item).replace(' ', '')
    item = re.sub(r'\(.*?\)', '', item)
    item = item.replace('馆', '').replace('室内', '').replace('场', '').replace('室外', '').replace('器械', '健身').replace(
        '房', '').replace('池', '').replace('~', '-').replace('—', '-').replace('至', '-').replace('、', ';').\
        replace(',', ';').replace('室外', '').replace('室', '').replace('－', '-').replace('乒乓', '乒乓球').\
        replace('田径', '跑步').replace('跑道', '跑步').replace('斯诺克', '台球').replace('滑轮', '溜冰').replace('滑轮', '滑冰').\
        replace('乒乓球球', '乒乓球').replace('健身健身', '健身').replace('步道', '跑步').replace('市民', '')
    return item


total = set()
for index, item in enumerate(df['开放项目时间'].iloc):
    item = standardize(item)
    word_list = jieba.lcut(item)
    # 定义正则表达式，匹配中文字符
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    pattern.findall(item)
    chinese_list = pattern.findall(' '.join(word_list))
    chinese_list = [x for x in chinese_list if len(x) > 1]
    sports_list = set(filter(lambda i: i not in '综合公园关闭时间以上国民上午小时全天恢复全部苑点日至测试点正常日起开始恢复正常市民区域日休暂'
                                                '停其余中心智慧接种维修期间每限团共享公益苑及对外开放所有灯光长者外地下午户外广等日日占用'
                                                '温水营业全天候预约休息开放活动放假日闭疫苗监测非标春节项目笼式设施体育锻炼训练', chinese_list))
    total |= sports_list
    # print(sports_list)
    # 插入值
    for sports in sports_list:
        facility_name = sports
        gym_name = df['设施名称'][index].strip().replace(' ', '').strip('1')
        cursor.execute("SELECT gym_id FROM gym WHERE gym_name = %s;", gym_name)
        result = cursor.fetchone()
        gym_id = result['gym_id']
        cursor.execute("SELECT COUNT(*) FROM facility WHERE facility_name = %s and gym_id = %s;", (facility_name, gym_id))
        result = cursor.fetchone()

        if not result['COUNT(*)']:
            try:
                cursor.execute("insert into facility (facility_name, gym_id) values(%s,%s)", (facility_name, gym_id))
                db.commit()
            except Exception as e:
                print(e)
print('facility表填充完毕')
print('其中运动设施有：', total)


def insert(pos, string1, string2):
    str_before = string1[:pos]
    str_after = string1[pos:]
    new_str = str_before + string2 + str_after
    return new_str


time_span = set()
for index, item in enumerate(df['开放项目时间'].iloc):
    item = standardize(item)
    # 使用正则表达式匹配24小时制时间段
    pattern1 = r"(2[0-3]|[01]?[0-9]|[1-9]):([0-5]?[0-9])-(2[0-3]|[01]?[0-9]|[1-9]):([0-5]?[0-9])"

    new_item_list = []
    for exercise in item.split('\n'):
        matches = re.finditer(pattern1, exercise)

        insert_pos = []
        for match in matches:
            start, end = match.span()
            insert_pos.append(start)

        offset = 0
        for pos in insert_pos:
            # 计算新的插入位置
            new_pos = pos + offset
            if exercise[new_pos-1] == ':' and exercise[new_pos-2] != '日':
                exercise = insert(new_pos, exercise, '1月31日-2月6日')
                offset += len('1月31日-2月6日')
            elif exercise[new_pos-1] == '0':
                exercise = insert(new_pos, exercise, ';')
                offset += 1
        new_item_list.append(exercise)

    # print(new_item_list)
    for i, _ in enumerate(new_item_list):
        matches = re.finditer(pattern1, new_item_list[i])
        delete_pos = []
        for match in matches:
            start, end = match.span()
            delete_pos.append(start)
        offset = 0
        for pos in delete_pos:
            new_pos = pos + offset
            if new_item_list[i][new_pos - 1] == ':':
                tmp = list(new_item_list[i])
                tmp[new_pos - 1] = '/'
                new_item_list[i] = ''.join(tmp)
                # new_item_list[i] = new_item_list[i][:new_pos - 1] + new_item_list[i][new_pos:]
                # offset -= 1
            elif new_item_list[i][new_pos - 1] == '日':
                new_item_list[i] = insert(new_pos, new_item_list[i], '/')
                offset += 1

    # 如果time_span之前是; 那么此time_span的date就和之前一个time_span的date相同
    # print(index + 2)
    # print(new_item_list)
    for bb, sport_time in enumerate(new_item_list):
        # print(sport_time)
        sport = sport_time.split(':', 1)[0]
        try:
            time = sport_time.split(':', 1)[1]
        except:
            time = None
        if time:
            new_item_list[bb] = time.split(';')
            # new_item_list[i] = [sport + ':' + x for x in time.split(';')]
            # print(new_item_list[i])
            # 2月1日-2日
            pattern2 = r'(\d{1,2})月(\d{1,2})日-(\d{1,2})日'
            # 2月3日-2月6日
            pattern3 = r'(\d{1,2}月\d{1,2}日)-(\d{1,2}月\d{1,2}日)'
            for j, x in enumerate(new_item_list[bb]):
                if '/' in x:
                    date = x.split('/')[0]
                else:
                    new_item_list[bb][j] = (date+'/') + new_item_list[bb][j]
            new_item_list[bb] = [sport + ':' + x for x in new_item_list[bb]]
            # print(new_item_list[bb])

            final_time = []
            for j, x in enumerate(new_item_list[bb]):
                match1 = re.findall(pattern2, x)
                match2 = re.findall(pattern3, x)
                tmp = new_item_list[bb][j]
                if match1:
                    month_start, day_start, day_end = match1[0]
                    final = []
                    # new_item_list[bb].remove(tmp)
                    for k in range(int(day_start), int(day_end) + 1):
                        date = f'{month_start}月{k}日'
                        # print(date)
                        sport = tmp.split(':')[0]
                        tmp_time_span = tmp.split('/')[1]
                        final.append(sport + ':' + date + '/' + tmp_time_span)
                    final_time += final
                elif match2:
                    # print(match2)
                    start_date, end_date = match2[0]
                    start_date = datetime.strptime(start_date, "%m月%d日")
                    end_date = datetime.strptime(end_date, "%m月%d日")

                    # 计算日期差
                    delta = end_date - start_date
                    num_days = delta.days + 1  # 包括起始日期和结束日期

                    final = []
                    # 遍历日期范围内的每一天，并打印出来
                    for nn in range(num_days):
                        day = start_date + timedelta(days=nn)
                        date = day.strftime("%m月%d日")
                        # print(date)
                        sport = tmp.split(':')[0]
                        tmp_time_span = tmp.split('/')[1]
                        final.append(sport + ':' + date + '/' + tmp_time_span)
                    final_time += final
                else:
                    final_time.append(tmp)
        else:
            final_time = []

        # print(final_time)
        gym_name = df['设施名称'][index].strip().replace(' ', '').strip('1')
        for every_sport_time in final_time:
            tmp = every_sport_time.replace(':', '*', 1)
            facility_name = tmp.split('*')[0]
            # try:
            facility_time = tmp.split('*')[1]
            time_ = facility_time.split('/')[1]
            date_ = datetime.strptime('22年'+facility_time.split('/')[0], '%y年%m月%d日').date()
            start_time = datetime.strptime(time_.split('-')[0], '%H:%M').time()
            end_time = datetime.strptime(time_.split('-')[1], '%H:%M').time()
            # print(date_, start_time, end_time)

            # 执行SQL语句，查询符合条件的facility_id
            query = """
            SELECT facility.facility_id
            FROM gym 
            JOIN facility ON gym.gym_id = facility.gym_id 
            WHERE gym.gym_name = '{}' AND facility.facility_name = '{}'
            """.format(gym_name, facility_name)
            cursor.execute(query)
            # 获取查询结果
            facility_id = cursor.fetchone()['facility_id']

            cursor.execute("SELECT COUNT(*) FROM time_slot WHERE date = %s and start_time = %s and end_time = %s and facility_id = %s",
                           (date_, start_time, end_time, facility_id))
            result = cursor.fetchone()
            if not result['COUNT(*)']:
                cursor.execute("insert into time_slot (date, start_time, end_time, facility_id) values(%s,%s,%s,%s)",
                               (date_, start_time, end_time, facility_id))
                db.commit()
            # except:
            #     pass

print('time_slot表填充完毕')

cursor.close()
db.close()


