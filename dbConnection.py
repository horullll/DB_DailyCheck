import cx_Oracle, json

def dbCon(serviceName) :
    with open('instance_list.json') as instance_list:
        json_data = json.load(instance_list)

    instance_host=json_data[serviceName]['HOST']
    instance_username=json_data[serviceName]['USERNAME']
    instance_password=json_data[serviceName]['PASSWORD']
    instance_service_name=json_data[serviceName]['SERVICE_NAME']
    instance_port=json_data[serviceName]['PORT']

    #print('\nDB instance :' + serviceName)


    #cmc_conn = cx_Oracle.connect('system/dksemfhapekxhRl#5@172.17.11.51/CMC001')
    db_conn = cx_Oracle.connect(instance_username+'/'+instance_password+'@'+instance_host+':'+instance_port+'/'+instance_service_name )
    return db_conn

def dbClose(db_conn) :
    # sql= """ select INSTANCE_NUMBER,
    #                  INSTANCE_NAME,
    #                  HOST_NAME,
    #                  VERSION,
    #                  STATUS,
    #                  ARCHIVER
    #            from v$instance """
    #
    # cursor= db_conn.cursor()
    # cursor.execute(sql)
    #
    # for i in cursor :
    #     print(i)
   db_conn.close()
