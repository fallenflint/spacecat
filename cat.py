import argparse


from application import Application

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--skip-menu', action='store_true')
    args = parser.parse_args()
    Application().run(args.skip_menu)
