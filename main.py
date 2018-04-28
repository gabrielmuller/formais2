from subprocess import *

def pl_query (query):
    return Popen(\
    ['swipl -s regular.pl -t "'+\
    query+',halt." --quiet'],\
    stdout=PIPE, shell=True, universal_newlines=True)\
    .communicate()[0]

print(pl_query('strings_of_size(X,5),print(X)'))


