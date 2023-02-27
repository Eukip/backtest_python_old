import os


async def delete_png_by_strategy(strategy_name=None):
    uploads_dir = "/app/static/uploads/"
    for file in os.listdir(uploads_dir):
        if strategy_name in file:
            path = uploads_dir + file
            os.remove(path)
