import src
import logging
import ConfigParser
from os import path

def get_config():
    base_dir = path.dirname(path.realpath(__file__))
    config = ConfigParser.RawConfigParser()
    config.read(path.join(base_dir, 'config.ini'))
    return config


def main():

    config = get_config()
    ll = config.get('main', 'log level')
    lfl = config.get('main', 'log file level')
    ltl = config.get('main', 'log term level')
    src.start_logging(ll, lfl, ltl)

    logging.info("Initialization")
    ctr1 = config.getfloat('parameters', 'ctr1')
    alfa = config.getfloat('parameters', 'alfa')
    efekt = config.getfloat('parameters', 'efekt')

    base = config.getint('constans', 'wartosc bazowa')
    los = config.getint('constans', 'los')
    ml = config.getint('constans', 'ml')
    step_value = config.getint('constans', 'krok doliczany')
    ls = config.getint('constans', 'ls')

    ###

    ctr2 = ctr1 * (1 + efekt)

    for x in range(20):
        src.clc.oss(base, step_value, ml, ctr1, ctr2, los, ls, alfa)

if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        logging.fatal("######## MANUAL STOP ########")