from tei_reader import TeiReader


def main():
    reader = TeiReader()
    corpora = reader.read_file('../../files/tei/1_1_1.tei')  # or read_string
    print(corpora.text)

    # show element attributes before the actual element text
    print(corpora.tostring(lambda x, text: str(list(a.key + '=' + a.text for a in x.attributes)) + text))


if __name__ == "__main__":
    main()
