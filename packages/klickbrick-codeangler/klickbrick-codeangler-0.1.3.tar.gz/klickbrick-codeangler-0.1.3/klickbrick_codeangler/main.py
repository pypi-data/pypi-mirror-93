from argparse import ArgumentParser

def get_args():
    parser = ArgumentParser()
    parser.add_argument("--name", type=str, help="optional name")
    args = parser.parse_args();

    return args


def greeting():
    args = get_args()
    if args.name is not None:
        message = f"Hello, {args.name}."
        return message
    else:
       message = "Hello World."
       return message

def main():
    message = greeting()
    print(message)


if __name__ == '__main__':
    main()
