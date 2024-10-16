import logging

# logging.basicConfig()
formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
LOG = logging.getLogger('BAY')
LOG.setLevel(logging.INFO)
LOG.addHandler(ch)
