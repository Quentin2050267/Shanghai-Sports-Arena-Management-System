from flask import Flask, render_template, request, redirect, jsonify, session, url_for
from flask.views import MethodView
import functools
import pymysql
from flask_cors import CORS
from datetime import date, timedelta, datetime, timezone
import json

from mylib.dbConfig import localSourceConfig as localConfig

localSourceConfig = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'passwd': 'Ab123456',
    'db': 'sports_facility_management',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor
}

# 连接数据库
config = localConfig


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


class GYMapi(MethodView):
    def __init__(self):
        # self.gym_id_list_mapping = {}
        cursor.execute('SELECT * FROM gym')
        self.results = cursor.fetchall()
        # 遍历每个gym_id，并查询其对应的列表
        for i, single in enumerate(self.results):
            gym_id = single['gym_id']
            query = f"SELECT facility_name FROM facility WHERE gym_id = '{gym_id}'"
            cursor.execute(query)
            res = cursor.fetchall()
            facility_list = [result['facility_name'] for result in res]  
            self.results[i]['facility'] = facility_list
            # self.gym_id_list_mapping[gym_id] = facility_list

    def get(self, gym_id):
        if not gym_id:
            # cursor.execute('SELECT * FROM gym')
            # results = cursor.fetchall()
            return {
                'status': 'success',
                'message': '数据库查询成功',
                'results': self.results,
                # 'facility': self.gym_id_list_mapping
            }
        else:
            cursor.execute("SELECT * FROM gym where gym_id = %s;", gym_id)
            results = cursor.fetchone()
            return {
                'gym_id': results['gym_id'],
                'gym_district': results['gym_district'],
                'gym_name': results['gym_name'],
                'gym_address': results['gym_address'],
                # 'facility': self.gym_id_list_mapping[results['gym_id']]
            }

    def delete(self, gym_id, facility_name=None):
        # 如果是删除facility
        if facility_name:
            # facility_id是外键，先查询facility_id
            cursor.execute("select facility_id FROM facility where gym_id = %s and facility_name = %s;", (gym_id, facility_name))
            results = cursor.fetchall()
            for facility in results:
                facility_id = facility['facility_id']
                # 删除time_slot中facility_id
                cursor.execute(
                    "DELETE FROM time_slot where facility_id = %s;", facility_id)
                cursor.execute("DELETE FROM facility where facility_id = %s;", facility_id)
                db.commit()

            # db.commit()
            return{
                'status': 'success',
                'message': '数据删除成功',
            }
        cursor.execute(
            'SELECT facility_id FROM facility WHERE gym_id = %s', gym_id)
        results = cursor.fetchall()
        for facility in results:
            facility_id = facility['facility_id']
            # 删除time_slot中facility_id
            cursor.execute(
                "DELETE FROM time_slot where facility_id = %s;", facility_id)
            db.commit()
            # 删除reservation中facility_id
            cursor.execute(
                "DELETE FROM reservation where facility_id = %s;", facility_id)
            db.commit()

        cursor.execute("DELETE FROM facility where gym_id = %s;", gym_id)
        cursor.execute("DELETE FROM gym where gym_id = %s;", gym_id)
        db.commit()
        return{
            'status': 'success',
            'message': '数据删除成功',
        }

    def post(self):
        form = request.json
        gym_district = form.get('gym_district')
        gym_name = form.get('gym_name')
        gym_address = form.get('gym_address')
        facility = form.get('facility_single', False)
        gym_id = form.get('gym_id', False)
        reservation_date = form.get('reservation_date', False)
        reservation_facility = form.get('facility', False)
        schedule_date = form.get('schedule_date', False)
        schedule_time = form.get('schedule_time', False)
        user_id = form.get('user_id', False)
        
        # 插入reservation表
        if reservation_date:
            # 查一下facility_id
            cursor.execute("SELECT facility_id FROM facility WHERE facility_name = %s and gym_id = %s ",(reservation_facility, gym_id))
            facility_id = cursor.fetchone()['facility_id']
            # 检查一下重复插入
            cursor.execute("SELECT COUNT(*) FROM reservation WHERE user_id = %s and facility_id = %s and schedule_date = %s and schedule_time = %s and reservation_date = %s",(user_id, facility_id, schedule_date, schedule_time, reservation_date))
            result = cursor.fetchone()
            if result['COUNT(*)']:
                return{
                    'status': 'failure',
                    'message': '数据添加失败',
                }
            cursor.execute("insert into reservation (user_id, facility_id, schedule_date, schedule_time, reservation_date, status) values(%s,%s,%s,%s,%s,%s)",(user_id, facility_id, schedule_date, schedule_time, reservation_date, 1))
            db.commit()
            return{
                'status': 'success',
                'message': '数据添加成功',
            }

        if facility:
            # 检查一下重复插入
            cursor.execute("SELECT COUNT(*) FROM facility WHERE gym_id = %s and facility_name = %s ",(gym_id, facility))
            result = cursor.fetchone()
            if result['COUNT(*)']:
                return{
                    'status': 'failure',
                    'message': '数据添加失败',
                }
            cursor.execute("insert into facility (gym_id, facility_name) values(%s,%s)",(gym_id, facility))
            db.commit()
            return{
                'status': 'success',
                'message': '数据添加成功',
            }


        # 检查一下重复插入
        cursor.execute("SELECT COUNT(*) FROM gym WHERE gym_district = %s and gym_name = %s and gym_address = %s ",
                       (gym_district, gym_name, gym_address))
        result = cursor.fetchone()
        if result['COUNT(*)']:
            return{
                'status': 'failure',
                'message': '数据添加失败',
            }
        cursor.execute("insert into gym (gym_district, gym_name, gym_address) values(%s,%s,%s)",
                       (gym_district, gym_name, gym_address))
        db.commit()
        return{
            'status': 'success',
            'message': '数据添加成功',
        }

    def put(self, gym_id):
        form = request.json
        gym_district = form.get('gym_district')
        gym_name = form.get('gym_name')
        gym_address = form.get('gym_address')


        if not gym_id:  # gym_id=0做查询
            # 模糊查询
            cursor.execute(
                "SELECT * FROM gym WHERE gym_name LIKE %s;", '%'+gym_name+'%')
            results = cursor.fetchall()

            # 再从results中找出相应在self.results中的记录
            matching_records = [record for record in self.results if record['gym_id'] in [result['gym_id'] for result in results]]

            return{
                'status': 'success',
                'message': '数据查询成功',
                'results': matching_records
            }
        
        cursor.execute("UPDATE gym SET gym_district = %s,gym_name = %s,gym_address = %s WHERE gym_id = %s",
                       (gym_district, gym_name, gym_address, gym_id))
        db.commit()
        return{
            'status': 'success',
            'message': '数据修改成功',
        }

class USERapi(MethodView):
    def get(self, user_id):
        if not user_id:
            cursor.execute('SELECT * FROM user')
            results = cursor.fetchall()
            return {
                'status': 'success',
                'message': '数据库查询成功',
                'results': results
            }
        else:
            cursor.execute("SELECT * FROM user where user_id = %s;", user_id)
            results = cursor.fetchone()
            return {
                'user_id': results['user_id'],
                'user_name': results['user_name'],
                'user_email': results['user_email'],
                'user_phone': results['user_phone'],
                'user_password': results['user_password'],
                'user_type': results['user_type'],
            }

    def delete(self, user_id):
        cursor.execute(
            "DELETE FROM reservation where user_id = %s;", user_id)
        db.commit()
        cursor.execute("DELETE FROM user where user_id = %s;", user_id)
        db.commit()
        return{
            'status': 'success',
            'message': '数据删除成功',
        }

    def post(self):
        form = request.json
        user_id = form.get('user_id')
        user_name = form.get('user_name')
        user_email = form.get('user_email')
        user_phone = form.get('user_phone')
        user_password = form.get('user_password')
        user_type = form.get('user_type')

        # 检查一下重复插入
        cursor.execute("SELECT COUNT(*) FROM user WHERE user_id = %s", user_id)
        result = cursor.fetchone()
        if result['COUNT(*)']:
            return{
                'status': 'failure',
                'message': '数据添加失败',
            }
        cursor.execute("insert into user (user_id, user_name, user_email, user_phone, user_password, user_type) values(%s,%s,%s,%s,%s,%s)",
                    (user_id, user_name, user_email, user_phone, user_password, user_type))
        db.commit()
        return{
            'status': 'success',
            'message': '数据添加成功',
        }
       

    def put(self, user_id):
        form = request.json
        user_id = form.get('user_id')
        user_name = form.get('user_name')
        user_email = form.get('user_email')
        user_phone = form.get('user_phone')
        user_password = form.get('user_password')
        user_type = form.get('user_type')

        if not user_id:  # gym_id=0做查询
            # 模糊查询
            cursor.execute(
                "SELECT * FROM user WHERE user_name LIKE %s;", '%'+user_name+'%')
            results = cursor.fetchall()
            return{
                'status': 'success',
                'message': '数据查询成功',
                'results': results
            }
        # 数据修改
        cursor.execute("UPDATE user SET user_name = %s , user_email = %s , user_phone = %s , user_password = %s , user_type = %s WHERE user_id = %s",
                       (user_name, user_email, user_phone, user_password, user_type, user_id))
        db.commit()

        cursor.execute(
                "SELECT * FROM user WHERE user_id = %s;", user_id)
        re = cursor.fetchall()
        return{
            'status': 'success',
            'message': '数据修改成功',
        }

class LOGINapi(MethodView):
    def post(self):
        form = request.json
        username = form.get('username')
        password = form.get('password')

        # 检查一下重复插入
        query = "SELECT * FROM user WHERE user_name = %s AND user_password = %s"
        cursor.execute(query, (username, password))

        # 获取查询结果
        result = cursor.fetchone()
        # 判断是否找到匹配的记录
        if result:
            user_type = result['user_type']
            user_id = result['user_id']
            return {
                'message': 'Login Successfully',
                'status':True,
                'user_type': user_type,
                'user_id': user_id
                }
        else:
            return {
                'message': 'Please check your name and passward',
                'status':False
                }
        
class FACTIMEapi(MethodView):
    def get(self, gym_id, facility_name):
        cursor.execute('SELECT facility_id FROM facility where gym_id=%s and facility_name=%s;', (gym_id, facility_name))
        result = cursor.fetchone()
        facility_id = result['facility_id']
        # self.facility_id = facility_id
        cursor.execute('SELECT * FROM time_slot where facility_id=%s;', facility_id)
        results = cursor.fetchall()


        converted_result = []
        for record in results:
            converted_record = {
                'date': record['date'].isoformat(),
                'start_time': record['start_time'].total_seconds(),
                'end_time': record['end_time'].total_seconds(),
            }
            converted_result.append(converted_record)

        
        return {
            'results': converted_result,
            'facility_id': facility_id
            }


    def delete(self, time_id):
        cursor.execute("DELETE FROM time_slot where time_id = %s ;", time_id)
        db.commit()
        return{
            'status': 'success',
            'message': '数据删除成功',
        }

    def post(self):
        form = request.json

        date = form.get('date')
        start_time = form.get('start_time')
        end_time = form.get('end_time')
        facility_id = form.get('facilityID')


        # 将字符串转换为 datetime 对象
        date_obj = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
        start_time_obj = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%fZ')
        end_time_obj = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S.%fZ')
        

        date_obj = date_obj.astimezone() + timedelta(hours=8)
        start_time_obj = start_time_obj.astimezone()+ timedelta(hours=8)
        end_time_obj = end_time_obj.astimezone()+ timedelta(hours=8)

        
        # 提取日期和时间
        date = date_obj.strftime('%Y-%m-%d')
        start_time = start_time_obj.strftime('%H:%M:%S')
        end_time = end_time_obj.strftime('%H:%M:%S')

        # 检查一下重复插入
        cursor.execute("SELECT COUNT(*) FROM time_slot WHERE date = %s and start_time = %s and end_time = %s and facility_id = %s",
                       (date, start_time, end_time, facility_id))
        result = cursor.fetchone()
        if result['COUNT(*)']:
            return{
                'status': 'failure',
                'message': '数据添加失败',
            }
        cursor.execute("insert into time_slot (date, start_time, end_time, facility_id) values(%s,%s,%s,%s)",
                       (date, start_time, end_time, facility_id))
        db.commit()
        return{
            'status': 'success',
            'message': '数据添加成功',
        }
    
    def put(self, time_id=None):        
        form = request.json
        date = form.get('date')
        start_time = form.get('start_time')
        end_time = form.get('end_time')
        facility_id = form.get('facility_id')
        # 如果有time_id，做数据修改
        if time_id:
            # 将字符串转换为 datetime 对象
            date_obj = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
            start_time_obj = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%fZ')
            end_time_obj = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S.%fZ')
            
            date_obj = date_obj.astimezone() + timedelta(hours=8)
            start_time_obj = start_time_obj.astimezone()+ timedelta(hours=8)
            end_time_obj = end_time_obj.astimezone()+ timedelta(hours=8)

            
            # 提取日期和时间
            date = date_obj.strftime('%Y-%m-%d')
            start_time = start_time_obj.strftime('%H:%M:%S')
            end_time = end_time_obj.strftime('%H:%M:%S')
            # 检查一下重复插入
            cursor.execute("SELECT COUNT(*) FROM time_slot WHERE date = %s and start_time = %s and end_time = %s and facility_id = %s;", (date, start_time, end_time, facility_id))
            result = cursor.fetchone()
            if result['COUNT(*)']:
                return{
                    'status': 'failure',
                    'message': '数据添加失败',
                }
            cursor.execute("UPDATE time_slot SET date = %s , start_time = %s , end_time = %s , facility_id = %s where time_id =%s;",
                       (date, start_time, end_time, facility_id, time_id))
            # cursor.execute("insert into time_slot (date, start_time, end_time, facility_id) values(%s,%s,%s,%s)",(date, start_time, end_time, facility_id))
            db.commit()
            return{
                'status': 'success',
                'message': '数据添加成功',
            }
        # 否则做查询time_id
        cursor.execute(
                "SELECT time_id FROM time_slot WHERE date = %s and start_time = %s and end_time = %s and facility_id = %s;", (date, start_time, end_time, facility_id))
        results = cursor.fetchone()
        return{
            'time_id':results['time_id']
        }

class RESapi(MethodView):
    def get(self, user_id):
        if not user_id:
            cursor.execute("SELECT * FROM reservation;")
            results = cursor.fetchall()
            new_re = results
            for index, result in enumerate(results):
                facility_id = result['facility_id']
                cursor.execute("SELECT * FROM facility where facility_id = %s;", facility_id)
                singleFacility = cursor.fetchone()
                gym_id = singleFacility['gym_id']
                facility_name = singleFacility['facility_name']
                cursor.execute("SELECT gym_name FROM gym where gym_id = %s;", gym_id)
                gym_name = cursor.fetchone()['gym_name']
                new_re[index]['facility_name'] = facility_name
                new_re[index]['gym_name'] = gym_name
            return {
                    'status': 'success',
                    'message': '数据库查询成功',
                    'results': new_re,
                }

        cursor.execute("SELECT * FROM reservation where user_id = %s;", user_id)
        results = cursor.fetchall()
        new_re = results
        for index, result in enumerate(results):
            facility_id = result['facility_id']
            cursor.execute("SELECT * FROM facility where facility_id = %s;", facility_id)
            singleFacility = cursor.fetchone()
            gym_id = singleFacility['gym_id']
            facility_name = singleFacility['facility_name']
            cursor.execute("SELECT gym_name FROM gym where gym_id = %s;", gym_id)
            gym_name = cursor.fetchone()['gym_name']
            new_re[index]['facility_name'] = facility_name
            new_re[index]['gym_name'] = gym_name
        return {
                'status': 'success',
                'message': '数据库查询成功',
                'results': new_re,
            }
    
    def put(self, reservation_id):
        form = request.json
        status = form.get('status')
        cursor.execute("UPDATE reservation SET status = %s WHERE reservation_id = %s", (status, reservation_id))
        db.commit()
        return {
            'status': 'success',
            'message': '数据修改成功',
        }
     


app = Flask(__name__)
CORS(app)
app.secret_key = 'bfnaklmmocpanvonenbv98q3r'


gym_view = GYMapi.as_view('gym_api')
app.add_url_rule('/gym/', defaults={'gym_id': None},
                 view_func=gym_view, methods=['GET', 'POST'])
app.add_url_rule('/gym/', view_func=gym_view, methods=['POST', ])
app.add_url_rule('/gym/<int:gym_id>', view_func=gym_view,
                 methods=['GET', 'PUT', 'DELETE'])
app.add_url_rule('/gym/<int:gym_id>/<facility_name>', view_func=gym_view,
                 methods=['DELETE'])

user_view = USERapi.as_view('user_api')
app.add_url_rule('/user/', defaults={'user_id': None},
                 view_func=user_view, methods=['GET', 'POST'])
app.add_url_rule('/user/', view_func=user_view, methods=['POST', ])
app.add_url_rule('/user/<user_id>', view_func=user_view,
                 methods=['GET', 'PUT', 'DELETE'])

login_view = LOGINapi.as_view('login_api')
app.add_url_rule('/login/', view_func=login_view, methods=['POST', ])

factime_view = FACTIMEapi.as_view('factime_api')
app.add_url_rule('/page1/<int:gym_id>/<facility_name>', view_func=factime_view,
                 methods=['GET', 'PUT'])
app.add_url_rule('/page1/', view_func=factime_view,
                 methods=['POST'])
app.add_url_rule('/page1/<int:time_id>', view_func=factime_view,
                 methods=['DELETE', 'PUT'])
app.add_url_rule('/page1/', view_func=factime_view,
                 methods=['PUT'])

reservation_view = RESapi.as_view('reservation_api')
app.add_url_rule('/reservation/', defaults={'user_id': None},
                 view_func=reservation_view, methods=['GET', 'POST'])
app.add_url_rule('/reservation/<int:reservation_id>', view_func=reservation_view, methods=['PUT', ])
app.add_url_rule('/reservation/<int:user_id>', view_func=reservation_view,
                 methods=['GET', 'PUT', 'DELETE'])
# app.add_url_rule('/gym/<int:gym_id>/<facility_name>', view_func=gym_view,
#                  methods=['DELETE'])


if __name__ == '__main__':
    app.run()
    cursor.close()
    db.close()
