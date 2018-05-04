#!/usr/bin/env python3
import sys
import os
import Utilities.ConvertDataType as conv
import psycopg2
from Conversation import Conversation
from twitter_apps.Keys import get_password
from Utilities.ProgressBar import display_progress_bar

"""
ResetHandleStatus.py: Updates the POSTGRES TABLE followers in twitterharassment DB by changing  status indicating of a 
                      the handle which followers data has not been collected. 
                      
                        Key of the profile file is: handle
                        Values for the file check are: 
                            0  Not processed
                            1  In process
                            2  Completed
"""

__author__ = 'Plinio H. Vargas'
__date__ = 'Fri,  Apr 17, 2018 at 13:14'
__email__ = 'pvargas@cs.odu.edu'


def main(**kwarg):
    path = kwarg['path']
    print('\nLoading conversations ...')
    observed = Conversation(path)

    interacting_handles = observed.all_conversation_elements_set()
    number_handles = len(interacting_handles)
    print('Number of Twitter accounts interacting in all conversations: {:,}'.format(number_handles))

    db_account = kwarg['user']
    password = get_password(db_account)
    db = kwarg['db']

    print('Making connection to <<{}>> DB ...'.format(db))
    dsn = "host={} dbname={} user={} password={}".format('localhost', db, db_account, password)
    conn = psycopg2.connect(dsn)
    cur = conn.cursor()
    print('Connection successful ...')

    if 'friends_path' in kwarg:
        table = 'friends'

        print('\nResetting friends table in <<{}>> DB'.format(db))

        friends = os.listdir(kwarg['friends_path'])
        for k, filename in enumerate(friends):
            friends[k] = filename[:filename.rfind('_')]
        friends = set(friends)
        friends_size = len(friends)
        print('Total number of saved Twitter accounts with friends data: {:,}'.format(friends_size))

        print('Obtaining account entries from table {} in DB ...'.format(table))
        db_friends = get_table_elements(conn, table)
        db_size = len(db_friends)
        print('Total number of tweets records in <<{}>> DB: {:,}'.format(db, db_size))

        # identify the set of elements not present in the database table
        set_tobe_added = interacting_handles - set(db_friends)
        added_size = add_elements(conn, table, set_tobe_added, friends)
        print('Number of records added into {} TABLE: {:,}'.format(table, added_size))

        # identify set already present in database table and update them
        set_tobe_updated = interacting_handles - set_tobe_added
        updated_set_size = update_elements(conn, table, set_tobe_updated, friends)
        del db_friends
        del set_tobe_added
        del set_tobe_updated
        print('Number of updated records in {} TABLE: {:,}'.format(table, updated_set_size))

    if 'followers_path' in kwarg:
        table = 'followers'

        print('\n\nResetting followers table in <<{}>> DB'.format(db))
        followers = os.listdir(kwarg['followers_path'])
        for k, filename in enumerate(followers):
            followers[k] = filename[:filename.rfind('_')]
        followers = set(followers)
        followers_size = len(followers)
        print('Total number of saved Twitter accounts with followers data: {:,}'.format(followers_size))

        print('Obtaining account entries from table {} in DB ...'.format(table))
        db_followers = get_table_elements(conn, table)
        db_size = len(db_followers)
        print('Total number of tweets records in <<{}>> DB: {:,}'.format(db, db_size))

        # identify the set of elements not present in the database table
        set_tobe_added = interacting_handles - set(db_followers)
        added_size = add_elements(conn, table, set_tobe_added, followers)
        print('Number of records added into {} TABLE: {:,}'.format(table, added_size))

        # identify set already present in database table and update them
        set_tobe_updated = interacting_handles - set_tobe_added
        updated_set_size = update_elements(conn, table, set_tobe_updated, followers)
        del db_followers
        del set_tobe_added
        del set_tobe_updated
        print('Number of updated records in {} TABLE: {:,}'.format(table, updated_set_size))

    if 'tweets_path' in kwarg:
        table = 'tweets'

        print('\n\nResetting tweets table in <<{}>> DB'.format(db))
        tweets = os.listdir(kwarg['tweets_path'])
        for k, filename in enumerate(tweets):
            tweets[k] = filename.split('.')[0]
        tweets = set(tweets)
        tweets_size = len(tweets)
        print('Total number of saved Twitter accounts with tweets data: {:,}'.format(tweets_size))

        print('Obtaining account entries from table {} in DB ...'.format(table))
        db_tweets = get_table_elements(conn, table)
        db_size = len(db_tweets)
        print('Total number of tweets records in <<{}>> DB: {:,}'.format(db, db_size))

        # identify the set of elements not present in the database table
        set_tobe_added = interacting_handles - set(db_tweets)
        added_size = add_elements(conn, table, set_tobe_added, tweets)
        print('Number of records added into tweets TABLE: {:,}'.format(added_size))

        # identify set already present in database table and update them
        set_tobe_updated = interacting_handles - set_tobe_added
        updated_set_size = update_elements(conn, table, set_tobe_updated, tweets)
        del db_tweets
        del set_tobe_added
        del set_tobe_updated
        print('Number of updated records in {} TABLE: {:,}'.format(table, updated_set_size))

    cur.close()
    conn.close()


def get_table_elements(db_conn, table):
    db_elements = {}
    sql_number_handles = 'SELECT handle, status FROM {};'.format(table)
    cur = db_conn.cursor()
    cur.execute(sql_number_handles)
    for handle, status in cur:
        db_elements[handle.strip()] = status

    cur.close()

    return db_elements


def add_elements(db_conn, table, set_to_add, obj_set):
    cur = db_conn.cursor()
    if set_to_add:
        print('\nAdding {:,} records'.format(len(set_to_add)))

    for counter, handle in enumerate(set_to_add):
        if handle in obj_set:
            value = 2
        else:
            value = 0

        display_progress_bar(25, counter / len(set_to_add))
        sql = 'INSERT INTO {} (handle, status) VALUES (\'{}\', {});'.format(table, handle, value)
        cur.execute(sql)

    if set_to_add:
        db_conn.commit()

    cur.close()

    return len(set_to_add)


def update_elements(db_conn, table, set_to_update, obj_set):
    cur = db_conn.cursor()
    if set_to_update:
        print('\nUpdating all {:,} records'.format(len(set_to_update)))

    for counter, handle in enumerate(set_to_update):
        display_progress_bar(25, counter / len(set_to_update))
        if handle in obj_set:
            value = 2
        else:
            value = 0
        sql = 'UPDATE {} SET status = {} WHERE handle = \'{}\';'.format(table, value, handle)
        cur.execute(sql)

    if set_to_update:
        db_conn.commit()

    cur.close()
    return len(set_to_update)


if __name__ == '__main__':
    """
    Parameters for the script are:
    :path: path to the file where all capture conversations are stored. The conversations will be uploaded into memory.
           The uploaded object will contain the handles that interacted in the conversations. This is a MANDATORY
           parameter.
           
    :db: name of database in use
    
    :user: user which has access to database.

    :friends_path: path of folder where interacting Twitter accounts\' friends will be stored. This is not a MANDATORY 
                   parameter.
    
    :followers_path: path of folder where interacting Twitter accounts\' followers will be stored. This is not a 
                    MANDATORY parameter.
                    
    :tweets_path: path of folder where interacting Twitter accounts\' tweets will be stored. This is not a 
                    MANDATORY parameter.                    
    """
    if len(sys.argv) < 5:
        print('\nNot enough arguments..', file=sys.stderr)
        print('path, db, user, are MANDATORY parameters. At least ONE of the following MUST be provided: ' +
              'friends_path, followers_path or tweets_path', file=sys.stderr)
        print('Usage: ./main.py path=path-to-conversations <friends_path=path-to-friends-folder> ' +
              'db=database-name  user=database-user',
              file=sys.stderr)
        sys.exit(-1)

    params = conv.list2kwarg(sys.argv[1:])

    if 'path' not in params or 'db' not in params or 'user' not in params or \
            ('friends_path' not in params and 'followers_path' not in params and 'tweets_path' not in params):
        print('\npath, db, user, are MANDATORY parameters. At least ONE of the following MUST be provided: ' +
              'friends_path, followers_path or tweets_path', file=sys.stderr)
        print('Usage: ./main.py path=path-to-conversations <friends_path=path-to-friends-folder> ' +
              'db=database-name  user=database-user',
              file=sys.stderr)
        sys.exit(-1)

    if not os.path.isfile(params['path']):
        print('\nCould not find file where conversation are stored: {}'.format(params['path']), file=sys.stderr)
        sys.exit(-1)

    if 'friends_path' in params and not os.path.isdir(params['friends_path']):
        print('\nCould not find folder where Twitter accounts\' friends reside: {}'.format(params['friends_path']),
              file=sys.stderr)
        sys.exit(-1)

    if 'friends_path' in params and params['friends_path'][-1] != '/':
        params['friends_path'] = params['friends_path'] + '/'

    if 'followers_path' in params and not os.path.isdir(params['followers_path']):
        print('\nCould not find folder where Twitter accounts\' followers reside: {}'.format(params['followers_path']),
              file=sys.stderr)
        sys.exit(-1)

    if 'followers_path' in params and params['followers_path'][-1] != '/':
        params['followers_path'] = params['followers_path'] + '/'

    if 'tweets_path' in params and not os.path.isdir(params['tweets_path']):
        print('\nCould not find folder where Twitter accounts\' tweets reside: {}'.format(params['tweets_path']),
              file=sys.stderr)
        sys.exit(-1)

    if 'tweets_path' in params and params['tweets_path'][-1] != '/':
        params['tweets_path'] = params['tweets_path'] + '/'

    main(**params)

    sys.exit(0)
