import configparser
import pymysql


def get_config_info(fpath):
    try:
        conf_dict = {}
        cfg = configparser.ConfigParser()
        cfg.read(fpath)
        for section in cfg.sections():
            # 将ini中的item组合到字典中,key=section+_option
            for item in cfg.items(section):
                key = section + '_' + item[0]
                value = item[1]
                if conf_dict.get(key, None) == None:
                    conf_dict[key] = value

        return conf_dict
    except Exception as e:
        raise e


class DbUtils():
    def __init__(self):
        conf_info = get_config_info('conf.ini')

        db_type = conf_info.get('db_type')
        host = conf_info.get('db_ip')
        port = conf_info.get('db_port')
        user = conf_info.get('db_user')
        password = conf_info.get('db_password')
        db = conf_info.get('db_databse')
        charset = conf_info.get('charset')

        self.conn = pymysql.connect(host=host, user=user, password=password, db=db, charset=charset)
        self.cursor = self.conn.cursor()

    def execute_many(self, execute_sql, data_list):
        try:
            self.cursor.executemany(execute_sql, data_list)
            self.conn.commit()
        except Exception as e:
            print('数据插入错误:', e)

    def execute(self, execute_sql):
        try:
            self.cursor.execute(execute_sql)
            self.conn.commit()
        except Exception as e:
            print('数据插入错误:', e)
    def test(self):
        print("dbutils测试")
        self.cursor.execute("select * from fund_morningstar")
        result = self.cursor.fetchall()
        print(result)


if __name__ == '__main__':
    dbutils = DbUtils()
    dbutils.execute("truncate table fund_morningstar_select")
    # dbutils.test()
