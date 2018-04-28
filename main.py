from subprocess import *

def pl_query (query, database):
    return Popen(\
    ['swipl -s regular.pl -t "'+'[\''+database+'\'],'+\
    query+',print(Output),halt." --quiet'],\
    stdout=PIPE, shell=True, universal_newlines=True)\
    .communicate()[0]

print(pl_query('strings_of_size(Output, 5)', 'nda.pl'))
