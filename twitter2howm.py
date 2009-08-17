# coding=utf-8
# require python-twitter 0.7-devel
# see http://code.google.com/p/python-twitter/
import os, time
import twitter

def run(userid, dir, since_id, count = None):
    api = twitter.Api()
    last_status_id = None
    for page in range(0,16):
        statuses = api.GetUserTimeline(userid, count = count,
                                       since_id = since_id, page = page)
        if len(statuses) == 0:
            return last_status_id
        print 'page=%d' % page
        for s in statuses:
            write_howm(dir, s)
            if s.id > last_status_id:
                last_status_id = s.id

    return last_status_id

# .howmを書き込む
def write_howm(dir, s):
    #print s.id
    #print s.text.encode('utf-8')
    # ファイル名
    filename = 'tw-%d.howm' % s.id
    # howm日時
    created_utc = time.mktime(time.strptime(s.created_at,
                                            '%a %b %d %H:%M:%S +0000 %Y'))
    created = time.localtime(created_utc - time.timezone)
    howm_time = time.strftime('[%Y-%m-%d %H:%M]', created)

    year = time.strftime('%Y', created)
    dirname = dir + '/' + year

    # ファイルに出力する
    try:
        os.makedirs(dirname)
    except OSError:
        None
    f = open(dirname + '/' + filename, 'w')
    # utf-8 で出力する
    print >>f, '= tw:' + howm_time + '. ' + s.text.encode('utf-8')
    f.close()

    return s.id

# キャッシュファイルから最終ステータスIDを取得
def read_cache(filename):
    try:
        f = open(filename, 'r')
        line = f.readline()
        last_status_id = eval(line)
        f.close()
    except IOError:
        last_status_id = 1

    return last_status_id

# キャッシュファイルに最終ステータスIDを保存
def save_cache(filename, last_status_id):
    if last_status_id != None:
        f = open(filename, 'w')
        print >>f, repr(last_status_id)
        f.close()

if __name__=='__main__':
    userid = 'iyoda'
    count = 200
    dir = '/Users/iyoda/Documents/howm'
    cache_filename = '.twitter2howm.cache'

    last_status_id = read_cache(dir + '/' + cache_filename)
    status_id = run(userid, dir, last_status_id, count)
    save_cache(dir + '/' + cache_filename, status_id)
