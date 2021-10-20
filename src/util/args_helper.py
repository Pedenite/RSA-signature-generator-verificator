import argparse

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'sim', 'true', 't', 'y', 's', '1'):
        return True
    elif v.lower() in ('no', 'não', 'nao', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
