import json
from json.decoder import JSONDecodeError


def load_config():
    with open("config.json") as fh:
        try:
            config = json.load(fh)
        except JSONDecodeError as err:
            print(f"Error while parsing config:{err.msg}")
            exit(1)
    return config


def main():
    config = load_config()
    print(config)


if __name__ == '__main__':
    main()
