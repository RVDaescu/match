import sqlite3

class sql(object):
    """
    Object for sql purposes (details bellow)
    """

    def connect(self, db):
        """
        creates/opens DB
        """
        self.con = sqlite3.connect(db)

    def add_table(self, db, tb, **kwargs):
        """adds a table and its header
        """

        self.connect(db)
        self.cursor = self.con.cursor()

        tb_fields = py2sql(kwargs)

        cmd = "CREATE TABLE %s (" %tb

        for key, val in tb_fields.items():
            cmd = cmd + "\"%s\" %s, " %(key, val)
        
        cmd = cmd+ " PRIMARY KEY(name));"

        try:
            self.cursor.execute(cmd)
        except:
            pass
        self.con.commit()

    def add_value(self, db, tb, **kwargs):
        """Adds entries inside sql db
        """
        
        order_dict = {1: 'name', 2: 'gda', 3: 'gpa', 4: 'mja', 5: 'mgda', 6: 'mgpa',
                                 7: 'gdd', 8: 'gpd', 9: 'mjd',10: 'mgdd',11: 'mgpd', 
                                12: 'va', 13: 'ea', 14: 'ia', 
                                15: 'vd', 16: 'ed', 17: 'ed'}


        if tb not in get_sql_db_table(db = db):
            self.add_table(db, tb, **kwargs)

        self.connect(db)
        self.cursor = self.con.cursor()

        #check if row exists; if yes, update data; if no, add data
        exists = self.cursor.execute('select name from %s where name = "%s"' \
                                       %(tb, kwargs['name'])).fetchall()
        
        if not exists:    
            k = v =  ''

            for key, val in kwargs.items():
                k = k + '%s, ' %key
                v = v + '"%s", ' %val

            k = k.replace('', '')[:-2]
            v = v.replace('', '')[:-2]

            cmd = 'INSERT INTO %s (%s) VALUES (%s);' %(tb, k, v)

            self.cursor.execute(cmd)
            self.con.commit()

            self.close()
        
        else:
            update = wh = ''
            cmd = 'update %s set ' %tb
            for key, val in kwargs.items():
                if key != 'name':
                    update = update + '%s = %s, ' %(key, val)
                else:
                    wh = ' where name = "%s";' %kwargs['name']
            cmd =  cmd + update.rstrip(', ') + wh
            
            self.cursor.execute(cmd)
            self.con.commit()
            
            self.close()

    def get_data(self, db, tb, field = '*'):
        """ 
        if filed == * - returns all fields
           else - returns selected field
        """

        self.connect(db)
        self.cursor = self.con.cursor()

        cmd = 'SELECT %s FROM %s;' %(field, tb)
    
        data = self.cursor.execute(cmd).fetchall()
        header = [i[0] for i in self.cursor.execute(cmd).description]
        header = dict(zip(header, range(0,(len(header)))))
        
        res = [header]+data
        
        self.close()

        return res

    def get_value(self, db, tb, field = '*', lookup = 'name', value = None):
        """
        gets only one value from db file based on field and field value
        gets entire column based on field
        """

        self.connect(db)
        self.cursor = self.con.cursor()

        if value:
            where = ' WHERE %s is "%s"' %(lookup, value)
        else:
            where = ''
       
        cmd = 'SELECT %s from %s%s;' %(field, tb, where)

        data = self.cursor.execute(cmd).fetchall()

        if value:
            return str(data[0][0])
        else:
            return [i[0] for i in data]

        self.close()

    def get_row(self, db, tb, lookup):
        """
        returns entire row for an lookup (usualy IP)
        """

        self.connect(db)
        self.cursor = self.con.cursor()

        cmd = "SELECT * from %s WHERE IP = \"%s\"" %(tb, lookup)
        data = self.cursor.execute(cmd).fetchall()
    
        header = [i[0] for i in self.cursor.execute(cmd).description]
        header = dict(zip(header, range(0,(len(header)))))
        return [header] + data

        self.close()

    def close(self):
        
        self.con.close()

def py2sql(dict):
    """
    Based on value type of input dict, return dict with Sqlite type value into a dict
    """

    py2sql_dict = {
            'int': 'INT',
            'str': 'VARCHAR(8000)',
            'float': 'FLOAT(2)',
            'unicode': 'VARCHAR(8000)',
            'long': 'BIGINT',
            'bool': 'BIT'
            }
    
    ls_dict = {}

    for i,j in dict.items():
        ls_dict[i] = py2sql_dict[ret_type(j)]

    return ls_dict

def get_sql_db_table(db):
    """
    For database "db" return all table list
    """

    connection = sqlite3.connect(db)
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type ='table';")
     
    val = cursor.fetchall()

    table_list = []

    if not val:
        return ''
    else:
        for i in range(len(val)):
            table_list.append(val[i][0].encode('utf-8'))
        
    return table_list

def ret_type(i):
    """Return python based type of value "i"
    """
    
    return str(type(i)).split("'")[1]