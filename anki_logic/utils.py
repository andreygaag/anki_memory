import datetime


def update_show_time(f):
    async def wrapper(*args, **kwargs):
        card = await f(*args, **kwargs)
        if card:
            card.show_time = datetime.datetime.now(tz=datetime.timezone.utc)
            await args[0].db.update_card_show_time(card)
        return card

    return wrapper
