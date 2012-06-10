import inflection


regexconv = "|".join


class strext(str):

    def __getattr__(self, name):
        return getattr(inflection, name)(self.__str__())

    def camelize(self, uppercase_first_letter=True):
        return inflection.camelize(self.__str__(), uppercase_first_letter)

    def parameterize(self, separator='-'):
        return inflection.parameterize(self.__str__(), separator)