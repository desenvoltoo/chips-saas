# -*- coding: utf-8 -*-
import bcrypt


def gerar_hash(senha: str) -> str:
    """
    Gera hash bcrypt para a senha em texto puro.
    """
    if not isinstance(senha, str):
        senha = str(senha)

    salt = bcrypt.gensalt(rounds=12)
    hash_bytes = bcrypt.hashpw(senha.encode("utf-8"), salt)
    return hash_bytes.decode("utf-8")


def verificar_hash(senha: str, senha_hash: str) -> bool:
    """
    Compara a senha digitada com o hash armazenado (bcrypt).
    Retorna True se bater, False se não bater ou der erro.
    """
    try:
        if not senha or not senha_hash:
            return False

        return bcrypt.checkpw(
            senha.encode("utf-8"),
            senha_hash.encode("utf-8"),
        )
    except Exception:
        return False
