__author__ = 'gbaranowski'

import numpy as np
from itertools import izip
import logging
from datetime import datetime
from dateutil import relativedelta


def bayes_props(s1, s2, p1, p2, ls):
    bd1 = np.random.beta(s1 + 1, p1 + 1, ls)
    bd2 = np.random.beta(s2 + 1, p2 + 1, ls)
    return sum(bd1 > bd2)/float(ls)

def oss(base_sample, step_value, max_steps, ctr1, ctr2, los, ls, alfa):
    t = datetime.now()
    border = 0.5
    current_sample_size = base_sample
    calculate_power = prepare_calculator(ctr1, ctr2, los, alfa, ls)
    for j in range(max_steps):
        current_sample_size += step_value
        power = calculate_power(current_sample_size)
        logging.debug("[] value:{} power:{}".format(current_sample_size, power))
        if power >= border:
            passed = relativedelta.relativedelta(datetime.now(), t)
            logging.info("Final value {} after {:02}:{:02}'{}".format(current_sample_size, passed.minutes, passed.seconds, passed.microseconds))
            break


def prepare_calculator(ctr1, ctr2, los, alfa, ls):
    def calculate_power(current_sample_size):
            bin1 = np.random.binomial(current_sample_size, ctr1, los)
            bin2 = np.random.binomial(current_sample_size, ctr2, los)
            power_sum = 0
            for s1, s2 in izip(bin1, bin2):
                bp = bayes_props(s1, s2, current_sample_size-s1, current_sample_size-s2, ls)
                power_sum += bp  <= alfa
                logging.debug("s1:{} s2:{} Ns1:{} Ns2:{} ls:{} bp:{} alfa:{} power_sum:{}".format(s1, s2, current_sample_size-s1, current_sample_size-s2, ls, bp, alfa, power_sum))
            return power_sum/float(los)
    return calculate_power