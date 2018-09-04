import ply.lex as lex
import ply.yacc as yacc

reserved = {
   'project' : 'PROJECT',
   'repositories' : 'REPOSITORIES',
   'ivy' : 'IVY',
   'layout' : 'LAYOUT',
   'name' : 'NAME',
   'url' : 'URL',
   'providedInterfaces' : 'PROVIDEDINTERFACES',
   'version' : 'VERSION',
   'versionedFiles' : 'VERSIONEDFILES',
   'buildFiles' : 'BUILDFILES',
   'new' : 'NEW',
   'file' : 'FILE',
   'File' : 'FILE',
   'requiredInterfaces' : 'REQUIREDINTERFACES',
   'compile' : 'COMPILE',

   '' : 'SOMELINK'
}

# List of token names.   This is always required
tokens = [
   'LPAREN',
   'RPAREN',
   'ID',
   'APOSTROF',
   'LESSLESS',
   'COMMA',
   'PATH',
   'LBRACKETS',
   'RBRACKETS'
] + list(reserved.values())

# Regular expression rules for simple tokens
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_APOSTROF = r'\''
t_LESSLESS = r'\<<'
t_COMMA = r'\,'
t_LBRACKETS = r'\{'
t_RBRACKETS = r'\}'

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def t_path(t):
    r'com/[a-zA-Z_0-9-./]*'
    t.type = 'PATH'
    return t

def t_ID(t):
    r'[a-zA-Z_0-9:][a-zA-Z_0-9-.]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t


# Build the lexer
lexer = lex.lex()

f = open('testInput.txt','r')
s = f.read()

# Give the lexer some input
lexer.input(s)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)

projectName = ''

def p_project(p):
    'project : PROJECT LPAREN APOSTROF ID APOSTROF RPAREN LBRACKETS repositories providedInterfaces RBRACKETS'
    print p[4]
    print 'here'
    return p[4]

def p_repositories(p):
    'repositories : REPOSITORIES LBRACKETS ivydata RBRACKETS'

def p_ivydata(p):
    'ivydata : IVY LBRACKETS layout name RBRACKETS'
    '        | empty'

def p_providedInterfaces(p):
    'providedInterfaces : PROVIDEDINTERFACES LBRACKETS interfaceData RBRACKETS'
    '        | empty'

def p_interfaceData(p):
    'interfaceData : ID LBRACKETS version versionedFiles RBRACKETS'
    print p[1]

def p_version(p):
    'version : VERSION APOSTROF ID APOSTROF'
    print p[3]

#LexToken(VERSIONEDFILES,'versionedFiles',11,167)
#LexToken(LESSLESS,'<<',11,182)
# LexToken(FILE,'file',11,185)
# LexToken(LPAREN,'(',11,189)
# LexToken(APOSTROF,"'",11,190)
# LexToken(PATH,'com/ext/inc/KMFT.h',11,191)
# LexToken(APOSTROF,"'",11,209)
# LexToken(RPAREN,')',11,210)
# LexToken(VERSIONEDFILES,'versionedFiles',12,218)
# LexToken(LESSLESS,'<<',12,233)
# LexToken(FILE,'file',12,236)
# LexToken(LPAREN,'(',12,240)
# LexToken(APOSTROF,"'",12,241)
# LexToken(PATH,'com/ext/inc/KMFT',12,242)
# LexToken(ID,'2.h',12,258)
# LexToken(APOSTROF,"'",12,261)
# LexToken(RPAREN,')',12,262)
# LexToken(RBRACKETS,'}',13,268)
# LexToken(RBRACKETS,'}',14,274)
# LexToken(RBRACKETS,'}',15,278)


def p_versionedFiles(p):
    '''versionedFiles : VERSIONEDFILES LESSLESS FILE LPAREN APOSTROF PATH APOSTROF RPAREN
                      | VERSIONEDFILES LESSLESS FILE LPAREN APOSTROF PATH APOSTROF RPAREN versionedFiles'''
    print p[6]

def p_empty(p):
    'empty :'
    pass

def p_layout(p):
    'layout : LAYOUT APOSTROF ID APOSTROF'
    print p[3]

def p_name(p):
    'name : NAME APOSTROF ID APOSTROF'
    print p[3]


# Build the parser
parser = yacc.yacc()

print s
result = parser.parse(s)
print result
print projectName
