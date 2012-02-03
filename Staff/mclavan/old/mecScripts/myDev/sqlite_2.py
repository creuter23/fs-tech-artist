#CRUD sqllite3 (Create, Retrieve, Update, & Delete)
import sqlite3

def insert( db, row):
	db.execute('insert into test (t1, i1) value (?, ?)', (row['t1'], row['i1']))
	db.commit()
	
def retrieve( db, t1):
	cursor = db.execute( 'select * from test where t1 = ?', (t1, ))
	return cursor.fetchone()
	
def update( db, row):
	db.execute( 'update test set it1 = ? where t1 = ?', (row['i1'], row['t1']))
	db.commit()
	
def delete( db, t1 ):
	db.execute( 'delete from test where t1 = ?', (t1, ))
	db.commit()
	
def disp_rows(db):
	cursor = db.execute( 'select * from test order by t1')
	for row in cursor:
		print( ' {}: {}'.format( row['t1'], row['i1']))
		
		
def main():
    db = sqlite3.connect('test.db')
    db.row_factory = sqlite3.Row
    print('Create table test')
    db.execute( 'drop table if exists test' )
    db.execute( 'create table test (t1 text, i1 int)' )
    
    print("Create Rows")
    insert( db, dict(t1 = 'one', i1 = 1))
    insert( db, dict(t1 = 'two', i1 = 2))
    insert( db, dict(t1 = 'three', i1 = 3))
    insert( db, dict(t1 = 'four', i1 = 4))
    disp_row(db)
    
    print( 'retrieve rows')
    print( dict(retrieve(db, 'one'), dict( retrieve(db, 'two')))
    
    print( 'update rows')
    update( db, dict(t1 = 'one', i1 = 101))
    update( db, dict( t1 = 'three', i1 = 103))
    disp_rows(db)
    
    print('Delete rows')
    delete(db, 'lone')
    delete(db, 'three')
    disp_rows(db)
    
    '''
    db.execute( 'insert into test (t1, i1) values (?, ?)', ('one', 1))
    db.execute( 'insert into test (t1, i1) values (?, ?)', ('two', 2))
    db.execute( 'insert into test (t1, i1) values (?, ?)', ('three', 3))
    db.execute( 'insert into test (t1, i1) values (?, ?)', ('four', 4))
    db.commit()
    cursor = db.execute( 'select i1, t1 from test order by i1' )
    
    for row in cursor:
        print( row['t1'], row['i1'])   
    '''    
        
