from pymongo.cursor import Cursor


def convert_object_to_str(object_cursor) -> list:
    list_cursor = []    

    for i in object_cursor:
        i["_id"] = str(i["_id"])
        list_cursor.append(i)
    
    return list_cursor