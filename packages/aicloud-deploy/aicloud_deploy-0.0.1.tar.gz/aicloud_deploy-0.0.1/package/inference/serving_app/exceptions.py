class StartServingException(Exception):
    """Вызывается, когда не удается запустить сервис"""


class InitServingException(Exception):
    """Вызывается, когда параметры запуска сервинга не проходят условия"""
