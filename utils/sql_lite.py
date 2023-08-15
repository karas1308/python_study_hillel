import sqlite3


class SQLiteDB:
    def __init__(self, db_name):
        self.db_name = db_name
        self.con = sqlite3.connect(self.db_name)
        self.con.row_factory = self.__dict_factory
        self.cur = self.con.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.commit()
        self.con.close()

    # def __dict_factory(self, cursor, row):
    #     fields = [column[0] for column in cursor.description]
    #     return {key: value for key, value in zip(fields, row)}

    def __dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def sql_query(self, query):
        res = self.cur.execute(query)
        return res.fetchall()

    def insert_into(self, table, params):
        columns = ', '.join(params.keys())
        values = ', '.join([f'"{str(i)}"' for i in params.values()])
        self.cur.execute(f"INSERT INTO {table} ({columns}) VALUES ({values})")

    def select_from(self, table, columns: list, where=None):
        if not where:
            where = {}
        columns = ', '.join(columns)
        query = f"SELECT {columns} FROM {table}"
        if where:
            if isinstance(where, dict):
                where = ', '.join([f"{key}='{value}'" for key, value in where.items()])
                query += f" WHERE {where}"
            else:
                query += f" WHERE {where}"
        return self.sql_query(query)

    def update_column_value(self, table, column_value, where=None):
        set_values = ', '.join([f"{key}='{value}'" for key, value in column_value.items()])
        query = f"Update {table} SET {set_values}"
        if where:
            if isinstance(where, dict):
                where = ', '.join([f"{key}='{value}'" for key, value in where.items()])
                query += f" WHERE {where}"
            else:
                query += f" WHERE {where}"
        return self.sql_query(query)
