from database import publisher_db, country_db

def insert_publisher(dict_values: dict) -> dict:
        try:
            exist_country = country_db.search_country(dict_values['country'])

            if exist_country:
                publishers = publisher_db.insert_publishers_db(dict_values)
                return dict(status=200, text=publishers)
            else:
                return dict(status=400, text="País não foi encontrado!")

        except Exception as error:
            return dict(status=400, text=error.args[0])   

def read_all_publishers() -> dict:
    try:
        publishers = publisher_db.read_all_publishers_db()
        return dict(status=200, text=publishers)
    except Exception as error:
        return dict(status=400, text=error.args[0])    
