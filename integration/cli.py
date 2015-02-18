from pynio import Instance, Service, Block

# from tools import pplist


def main(host, port, username, password):
    nio = Instance(host, port, (username, password))
    print("#" * 50)
    print("#" * 5, "Connected to nio instance:", nio)
    # print("#" * 50)
    # print("#" * 5, "Existing Services:")
    # pplist(tuple(nio.service_names()), indent=4)
    # print("#" * 50)
    # print("#" * 5, "Existing Blocks:")
    # pplist(tuple(nio.block_names()), indent=4)
    try:
        '''http://ipython.org/ipython-doc/stable/interactive/reference.html\
            #embedding-ipython'''
        import IPython
        IPython.embed()
    except ImportError:
        import code
        code.interact(local=locals())


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Open an interactive session to a nio Instance')
    parser.add_argument('-i', '--host', default='127.0.0.1')
    parser.add_argument('-p', '--port', type=int, default=8181)
    parser.add_argument('-l', '--login', type=str, nargs=2,
                        metavar=("USERNAME", "PASSWORD"),
                        default=('Admin', 'Admin'))
    args = parser.parse_args()
    print("Using settings:", args)
    main(args.host, args.port, *args.login)
