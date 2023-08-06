from datetime import datetime, time


def is_time_between(inicio_hora, fim_hora, check_hora=None):
    # Se nao passar check_hora, o check sera pela hora atual.
    # Exemplo de uso:
    # is_time_between(time(10,30), time(16,33)) # Data antes da meia noite. Entre 10:30 e 16:33
    # is_time_between(time(22,0), time(4,54)) # Data depois da meia noite. Entre 22:00 e 04:54

    check_hora = check_hora or datetime.utcnow().time()
    if inicio_hora < fim_hora:  # antes da meia noite
        return check_hora >= inicio_hora and check_hora <= fim_hora
    else:  # se passar da meia noite
        return check_hora >= inicio_hora or check_hora <= fim_hora