'''
Created on Aug 24, 2014

@author: Deep
'''

import sys
import GetSchema
import os.path

def Initialize():
    print ' \n SLICEDBMS :  \n'
 
    print '1. Create database (table name, count, column name/column_type pairs, index)'
    print '2. Update Record   (database name, data values)'
    print '3. Add record      (database name, data values)'
    print '4. Delete Record   (database name, key value)'
    print '5. Bulk load       (database name, upload file name)'
    print '6. Display Join    (database 1, database 2, join column)'
    print '7. Run Query       (table name, display_columns, condition)'
    print '8. Report 1        (nothing required)'
    print '9. Report 2        (nothing required)'
    print '0. Exit            (nothing required)'
    inputvar = raw_input("\nSelect: ")
    select(inputvar)

def select(option):
    if(option=='1'):
        CreateDatabase()
    elif(option=='2'):
        UpdateRecord()
    elif(option=='3'):
        UpdateRecord()
    elif(option=='4'):
        DeleteRecord()
    elif(option=='5'):
        BulkLoad()
    elif(option=='6'):
        DisplayJoin()
    elif(option=='7'):
        RunQuery()
    elif(option=='8'):
        os.system("Report1.exe")
    elif(option=='9'):
        os.system("Report2.exe")
    elif(option=='0'):
        print ' Good Bye... \n '
        sys.exit()

def CreateDatabase():
    _columns=""
    no=1
    print '\n 1. You Have selcted Create database \n'
    _dbname=raw_input(" Database Name : ")
    _check=GetSchema.checkdb(_dbname)
    if(_check=="false"):
        _number=raw_input(" Number of columns : ")
        _no=int(_number)
        while(_no>0):
            _cname=raw_input('  Name of Column '+str(no)+' : ')
            _col=_columns.split(',')
            check="false"
            for c in _col:
                _name=c.split('/')
                if(_cname==_name[0]):
                    check="true"
                    break
                else:
                    check="false"
            if(check=="false"):
                _ctype=raw_input('  Type of Column '+str(no)+'(INT,FLOAT,STRING) : ')
                if(_ctype=="INT" or _ctype=="FLOAT" or _ctype=="STRING"):
                    _columns=_columns+","+_cname+'/'+_ctype
                    no=no+1
                    _no=_no-1
                else:
                    print "Type of column is not valid\nPlease try again..."
                    Initialize()
            else:
                print "Column already exist\nPlease try again..."
                Initialize()
        _input=raw_input(" Enter index : ")
        if _input==None:
            _index=""
        else:
            _index=_input
        fo = open(_dbname+".slc", "a")
        fschema = open("schema.slc", "a")
        fschema.write( _dbname+"|"+str(_number)+"|"+_columns[1:]+"|"+_index+"\n");
        fschema.close()
        fo.close()
        Initialize()
    else:
        print "Database is already exist\nPlease try again..."
        Initialize()

def AddRecord(_dbname):
    _value=""
    #print '\n 1. You Have selcted Create database \n'
    #_dbname=raw_input(" Database Name : ")
    _columns=GetSchema.Getschema(_dbname)
    
    if _columns:
        #print len(_columns)
        for _col in _columns:
            #print key
                _cl=_col.split("/")
                _check="false"
                if(_cl[1]=="INT"):
                    while(_check=="false"):
                        try:
                            intvalue=int(raw_input("Enter "+_cl[0]+" ("+_cl[1]+")"))
                            if(type(intvalue) is int):
                                _value=_value+"|"+str(intvalue)
                                _check="true"
                            else:
                                print "Enter Correct Value"
                                _check="false"
                        except Exception:
                            print "Enter Correct Value"
                            _check="false"
                elif(_cl[1]=="FLOAT"):
                        while(_check=="false"):
                            try:
                                floatvalue=float(raw_input("Enter "+_cl[0]+" ("+_cl[1]+")"))
                                if(type(floatvalue) is float):
                                    _value=_value+"|"+str(floatvalue)
                                    _check="true"
                                else:
                                    print "Enter Correct Value"
                                    _check="false"
                            except Exception:
                                print "Enter Correct Value"
                                _check="false"
                elif(_cl[1]=="STRING"):
                        while(_check=="false"):
                            try:
                                strvalue=raw_input("Enter "+_cl[0]+" ("+_cl[1]+")")
                                if(type(strvalue) is str):
                                    _value=_value+"|"+str(strvalue)
                                    _check="true"
                                else:
                                    print "Enter Correct Value"
                                    _check="false"
                            except Exception:
                                print "Enter Correct Value"
                                _check="false"
        
        fo = open(_dbname+".slc", "a")
        fo.write(_value[1:]+"\n");
        fo.close()
        Initialize()
    else:
        print "Dataabase is not exist\nPleases try again..."
        Initialize()

def DeleteRecord():
    print '\n 1. You Have selcted Delete Record Option \n'
    _dbname=raw_input(" Database Name : ")
    _columns=GetSchema.Getschema(_dbname)
    _index=""
    if _columns:
        _index=GetSchema.IndexField(_dbname)
        if(_index==""):
            print "Index field is not set for this database\ntry with different database"
            Initialize()
        else:
            _datafile=[]
            _uservalue=raw_input('Enter keyvalue : ')
            count=GetSchema.countIndex(_dbname,_index)     
            for lines in open(_dbname+'.slc', 'r'):
                _datafile.append(lines)
            _tnum=GetSchema._tuplecount(_datafile, count, _uservalue)
            
            del _datafile[_tnum]
            fo = open(_dbname+".slc", "w+")
            for _data in _datafile:
                fo.write(_data);
            fo.close()
            Initialize()
    else:
        print "Dataabase is not exist\nPleases try again..."
        Initialize()
            
def RunQuery():
    print '\n 1. You Have selcted Run Query Option \n'
    _dbname=raw_input(" Database Name : ")
    _columns=GetSchema.Getschema(_dbname)
    if _columns:
        _discol={}
        _data=[]
        
        _display=raw_input('Supply a lists of columns names to display, delimited by the "|" symbol')
        display=_display.split('|')
        _ch="false"
        for d in display:
            _c=GetSchema.CheckCol(_dbname,d[0])
            if(_c=="true"):
                _ch="true"
            else:
                _ch="false"
        if(_ch=="false"):
            print "Please Try with different columns"
            Initialize() 
        _con=raw_input('Enter Condition like (name|EQ(EQ, LT or GT)|Joe Smith)')
        con=_con.split("|")
        for _d in display:
            _discol[_d]=GetSchema.countIndex(_dbname,_d)
        _conindex=GetSchema.countIndex(_dbname,con[0])
        _type=""
        for _col in _columns:
            _split=_col.split('/')
            if(con[0]==_split[0]):
                _type=_split[1]
        for lines in open(_dbname+'.slc', 'r'):
            line=lines.split('|')
            if(_type=="STRING"):
                if(con[1]=="EQ"):
                    if((line[_conindex])==con[2]):
                        _dataline=""
                        for key in _discol:
                            _dataline=_dataline+" "+line[_discol[key]]
                        _data.append(_dataline[1:])
                else:
                    print "Condition is not valid"
                    Initialize()
            elif(_type=="INT"):
                if(con[1]=="EQ"):
                    if(int((line[_conindex]))==int(con[2])):
                        _dataline=""
                        for key in _discol:
                            _dataline=_dataline+" "+line[_discol[key]]
                        _data.append(_dataline[1:])
                elif(con[1]=="LT"):
                    if(int((line[_conindex]))<int(con[2])):
                        _dataline=""
                        for key in _discol:
                            _dataline=_dataline+" "+line[_discol[key]]
                        _data.append(_dataline[1:])
                elif(con[1]=="GT"):
                    if(int((line[_conindex]))>int(con[2])):
                        _dataline=""
                        for key in _discol:
                            _dataline=_dataline+" "+line[_discol[key]]
                        _data.append(_dataline[1:])
            elif(_type=="FLOAT"):
                if(con[1]=="EQ"):
                    if(float((line[_conindex]))==float(con[2])):
                        _dataline=""
                        for key in _discol:
                            _dataline=_dataline+" "+line[_discol[key]]
                        _data.append(_dataline[1:])
                elif(con[1]=="LT"):
                    if(float((line[_conindex]))<float(con[2])):
                        _dataline=""
                        for key in _discol:
                            _dataline=_dataline+" "+line[_discol[key]]
                        _data.append(_dataline[1:])
                elif(con[1]=="GT"):
                    if(float((line[_conindex]))>float(con[2])):
                        _dataline=""
                        for key in _discol:
                            _dataline=_dataline+" "+line[_discol[key]]
                        _data.append(_dataline[1:])
        if _data:
            for d in _data:
                print d+"\n"
            Initialize()
        else:
            print "No data to display"
    else:
        print "Dataabase is not exist\nPleases try again..."
        Initialize()
                
            
def BulkLoad():
    print '\n 1. You Have selcted Bulk Load Option \n'
    _dbname=raw_input(" Database Name : ")
    _updatedbname=raw_input(" New Database Name : ")
    _columns=GetSchema.Getschema(_dbname)
    _data=[]
    if _columns:  
        for lines in open(_updatedbname+'.slc', 'r'):
            no=0
            _value=""
            for i, j in zip(lines, _columns):
                _cl=j.split("/")
                line=lines.split('|')
                _check="false"
                if(_cl[1]=="INT"):
                    while(_check=="false"):
                        try:
                            if(type(int(line[no])) is int):
                                _value=_value+"|"+str(line[no])
                                _check="true"
                                no=no+1
                            else:
                                print "Enter Correct Value"
                                _check="false"
                                Initialize()
                        except Exception:
                            print "Enter Correct Value"
                            _check="false"
                            Initialize()
                elif(_cl[1]=="FLOAT"):
                        while(_check=="false"):
                            try:
                                #floatvalue=float(raw_input("Enter "+_cl[0]+" ("+_cl[1]+")"))
                                if(type(float(line[no])) is float):
                                    _value=_value+"|"+str(float(line[no]))
                                    _check="true"
                                    no=no+1
                                else:
                                    print "Enter Correct Value"
                                    _check="false"
                                    Initialize()
                            except Exception:
                                print "Enter Correct Value"
                                _check="false"
                                Initialize()
                elif(_cl[1]=="STRING"):
                        while(_check=="false"):
                            try:
                                #strvalue=raw_input("Enter "+_cl[0]+" ("+_cl[1]+")")
                                if(type(line[no]) is str):
                                    _value=_value+"|"+str(line[no])
                                    _check="true"
                                    no=no+1
                                else:
                                    print "Enter Correct Value"
                                    _check="false"
                                    Initialize()
                            except Exception:
                                print "Enter Correct Value"
                                _check="false"
                                Initialize()
            _data.append(_value[1:])
        try:
            fo = open(_dbname+".slc", "w+")
            for d in _data:
                fo.write(d);
            fo.close()
            Initialize()
        except Exception:
            print "Database doesn't exist\nPlease try again..."
            Initialize()
              
    else:
        print "Dataabase is not exist\nPleases try again..."
        Initialize()
          
def UpdateRecord():
    print '\n 1. You Have selcted Update/Add Record Option \n'
    _dbname=raw_input(" Database Name : ")
    _columns=GetSchema.Getschema(_dbname)
    _index=""
    if _columns:
        _index=GetSchema.IndexField(_dbname)
        if(_index==""):
            AddRecord(_dbname)
        else:
            indexnum=GetSchema.countIndex(_dbname, _index)
            _data={}
            for lines in open(_dbname+'.slc', 'r'):
                line=lines.split('|')
                _data[line[indexnum]]=line
            _value=""
            for c in _columns:
                _cl=c.split('/')
                _check="false"
                if(_cl[1]=="INT"):
                    while(_check=="false"):
                        try:
                            intvalue=int(raw_input("Enter "+_cl[0]+" ("+_cl[1]+")"))
                            if(type(intvalue) is int):
                                _value=_value+"|"+str(intvalue)
                                _check="true"
                            else:
                                print "Enter Correct Value"
                                _check="false"
                        except Exception:
                            print "Enter Correct Value"
                            _check="false"
                elif(_cl[1]=="FLOAT"):
                        while(_check=="false"):
                            try:
                                floatvalue=float(raw_input("Enter "+_cl[0]+" ("+_cl[1]+")"))
                                if(type(floatvalue) is float):
                                    _value=_value+"|"+str(floatvalue)
                                    _check="true"
                                else:
                                    print "Enter Correct Value"
                                    _check="false"
                            except Exception:
                                print "Enter Correct Value"
                                _check="false"
                elif(_cl[1]=="STRING"):
                        while(_check=="false"):
                            try:
                                strvalue=raw_input("Enter "+_cl[0]+" ("+_cl[1]+")")
                                if(type(strvalue) is str):
                                    _value=_value+"|"+str(strvalue)
                                    _check="true"
                                else:
                                    print "Enter Correct Value"
                                    _check="false"
                            except Exception:
                                print "Enter Correct Value"
                                _check="false"
            value=_value[1:].split('|')
            _list=[]
            if(value[indexnum]==None):
                print "Index field cannot be null\nPlease try again..."
                Initialize()
            else:
                _list.append(value)
            _data[value[indexnum]]=value
        fo = open(_dbname+".slc", "w+")
        for key in _data:
            val=""
            for v in _data[key]:
                val=val+"|"+v
            fo.write(val[1:])
        fo.close()
        Initialize()
    else:
        print "Dataabase is not exist\nPleases try again..."
        Initialize()

def DisplayJoin():
    print 'You have selected Display Join Option '
    _dbname1=raw_input('Enter 1st database to join : ')
    _dbname2=raw_input('Enter 2nd database to join : ')
    _column=raw_input('Enter Join Column : ')
    _schema1=GetSchema.Getschema(_dbname1)
    _schema2=GetSchema.Getschema(_dbname2)
    _join1=GetSchema.countIndex(_dbname1,_column)
    _join2=GetSchema.countIndex(_dbname2, _column)
    _data=[]
    if _schema1 and _schema2:
        for j1 in open(_dbname1+'.slc', 'r'):
                join1=j1[:-1].split('|')
                for j2 in open(_dbname2+'.slc', 'r'):
                    join2=j2[:-1].split('|')
                    _value=""
                    if(join1[_join1]==join2[_join2]):
                        for join in join2:
                            if(join2[_join2]!=join):
                                _value=_value+"|"+join
                        _data.append(j1[:-1]+"|"+_value[1:])
        
        if _data:
            for d in _data:
                print d
            Initialize()
        else:
            print "No Data to Display\nPlease Try again..."
            Initialize()
    else:
        print "Databases are not correct\nPlease try again"
        Initialize()               
    
fschema = open("schema.slc", "a")
fschema.close()
Initialize()
#AddRecord()
#CreateDatabase()