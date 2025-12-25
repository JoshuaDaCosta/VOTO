import logging
import os

def setup_logger():
    logger = logging.getLogger("votologger")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S',
    )

    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 🔥 GARANTIR QUE A PASTA EXISTE
    log_dir = "logs_voto"
    os.makedirs(log_dir, exist_ok=True)

    log_path = os.path.join(log_dir, "voto.log")

    # Handler para arquivo
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
