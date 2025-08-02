import logging

def setup_logger():
    # Criar um logger
    logger = logging.getLogger("votologger")
    logger.setLevel(logging.DEBUG)

    # Formatação dos logs
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S',
    )

    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler para arquivo
    file_handler = logging.FileHandler("logs_voto/voto.log", encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
