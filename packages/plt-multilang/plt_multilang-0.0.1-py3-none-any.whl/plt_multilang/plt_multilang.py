__author__ = "Lukas Merkle"
__copyright__ = "Copyright 21.01.21"
__email__ = 'lukas.merkle@tum.de'

class LanguageNotFound(Exception):
    pass


class MultiLang:
    def __init__(self, language):
        self.language = language

    def text(self, **kwargs):

        if self.language not in kwargs:
            if "gen" in kwargs:
                return kwargs["gen"]
            else:
                raise LanguageNotFound

        return kwargs[self.language]






if __name__ == "__main__":
    ml = MultiLang("en")

    print(ml.text(de="Dies ist der deutsche text", en="This is the english version"))