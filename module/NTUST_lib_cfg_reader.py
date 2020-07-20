import configparser

def read_cfg():
    conf = configparser.ConfigParser()
    cfg_path = r"res/cfg.ini"
    conf.read(cfg_path, encoding="utf-8")
    items = conf.items(conf.sections()[0])
    return [items[0][1][1:-1], items[1][1][1:-1]]
