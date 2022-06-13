from tortoise import Tortoise, ModelMeta
from tortoise.contrib.pydantic import PydanticModel


async def filter_qs(model, pydantic_model: PydanticModel, **kwargs):
    conn = Tortoise.get_connection('default')
    arr_value_like = []
    for param, value in kwargs.items():
        if value is not None:
            if type(value) == int:
                arr_value_like.append(f'{param} BETWEEN {value} AND {value}')
            else:
                arr_value_like.append(f"{param} LIKE '{value}%'")
    if len(arr_value_like) == 0:
        qs = await conn.execute_query(f'SELECT * FROM {model._meta.db_table}')
    else:
        str_query = f'SELECT * FROM {model._meta.db_table} WHERE ' + 'and '.join(arr_value_like)
        qs = await conn.execute_query(str_query)
    data_filter = []
    for item in qs[1]:
        get_obj = await model.get(uid=item.get('uid'))
        data_filter.append(await pydantic_model.from_tortoise_orm(get_obj))
    return data_filter

