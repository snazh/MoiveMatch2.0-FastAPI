from src.pages.router import templates


def truncate(value, length):
    if len(value) <= length:
        return value
    return value[:length] + "..."


templates.env.filters['truncate'] = truncate
