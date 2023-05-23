def into_json(org_id, name, address, website, opening_hours, ypage, goods, rating, reviews, phone, social):
    """ Шаблон файла OUTPUT.json"""

    # Проверка opening_hours на отсутствие одного их рабочих дней=
    data_grabbed = {
        "ID": org_id,
        "name": name,
        "address": address,
        "rating": rating,
        "reviews": reviews,

    }
    return data_grabbed