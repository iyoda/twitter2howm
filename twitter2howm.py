# coding=utf-8
import os, time
import twitter

def run(userid, dir, last_created_utc, count = None):
    api = twitter.Api()
    since = time.strftime('%a %b %d %H:%M:%S %Y',
                          time.localtime(last_created_utc))
    statuses = api.GetUserTimeline(userid, count, since)
    statuses.reverse()
    for s in statuses:
        # ファイル名
        filename = 'tw-%d.howm' % s.id
        # howm日時
        created_utc = time.mktime(time.strptime(s.created_at,
                                                '%a %b %d %H:%M:%S +0000 %Y'))
        if last_created_utc < created_utc:
            # 最終取得日時
            last_created_utc = created_utc
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
        # euc-jp で出力する
        print >>f, '= tw:' + howm_time + '. ' + s.text.encode('utf-8')
        f.close()

    return last_created_utc

# キャッシュファイルから最終ステータス時刻を取得
def read_cache(filename):
    try:
        f = open(filename, 'r')
        line = f.readline()
        last_created_utc = eval(line)
        f.close()
    except IOError:
        last_created_utc = 0

    return last_created_utc

# キャッシュファイルに最終ステータス時刻を保存
def save_cache(filename, last_created_utc):
    f = open(filename, 'w')
    print >>f, repr(last_created_utc + 1)
    f.close()

if __name__=='__main__':
    userid = 'iyoda'
    count = 2000
    dir = '/Users/iyoda/Documents/howm'
    cache_filename = '.twitter2howm.cache'

    last_created_utc = read_cache(dir + '/' + cache_filename)
    last_created_utc = run(userid, dir, last_created_utc, count)
    save_cache(dir + '/' + cache_filename, last_created_utc)
