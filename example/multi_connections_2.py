import asyncio
import mysql_async.connector
import mysql_async.connector.pooling

CREATE_TABLE = (
   "CREATE TABLE names ("
        "    id INT UNSIGNED NOT NULL AUTO_INCREMENT, "
        "    name NVARCHAR(30) DEFAULT '' NOT NULL, "
        "    info TEXT ,"
        "    age TINYINT UNSIGNED DEFAULT '30', "
        "    PRIMARY KEY (id))"
)


async def main(pcnx, loop):
    cnx = await pcnx.get_connection()  # fetch a Mysqlconnector from a pool
    cursor = await cnx.cursor()
    # Drop table if exists, and create it new
    stmt_drop = "DROP TABLE IF EXISTS names"
    await cursor.execute(stmt_drop)
    await cursor.execute(CREATE_TABLE)

    print("Inserting data")
    names = (('Geert', 20,), ('Jan', 25,),('Geert', 20,), ('Jan', 25,),
             ('Geert', 20,), ('Geert', 20,), ('Jan', 25,), ('Jan', 25,),
             ('Geert', 20,), ('Geert', 20,), ('Jan', 25,), ('Jan', 25,),
             ('Geert', 20,), ('Geert', 20,), ('Jan', 25,), ('Jan', 25,),
             ('Geert', 20,), ('Jan', 25,), ('Jan', 25,), ('Michel', 18,))
    stmt_insert = "INSERT INTO names (name, age) VALUES (%s,%s)"
    await cursor.executemany(stmt_insert, names)
    print("Inserted {0} row{1}".format(cursor.rowcount, 's' if cursor.rowcount > 1 else ''))
    await asyncio.wait([foo1(pcnx), foo2(pcnx)], loop=loop)
    cursor.close()
    cnx.close()

async def foo2(pcnx):
    cnx = await pcnx.get_connection()
    cursor = await cnx.cursor()
    stmt_fetch = "select * from names limit 1,16 "  # changed last number to see which completed first.
    await cursor.execute(stmt_fetch)
    for row in (await cursor.fetchall()):
        pass
        #print("foo2-> ", row[0], row[1], row[2])
    print('foo2 completed!')
    cursor.close()
    cnx.close()

async  def foo1(pcnx):
    cnx = await pcnx.get_connection()
    cursor = await cnx.cursor()
    stmt_fetch = "select * from names limit 1,12"  # changed last number to see which completed first.
    await cursor.execute(stmt_fetch)
    for row in (await cursor.fetchall()):
        #print("foo1-> ", row[0], row[1], row[2])
        pass
    print('foo1 completed!')

    cursor.close()
    cnx.close()

if __name__ == '__main__':

    config = {
        'unix_socket': '/var/run/mysqld/mysqld.sock',
        'database': 'test',
        'user': 'user1',
        'password': 'user1',
        'charset': 'utf8',
        'use_unicode': True,
        'get_warnings': True,
        'pool_size': 10,
    }

    #make a MySQLConnectionPool
    pcnx = mysql_async.connector.pooling.MySQLConPool(**config)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(pcnx, loop))