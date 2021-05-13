from database import publisher_db, country_db

def insert_publisher(dict_values: dict) -> dict:
    exist_country = country_db.search_country(dict_values['country'])
    
    if exist_country:
        try:
            publishers = publisher_db.insert(dict_values)
            return dict(status=200, text=publishers)
        except Exception as error:
            return dict(status=400, text=error)
    else:
        return dict(status=400, text="País não foi encontrado !")

def read_all_publishers() -> dict:
    try:
        publishers = publisher_db.read_all()
        return dict(status=200, text=publishers)
    except Exception as error:
        return dict(status=400, text=error.args[0])    
