def convert_object_id_to_string(object_cursor) -> list:
    list_cursor = []    

    for i in object_cursor:
        i["_id"] = str(i["_id"])
        list_cursor.append(i)
    
    return list_cursor