'''
Created on Aug 24, 2014

@author: Deep
'''
from lib2to3.pgen2.token import INDENT
def Getschema(_dbname):
    _col=[]
    _columns=[]
    for lines in open('schema.slc', 'r'):
        line=lines.split('|')
        name=line[0].strip()
        no=line[1].strip()
        col=line[2].strip()
        _col=col.split(",")
        if(name==_dbname):
            for _column in _col:
                _columns.append(_column)
            break
    return _columns

def IndexField(_dbname):
    _index=""
    for lines in open('schema.slc', 'r'):
        line=lines.split('|')
        name=line[0].strip()
        if(name==_dbname):
            _index=line[3].strip()
            break
    return _index

def countIndex(_dbname,_index):
    count=0
    _columns=Getschema(_dbname)
    #_index=IndexField(_dbname)
    for _col in _columns:
        _cl=_col.split("/")
        if(_cl[0]==_index):
            break
        else:
            count=count+1
    return count

def _tuplecount(_datafile,count,_uservalue):
    _tnum=0
    for _tuple in _datafile:
        t=_tuple.split('|')
        if(t[count]==_uservalue):
            break
        else:
            _tnum=_tnum+1
    return _tnum

def checkdb(_dbname):
    _check="false"
    for lines in open('schema.slc', 'r'):
        line=lines.split('|')
        name=line[0].strip()
        if(name==_dbname):
            _check="true"
        else:
            _check="false"
    return _check

def CheckCol(_dbname,_col):
    _check="false"
    for lines in open('schema.slc', 'r'):
        line=lines.split('|')
        name=line[0].strip()
        if(name==_dbname):
            _col=line[2].split('|')
            _check="true"
        else:
            _check="false"
    return _check