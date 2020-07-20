import configparser

def read_cfg():
    conf = configparser.ConfigParser()
    #cfg_path = r"../res/cfg.ini"
    cfg_path = r"res/cfg.ini"
    conf.read(cfg_path, encoding="utf-8")
    items = conf.items(conf.sections()[0])
    #print(items[1][1][1:-1])
    return [items[0][1][1:-1], items[1][1][1:-1]]
'''
if __name__ == "__main__":
    read_cfg()
'''