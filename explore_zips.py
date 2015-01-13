import sys, json, subprocess, os, shutil, tempfile, sqlite3

if __name__ == '__main__':
    db = sqlite3.connect('inegi.db')
    conn = db.cursor()

    j = None

    def _is_zip(filename):
        return filename.split('.')[-1].lower() == 'zip'

    def _test_zip(path, filename):
        conn.execute("SELECT contents FROM inegi_files WHERE filename=?", ((path + '/' + filename),))
        row = conn.fetchone()
        if row is not None:
            return row[0]
        else:
            url = 'ftp://rgnaftp:rgnaftp@geodesia.inegi.org.mx' + (path + '/' + filename).replace('/home/rgna', '')
            print 'fetching %s' % url
        try:                    
            tmpdir = tempfile.mkdtemp()
            subprocess.check_call(['curl', url, '-o', tmpdir + '/out.zip'])
            lszip = subprocess.check_output(['unzip', '-l', tmpdir + '/out.zip'])
            shutil.rmtree(tmpdir)
            conn.execute("INSERT INTO inegi_files (filename, contents) VALUES (?, ?)", ((path + '/' + filename), lszip))
            db.commit()
            return lszip
        except Exception, e:
            shutil.rmtree(tmpdir)
            return 'Error'                

    def recurse_c(branch, path=''):
        if type(branch) is dict:                
            keys = branch.keys()
            for k in keys:
                branch[k] = recurse_c(branch[k], path + '/' + k)

        if type(branch) is list:
            new_branch = {}
            tested_zip = False
            for k in branch:                
                if _is_zip(k) and not tested_zip:                    
                    new_branch[k] = _test_zip(path, k)
                    print new_branch[k]
                    tested_zip = True
                else:
                    new_branch[k] = ''
            branch = new_branch

        return branch


    with open(sys.argv[1], 'r') as f:
        j = json.load(f)
        j = recurse_c(j)

    conn.close()