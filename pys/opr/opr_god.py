from pys.fisco import god
from pys.log import logger


def opr_god(fisco_path):
    logger.info('god start.')
    opr_god = god.God(fisco_path)
    opr_god.export()
    opr_god.replace()
    logger.info('god end.')