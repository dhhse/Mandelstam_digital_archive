from yattag import Doc, indent


class Tei:
    def __init__(self):
        doc, tag, text = Doc().tagtext()
        self.doc = doc
        self.tag = tag
        self.text = text

        self.body_text = None
        self.head = None
        self.resp_statements = []
        self.main_title = None
        self.author = None
        self.publication_place = None
        self.publication_publisher = None
        self.publication_date = None
        self.source_author = None
        self.source_edition = None
        self.encoding_sampling = None
        self.note = None
        self.profile_creation_date = None
        self.languages = []
        self.text_desc = None
        self.text_volume = None
        self.text_type = None
        self.text_type_n = None
        self.text_rhyme = None
        self.catrefs = []

    def _export_header_titleStmt_respStmt(self, resp):
        with self.tag('respStmt'):
            if 'resp' in resp:
                with self.tag('resp'):
                    self.text(resp['resp'])
            if 'name' in resp:
                with self.tag('name'):
                    self.text(resp['name'])
            if 'orgName' in resp:
                with self.tag('orgName'):
                    self.text(resp['orgName'])
        return self.doc

    def _export_header_titleStmt(self):
        with self.tag('titleStmt'):
            with self.tag('title'):
                self.text(self.main_title)
            with self.tag('author'):
                self.text(self.author)
            for resp_statement in self.resp_statements:
                self._export_header_titleStmt_respStmt(resp_statement)
        return self.doc

    def _export_header_note(self):
        with self.tag('note'):
            self.text(self.note)
        return self.doc

    def _export_header_catrefs(self):
        for type, target in self.catrefs:
            self.doc.stag('catref', type=type, target=target)
        return self.doc


    def _export_header_publicationStmt(self):
        with self.tag('publicationStmt'):
            with self.tag('pubPlace'):
                self.text(self.publication_place)
            with self.tag('publisher'):
                self.text(self.publication_publisher)
            with self.tag('date'):
                self.text(self.publication_date)
        return self.doc


    def _export_header_sourceDesc(self):
        with self.tag('sourceDesc'):
            with self.tag('biblStruct'):
                with self.tag('monogr'):
                    with self.tag('author'):
                        self.text(self.source_author)
                    with self.tag('edition'):
                        self.text(self.source_edition)
        return self.doc

    def _export_header_fileDesc(self):
        with self.tag('fileDesc'):
            self._export_header_titleStmt()
            self._export_header_publicationStmt()
            self._export_header_sourceDesc()

    def _export_header_encodingDesc(self):
        with self.tag('encodingDesc'):
            with self.tag('samplingDecl'):
                with self.tag('p'):
                    self.text(self.encoding_sampling)
        return self.doc

    def _export_header_profileDesc(self):
        with self.tag('profileDesc'):
            with self.tag('creation'):
                with self.tag('date',
                              notBefore=self.profile_creation_date['notBefore'],
                              notAfter=self.profile_creation_date['notAfter']):
                    self.text(self.profile_creation_date['text'])
            with self.tag('langUsage'):
                for language in self.languages:
                    with self.tag('language', ident=language["ident"]):
                        self.text(language['text'])
            self.doc.stag('textDesc', n=self.text_desc)

        return self.doc

    def _export_header(self):
        with self.tag('teiHeader'):
            self._export_header_fileDesc()
            self._export_header_encodingDesc()
            self._export_header_profileDesc()
            self._export_header_note()
            self._export_header_catrefs()

        return self.doc

    def _export_lg(self):
        for quatrain in self.body_text:
            if 'met' not in quatrain:
                quatrain['met'] = ""
            if 'rhyme' not in quatrain:
                quatrain['rhyme'] = ""
            with self.tag('lg', type=quatrain["type"], rhyme=quatrain['rhyme'], met=quatrain['met']):
                for line in quatrain['lines']:
                    with self.tag('l', n=line['n']):
                        if 'rhyme_label' in line:
                            self.doc.stag('rhyme', label=line['rhyme_label'])
                        self.text(line['text'])
                        if 'rhyme_word' in line:
                            with self.tag('rhyme'):
                                self.text(line['rhyme_word'])
                        if 'entities' in line:
                            for entity in line['entities']:
                                self.doc.stag('rs', ref=entity['ref'], type=entity['type'])
        return self.doc

    def _export_text(self):
        with self.tag('text'):
            with self.tag('body'):
                with self.tag('div1', n=self.text_volume, type="volume"):
                    with self.tag('div2', n=self.text_type_n, type=self.text_type, rhyme=self.text_rhyme):
                        with self.tag('head'):
                            self.text(self.head)
                        self._export_lg()

        return self.doc
    """
        Actual xml constrution goes here
    """
    def export(self):

        with self.tag('TEI', xmlns="http://www.tei-c.org/ns/1.0"):
            self._export_header()
            self._export_text()

        return indent(
            self.doc.getvalue(),
            indentation=' '*4,
            newline='\r\n'
        )

    """
        Setting object fields
    """
    def set_body_text(self, text):
        self.body_text = text

    def set_head(self, head):
        self.head = head

    def set_resp_statements(self, resp_statements):
        self.resp_statements = resp_statements

    def set_header_title(self, main_title, author):
        self.main_title = main_title
        self.author = author

    def set_header_publication(self, place, publisher, date):
        self.publication_place = place
        self.publication_publisher = publisher
        self.publication_date = date

    def set_header_source(self, author, edition):
        self.source_author = author
        self.source_edition = edition

    def set_header_encoding(self, sampling):
        self.encoding_sampling = sampling

    def set_header_note(self, note):
        self.note = note

    def set_header_catref(self, type, target):
        self.catrefs.append((type, target))

    def set_header_profile(self, creation_date, languages, text_desc):
        self.profile_creation_date = creation_date
        self.languages = languages
        self.text_desc = text_desc

    def set_body_text_metadata(self, volume, type, type_n, rhyme):
        self.text_volume = volume
        self.text_type = type
        self.text_type_n = type_n
        self.text_rhyme = rhyme

def main():
    t = Tei()
    text = [
        {
            "type": "quatrain",
            "rhyme": "aabb",
            "met": "-u|-u|-u|-u|-u||-u-/",
            "lines": [
                {
                    "n": 1,
                    "rhyme_label": 'a',
                    "rhyme_word": 'богата',
                    "text": 'Куда как тетушка моя была богата.',
                },
                {
                    "n": 2,
                    "rhyme_label": 'a',
                    "rhyme_word": 'палата,',
                    "text": 'Фарфора, серебра изрядная палата,',
                },
                {
                    "n": 3,
                    "rhyme_label": 'b',
                    "rhyme_word": 'акажу',
                    "text": 'Безделки разные и мебель акажу,',
                },
                {
                    "n": 4,
                    "rhyme_label": 'b',
                    "rhyme_word": 'расскажу',
                    "text": 'Людовик, рококо — всего не расскажу.',
                },

            ]
        }, {
            "type": "quatrain",
            "rhyme": "ccdd",
            "met": "-u|-u|-u|-u|-u||-u-/",
            "lines": [
                {
                    "n": 1,
                    "rhyme_label": 'c',
                    "rhyme_word": 'зале',
                    "text": 'У тетушки моей стоял в гостином зале',
                },
                {
                    "n": 2,
                    "rhyme_label": 'c',
                    "rhyme_word": 'рояле',
                    "text": 'Бетховен гипсовый на лаковом рояле',
                    "entities": [
                        {
                            "ref": "Бетховен, Людвиг ван",
                            "type": "person"
                        }
                    ],
                },
                {
                    "n": 3,
                    "rhyme_label": 'd',
                    "rhyme_word": 'чести',
                    "text": 'У тетушки моей он был в большой чести.',
                },
                {
                    "n": 4,
                    "rhyme_label": 'd',
                    "rhyme_word": 'прийти',
                    "text": 'Однажды довелось мне в гости к ней прийти, -',
                },

            ]
        }
    ]

    t.set_resp_statements([
        {
            "resp": 'подготовка TEI/XML',
            "name": 'Алексей Литвинцев, Вероника Файнберг, Тимофей Молчанов'
        }, {
            "resp": 'Идея, постановка задач, руководство',
            "name": 'Анастасия Бонч-Осмоловская, Павел Нерлер, Леонид Видгоф,  Дмитрий Зуев, Вероника Файнберг, Павел Литвинов',
            "orgName": 'Центр Digital Humanities НИУ ВШЭ'
        }
    ])
    t.set_header_title('Тетушка и Марат', 'О.Э. Мандельштам')
    t.set_header_publication('Москва', 'АРТ-БИЗНЕС-ЦЕНТР МОСКВА', '1993')
    t.set_header_source('О.Э. Мандельштам', 'Собрание сочинений в 4 томах.')
    t.set_header_encoding('Издание подготовлено Мандельштамовским обществом')
    t.set_header_profile({
        "notBefore": '1920',
        "notAfter": '1920',
        "text": '1920'
    }, [
        {
            "ident": "RU",
            "text": 'Whole text in Russian.'
        }
    ], "poem")
    t.set_head("ТЕТУШКА И МАРАТ")
    t.set_body_text(text)
    t.set_body_text_metadata(volume="2", type="poem", type_n="63", rhyme="aabbccddeeffaaff")

    print(t.export())


if __name__ == "__main__":
    main()
