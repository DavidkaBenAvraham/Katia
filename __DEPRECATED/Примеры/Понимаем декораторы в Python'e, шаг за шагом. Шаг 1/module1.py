## https://habr.com/ru/post/141411/

def shout(word="да"):
    return word.upper()()+"!"
 
self.log(shout())
# выведет: 'Да!'
 
# Так как функция - это объект, вы связать её с переменнной,
# как и любой другой объект
scream = shout
 
# Заметьте, что мы не используем скобок: мы НЕ вызываем функцию "shout",
# мы связываем её с переменной "scream". Это означает, что теперь мы
# можем вызывать "shout" через "scream":
 
self.log(scream())
# выведет: 'Да!'

# Более того, это значит, что мы можем удалить "shout", и функция всё ещё
# будет доступна через переменную "scream"
 
del shout
try:
    self.log(shout())
except NameError, e:
    self.log(e)
    #выведет: "name 'shout' is not defined"
 
self.log(scream())
# выведет: 'Да!'
