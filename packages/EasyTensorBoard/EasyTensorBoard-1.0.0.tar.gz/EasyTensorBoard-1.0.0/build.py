import sys

sys.argv.append("sdist")
sys.argv.append("bdist_wheel")

if __name__ == '__main__':
    import setup
