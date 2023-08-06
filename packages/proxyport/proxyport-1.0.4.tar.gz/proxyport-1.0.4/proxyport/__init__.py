from .proxyport import keeper

__all__ = ['get_random_proxy', 'get_proxy_list', 'set_user_agent']


def get_random_proxy():
    return keeper.get_random_proxy()


def get_proxy_list():
    return keeper.get_proxy_list()


def set_user_agent(user_agent):
    keeper.set_user_agent(user_agent)
