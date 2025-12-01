import bcrypt

def gerar_hash(senha: str) -> str:
    """
    Gera e retorna o hash seguro da senha informada.
    """
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()


def verificar_hash(senha: str, hash_salvo: str) -> bool:
    """
    Verifica se a senha corresponde ao hash armazenado.
    """
    try:
        return bcrypt.checkpw(senha.encode(), hash_salvo.encode())
    except:
        return False
