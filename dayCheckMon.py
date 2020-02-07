import dbConnection

def main(instanceName) :
    dbCon = dbConnection.dbCon(instanceName)
    cursor = dbCon.cursor()
    print('\nDB instance :' + instanceName)
    printDBinfo(cursor)

    if instanceName == 'HIS015' or instanceName == 'HIS016' or instanceName == 'DEV502' :
        tablespaceUseInfo_v12c(cursor)
    else :
        tablespaceUseInfo(cursor)

    rmanBackupCheck()
    cursor.close()
    dbConnection.dbClose(dbCon)

def printDBinfo(cursor) :

    databaseInfoSql = """ select INSTANCE_NUMBER,
                     INSTANCE_NAME,
                     HOST_NAME,
                     VERSION,
                     STATUS,
                     ARCHIVER
                     from v$instance """

    cursor.execute(databaseInfoSql)

    for i in cursor :

        print('HOST_NAME : ' + i[2])
        print('VERSION : ' + i[3])
        print('ARCHIVE MODE : ' + i[5])

        if i[4] == 'OPEN' :
            print("\nInstance is OPEN !!")
        else :
            print('check database!!!!! db status :' +  i[4])

def tablespaceUseInfo(cursor) :
    print("\nTABLESPACE USAGE")
    print('you shoud add the tablespace about uder list! \n')

    sql = """    SELECT A0.TABLESPACE_NAME
                ,ROUND(A1.tbsize/1024/1024) T_SIZE
                ,ROUND(A1.tbfree/1024/1024) F_SIZE
                ,ROUND((A1.TBSIZE - A1.TBFREE)*100/A1.TBSIZE ,2)  USED
                 , A0.CONTENTS
                 , (SELECT  PHSWM.FN_GETTBS_3MON_INC(A0.TABLESPACE_NAME )  FROM dual) TBS_3MON_INC
            FROM dba_tablespaces A0,
            (       SELECT  a.tablespace_name , a.bytes as tbsize , nvl(f.bytes,0) tbfree
                    FROM
                            (SELECT tablespace_name, sum(bytes) bytes
                             FROM DBA_DATA_FILES group by tablespace_name)a,
                            (SELECT tablespace_name, sum(bytes) bytes
                             FROM dba_free_space group by tablespace_name) f
                    WHERE A.tablespace_name=F.tablespace_name(+)
                    AND A.tablespace_name NOT IN
                    (
                        select tablespace_name
                          from (
                                    select TABLESPACE_NAME
                                         , SUBSTR(TABLESPACE_NAME,INSTR(TABLESPACE_NAME,'_',1,1)+1, 6) FROMDD
                                         , DECODE(SUBSTR(TABLESPACE_NAME,INSTR(TABLESPACE_NAME,'_',1,2)+1, 6)
                                         , 'D08'
                                         , SUBSTR(TABLESPACE_NAME,INSTR(TABLESPACE_NAME,'_',1,1)+1, 6)
                                         , SUBSTR(TABLESPACE_NAME,INSTR(TABLESPACE_NAME,'_',1,2)+1, 6)) TODD
                                      from dba_tablespaces
                                     where regexp_like (tablespace_name, '*_[0-9]{6}_*')
                               )
                         where todd <to_char(SYSDATE,'YYYYMM')
                        union all
                        select tablespace_name
                          from dba_tablespaces
                         where regexp_like (tablespace_name, '*_PRE_*')
                    )
            ) A1
            WHERE A0.tablespace_name = A1.tablespace_name
            AND   A0.tablespace_name not in ('UNDOTBS1','UNDOTBS2')
            AND   ROUND((A1.TBSIZE - A1.TBFREE)*100/A1.TBSIZE ,2) >=95
            ORDER BY USED DESC   
    """

    cursor.execute(sql)

    for i in cursor :
        print("TABLESPACE_NAME : " + i[0] + "  USE(%) : "+ str(i[3]))
        #print(i)

def printDBinfo(cursor) :

    databaseInfoSql = """ select INSTANCE_NUMBER,
                     INSTANCE_NAME,
                     HOST_NAME,
                     VERSION,
                     STATUS,
                     ARCHIVER
                     from v$instance """

    cursor.execute(databaseInfoSql)

    for i in cursor :

        print('HOST_NAME : ' + i[2])
        print('VERSION : ' + i[3])
        print('ARCHIVE MODE : ' + i[5])

        if i[4] == 'OPEN' :
            print("\nInstance is OPEN !!")
        else :
            print('check database!!!!! db status :' +  i[4])

def tablespaceUseInfo_v12c(cursor) :
    print("\nTABLESPACE USAGE")
    print('you shoud add the tablespace about uder list! \n')

    sql = """ SELECT TABLESPACE_NAME,RT_SIZE_MB,FT_SIZE_MB,U_SIZE_MB,F_SIZE_MB,"USED(%)","USED2(%)" ,FILE_STAT_CNT,AVG_INC_SIZE_MB
                FROM
                (
                SELECT  T1.TABLESPACE_NAME, ROUND(T1.RT_SIZE_MB) RT_SIZE_MB, ROUND(T1.FT_SIZE_MB) FT_SIZE_MB  ,
                         ROUND(T1.FT_SIZE_MB - NVL(F1.F_SIZE_MB,0) ) U_SIZE_MB
                       ,  ROUND( RT_SIZE_MB   - (T1.FT_SIZE_MB -  NVL(F1.F_SIZE_MB,0) )  ) F_SIZE_MB
                       ,  ROUND((T1.FT_SIZE_MB -  NVL(F1.F_SIZE_MB,0) )*100/T1.RT_SIZE_MB ,2)  "USED(%)"
                       ,  ROUND((T1.FT_SIZE_MB -  NVL(F1.F_SIZE_MB,0) )*100/T1.FT_SIZE_MB ,2)  "USED2(%)"
                       ,   'TF:'||FILE_CNT||'# AF:'||AUTO_FILE_CNT FILE_STAT_CNT
                     , ROUND( AVG_INC_SIZE_MB) AVG_INC_SIZE_MB
                FROM
                (
                    SELECT TABLESPACE_NAME,   SUM(T_SIZE_MB) RT_SIZE_MB , SUM(BYTES)/1024/1024 FT_SIZE_MB , AVG(INCREMENTAL_SIZE_MB) AVG_INC_SIZE_MB , COUNT(*) FILE_CNT,
                             SUM(CASE WHEN AUTOEXTENSIBLE='YES' THEN 1 END) AUTO_FILE_CNT
                    FROM
                    (
                    SELECT  TABLESPACE_NAME , AUTOEXTENSIBLE , MAXBYTES , BYTES ,  CASE WHEN AUTOEXTENSIBLE='YES' THEN MAXBYTES/1024/1024 ELSE BYTES/1024/1024  END T_SIZE_MB
                           ,  (INCREMENT_BY* (select value from v$parameter where name='db_block_size') )/1024/1024  INCREMENTAL_SIZE_MB
                    FROM DBA_DATA_FILES
                    WHERE TABLESPACE_NAME NOT IN
                       (
                            select tablespace_name
                              from (
                                        select TABLESPACE_NAME
                                             , SUBSTR(TABLESPACE_NAME,INSTR(TABLESPACE_NAME,'_',1,1)+1, 6) FROMDD
                                             , DECODE(SUBSTR(TABLESPACE_NAME,INSTR(TABLESPACE_NAME,'_',1,2)+1, 6)
                                             , 'D08'
                                             , SUBSTR(TABLESPACE_NAME,INSTR(TABLESPACE_NAME,'_',1,1)+1, 6)
                                             , SUBSTR(TABLESPACE_NAME,INSTR(TABLESPACE_NAME,'_',1,2)+1, 6)) TODD
                                          from dba_tablespaces
                                         where regexp_like (tablespace_name, '*_[0-9]{6}_*')
                                   )
                             where todd <to_char(SYSDATE,'YYYYMM')
                            union all
                            select tablespace_name
                              from dba_tablespaces
                             where regexp_like (tablespace_name, '*_PRE_*')
                       )
                    )
                    GROUP BY TABLESPACE_NAME
                )T1,
                (
                   SELECT tablespace_name, sum(bytes)/1024/1024 F_SIZE_MB
                   FROM dba_free_space group by tablespace_name
                )F1
                WHERE
                  T1.tablespace_name=F1.tablespace_name(+)
                )
                WHERE  "USED(%)" > 60
                ORDER BY       "USED(%)" DESC
    
    """

    cursor.execute(sql)

    for i in cursor :
        print("TABLESPACE_NAME : " + i[0] + "  USE(%) : "+ str(i[5]))



def rmanBackupCheck() :
    print("\nRMAN BACKUP CHECK!!\n")
    alter_data_format = "alter session set nls_date_format='YYYYMMDD-HH24:MI:SS'  "

    dbCon = dbConnection.dbCon('HIS011CA')
    cursor = dbCon.cursor()
    cursor.execute(alter_data_format)

    sql = """
                SELECT --A.RECID,
                   --A.PARENT_RECID PRECID,
                   A.ROW_TYPE,
                   A.OPERATION,
                   A.CHANNEL,
                   A.STATUS,
                   A.START_TIME,
                   A.TAKEN_TIME,
                   A.OBJECT_TYPE,
                   A.OUTPUT_DEVICE_TYPE,
                   A.OPTIMIZED,
                   ROUND(B.COMPRESSION_RATIO,4)                                                     AS COMPRESS_RATIO, 
                   A.INPUT_TB,
                   A.OUTPUT_TB,
                   B.INPUT_BYTES_PER_SEC_DISPLAY                                                    AS INPUT_PER_SEC_MB,
                   B.OUTPUT_BYTES_PER_SEC_DISPLAY                                                   AS OUTPUT_PER_SEC_MB,
                   (SELECT ALGORITHM_NAME FROM V$RMAN_COMPRESSION_ALGORITHM WHERE IS_DEFAULT='YES')||'('||
                   (SELECT ALGORITHM_NAME FROM V$RMAN_ENCRYPTION_ALGORITHMS WHERE IS_DEFAULT='YES')||')' AS DEF_ALGO
                   --B.TIME_TAKEN_DISPLAY
              FROM 
                   (
                    SELECT  recid,
                            PARENT_RECID,
                            row_type,
                            LPAD('   ', (LEVEL-1)*2)||operation operation,
                            (SELECT decode(count(distinct output),0,null,count(distinct output)) FROM V$RMAN_OUTPUT b where b.OUTPUT like 'allocated channel: ch%' and b.SESSION_RECID = a.recid) channel,
                            status,
                            start_time,
                            LPAD (MOD (TRUNC ((( end_time-start_time) * 86400) / (60 * 60)), 24), 2, 0) || ':'
                         || LPAD (MOD (TRUNC ((( end_time-start_time) * 86400) / 60), 60), 2, 0) || ':'
                         || LPAD (TRUNC(MOD  ((( end_time-start_time) * 86400), 60)), 2, 0) TAKEN_TIME,
                            round(input_bytes/1024/1024/1024/1024,2) input_Tb,
                            round(output_bytes/1024/1024/1024/1024,2) output_Tb,
                            object_type,
                            output_device_type,
                            optimized
                    FROM    v$rman_status a
                    WHERE   start_time >= (sysdate - 1)
                    START   WITH recid in (SELECT DISTINCT parent_recid FROM v$rman_status WHERE start_time >= (sysdate - 1))  AND PARENT_RECID IS NULL
                    CONNECT BY prior recid = parent_recid
                   ) A,
                   V$RMAN_BACKUP_JOB_DETAILS B
            WHERE  A.RECID = B.SESSION_RECID(+)
            ORDER BY NVL(A.PARENT_RECID,A.RECID),  A.RECID, A.START_TIME 
    """
    cursor.execute(sql)

    for i in cursor :
        print(i)

