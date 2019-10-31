#!/usr/bin/env python
# coding:utf-8
import datetime
import mysql.connector
import logging



class MysqlHelper(object):

    def check_lgt_lat(self):
        try:
            cur.execute("select longitude,latitude from city_point_tbl where city_english_name='xiamenshi';")
            return cur.fetchall()

        except Exception as e:
            self.mysql_msg(e)
            return self.check_lgt_lat()

    def save_lgt_lat_page(self, lgt, lat):
        try:
            sql = "INSERT INTO meituan_city_point (longitude,latitude) VALUES ('{0}','{1}')"
            cur.execute(sql.format(lgt, lat))
            cnx.commit()
        except Exception as e:
            self.mysql_msg(e)
            cnx.rollback()

    def get_city_tracking_points(self):
        try:
            cur.execute(
                "SELECT longitude,latitude,page FROM meituan_city_point WHERE status_code='0'")
            return cur.fetchall()
        except Exception as e:
            print e
            return self.get_city_tracking_points()


    def get_token(self):
        try:
            cur2.execute(
                "SELECT url,headers,token FROM  tb_whalewins_meituan_token")
            return cur2.fetchall()
        except Exception as e:
            print e
            # return self.get_token()

    def update_location_page(self,wm_longitude, wm_latitude,page):
       
        try:
            cur.execute("UPDATE meituan_city_point SET page ={2} WHERE longitude = '{0}' and latitude ='{1}'".format(wm_longitude, wm_latitude, page))
            cnx.commit()
        except Exception as e:
            print e
            cnx.rollback()

            pass


    def update_location_state(self, wm_longitude, wm_latitude,page):
        
        try:
            cur.execute("UPDATE meituan_city_point SET status_code= 1 ,page ={2} WHERE longitude = '{0}' and latitude ='{1}'".format(wm_longitude, wm_latitude, page))
            cnx.commit()
        except Exception as e:
            print e
            cnx.rollback()
            pass

    def update_location_state_page(self, wm_longitude, wm_latitude,page):
     
        try:
            cur.execute("UPDATE meituan_city_point SET status_code= 0 ,page ={2} WHERE longitude = '{0}' and latitude ='{1}'".format(wm_longitude, wm_latitude, page))
            cnx.commit()
        except Exception as e:
            print e
            cnx.rollback()
            pass

    def update_params_state(self, url, headers, token):
   
        try:
            cur2.execute(
                """UPDATE tb_whalewins_meituan_token SET status=1 WHERE url= {0} and headers ='{1}' and token='{2}';""".format(
                    url, headers, token))
            cnx2.commit()
        except Exception as e:
            print e
            cnx.rollback()
            pass

    def update_params_count(self, count, url):
   
        try:
            cur2.execute("""UPDATE tb_whalewins_meituan_token SET count={0} WHERE url= "{1}" """.format(
                count, url))
            cnx2.commit()
            print ('update_count_success')
        except Exception as e:
            print (e, 'update_count_error')
            cnx.rollback()
            pass

    def mysql_msg(self, msg):
        loginLogger = logging.getLogger('checkMysqlLogger')
        loginLogger.setLevel(logging.DEBUG)
        fh = logging.FileHandler('%s_check_Mysql.log' % str(datetime.datetime.now().date()), mode='a',
                                 encoding=None, delay=False)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        loginLogger.addHandler(fh)
        loginLogger.info(msg)
        loginLogger.removeHandler(fh)


if __name__ == '__main__':
    mysql_helper = MysqlHelper()
    values_list = mysql_helper.check_lgt_lat()
    for lgt, lat in values_list:
        mysql_helper.save_lgt_lat_page(lgt, lat)
