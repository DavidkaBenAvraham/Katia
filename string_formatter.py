import re
class Formatter():
    remove_HTML :re = re.compile ('<[^<]+?>')
    #@staticmethod
    #def remove_HTML_tags(string_HTML:str)->str:
    #    ''' Удаляю HTML из строки'''
    #    return Formatter.remove_HTML.sub(r' ', str)

    def remove_HTML_tags(self,string_HTML:str)->str:
        ''' Удаляю HTML из строки'''
        return self.remove_HTML.sub(r' ', str)