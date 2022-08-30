from repositories.Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens



    @staticmethod
    def read_device_onderwerp(onderwerp):
        sql = "SELECT deviceid, onderwerp from device where onderwerp like %s "
        params = [onderwerp]
        return Database.get_one_row(sql, params)

    @staticmethod
    def create_meting(deviceid, gemeten_waarde,datum):
        sql= "insert into meting(deviceid, gemeten_waarde,datum) values (%s, %s, %s)"
        params = [deviceid, gemeten_waarde, datum]
        return Database.execute_sql(sql, params)

    @staticmethod
    def read_history_temp():
        sql= "SELECT * from meting where deviceid like 2 order by volgnummer desc limit 30" #"SELECT * from (select * from meting where deviceid like 1 order by volgnummer desc limit 15)order by volgnummer asc"
        params = []
        return Database.get_rows(sql, params)
    @staticmethod
    def read_history_ph():
        sql= "SELECT * from meting where deviceid like 3 order by volgnummer desc limit 30" #"SELECT * from (select * from meting where deviceid like 1 order by volgnummer desc limit 15)order by volgnummer asc"
        params = []
        return Database.get_rows(sql, params)
    @staticmethod
    def read_history_ldr():
        sql= "SELECT * from meting where deviceid like 1 order by volgnummer desc limit 30" #"SELECT * from (select * from meting where deviceid like 1 order by volgnummer desc limit 15)order by volgnummer asc"
        params = []
        return Database.get_rows(sql, params)

    @staticmethod
    def read_history_temp_juni():
        sql= "SELECT * from meting where datum between '2022-06-OO 00:00:00' and  '2022-06-3O 23:59:59' limit 5"
        params = []
        return Database.get_rows(sql, params)




##################### worden nog niet gebruikt ###########################################

    # @staticmethod
    # def read_status_device():
    #     sql = "SELECT * from device"
    #     return Database.get_rows(sql)

    # @staticmethod
    # def read_status_deviceid(deviceid):
    #     sql = "SELECT * from device WHERE deviceid = %s"
    #     params = [deviceid]
    #     return Database.get_one_row(sql, params)

    # @staticmethod
    # def update_status_device(id, status):
    #     sql = "UPDATE device SET status = %s WHERE deviceid = %s"
    #     params = [status, id]
    #     return Database.execute_sql(sql, params)

    # @staticmethod
    # def update_status_all_device(status):
    #     sql = "UPDATE device SET status = %s"
    #     params = [status]
    #     return Database.execute_sql(sql, params)

############################################################################

    # @staticmethod
    # def read_status_device():
    #     sql = "SELECT * from device"
    #     return Database.get_rows(sql)

    # @staticmethod
    # def read_status_deviceid(deviceid):
    #     sql = "SELECT * from device WHERE deviceid = %s"
    #     params = [deviceid]
    #     return Database.get_one_row(sql, params)

    # @staticmethod
    # def update_status_device(id, status):
    #     sql = "UPDATE device SET status = %s WHERE deviceid = %s"
    #     params = [status, id]
    #     return Database.execute_sql(sql, params)

    # @staticmethod
    # def update_status_all_device(status):
    #     sql = "UPDATE device SET status = %s"
    #     params = [status]
    #     return Database.execute_sql(sql, params)

    # @staticmethod
    # def create_device(onderwerp, meetapparaat, deviceid, meeteenheid, beschrijving):
    #     sql = "insert into device(onderwerp, meetapparaat, deviceid, meeteenheid, beschrijving) values (%s, %s, %s, %s, %s)"
    #     params = [onderwerp, meetapparaat, deviceid, meeteenheid, beschrijving]
    #     return Database.execute_sql(sql, params)




    # @staticmethod
    # def read_device_onderwerp(onderwerp):
    #     sql = "SELECT deviceid, onderwerp from meting where onderwerp like %s "
    #     params = [onderwerp]
    #     return Database.get_one_row(sql, params)

    # @staticmethod
    # def update_meting(deviceid, gemeten_waarde,datum):
    #     sql= "insert into meting(deviceid, gemeten_waarde,datum) values (%s, %s, %s, %s, %s)"
    #     params = [deviceid, gemeten_waarde, datum]
    #     return Database.execute_sql(sql, params)