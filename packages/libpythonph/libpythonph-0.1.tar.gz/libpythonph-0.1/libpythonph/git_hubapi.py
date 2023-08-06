import requests


def buscar_avatar(usuario):
    """
    Busca o avatar de um usuario no github
    :param usuario: str com nome de usuario no github
    :return: str com o link do avatar
    """
    url = f"https://api.github.com/users/{usuario}"
    resp = requests.get(url)
    return resp.json()['avatar_url']
    # json() transforma um json em um dicionario (o json ja tem o formato de dicionario)


if __name__ == '__main__':
    print(buscar_avatar('dunossauro'))
