from RDBService import RDBService

class BaseRDBResource:
    '''
        represent relational database table
    '''

    @classmethod
    def get_db_and_table_name(cls):
        pass
    
    @classmethod
    def find_by_template(cls, template, fields_str=None):
        db_name, table_name = cls.get_db_and_table_name()
        result = RDBService.find_by_template(db_name, table_name, template, fields_str)
        return result
    
    @classmethod
    def find_all(cls):
        db_name, table_name = cls.get_db_and_table_name()
        sql_stmt = f"select * from {db_name}.{table_name}"
        result = RDBService.run_sql(sql_stmt)
        return result

    @classmethod
    def create(cls, row_data):
        db_name, table_name = cls.get_db_and_table_name()
        created_row_id = RDBService.create(db_name, table_name, row_data)
        return created_row_id

    @classmethod
    def update(cls, template, new_data):
        db_name, table_name = cls.get_db_and_table_name()
        RDBService.update(db_name, table_name, template, new_data)

    @classmethod
    def delete(cls, template):
        db_name, table_name = cls.get_db_and_table_name()
        RDBService.delete(db_name, table_name, template)

class UserResource(BaseRDBResource):
    '''
        represent the e6156.user table
    '''
    
    @classmethod
    def get_db_and_table_name(cls):
        return "e6156", "user"


class AddressResource(BaseRDBResource):
    '''
        represent the e6156.address table
    '''

    @classmethod
    def get_db_and_table_name(cls):
        return "e6156", "address"


# template = {
#     "first_name": "zi",
# }
# result = UserResource.find_by_template(template)
# print(result)

# result = UserResource.find_all()
# print(result)
