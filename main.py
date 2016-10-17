from search_engine import Engine


def main():
    engine = Engine('/home/mcfeod/PycharmProjects/vesna.yandex', extension='.txt')
    go = True
    print("Введите запрос (выход - ctrl-D)")
    while go:
        try:
            for x in engine.search_phrase(input("=> ")):
                print(x)
        except (KeyboardInterrupt, EOFError):
            go = False

if __name__ == '__main__':
    main()
