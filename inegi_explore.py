import sys
from ftplib import FTP
import json
import re
import Queue as queue


def dir_walk(ftp, path, collection):    
    re_file_or_dir = re.compile(r'^[drwx\-]{10}')
    re_whitespace = re.compile(r'\s+')
    
    current_path = path
    q = queue.Queue()
    q.put(current_path)

    def process_lines(line):        
        if re_file_or_dir.match(line):
            line_parts = re_whitespace.split(line)
            this_path = current_path + '/' + line_parts[-1]

            x = collection
            for p in this_path.split('/'):
                if len(p)==0:
                    continue

                if not p in x:
                    x[p] = {}
                x = x.get(p)                    

            if line_parts[0][0] == 'd':
                q.put(this_path)

            x['file'] = (line_parts[0] != 'd')
            
    
    while not q.empty():
        current_path = q.get()
        ftp.cwd(current_path)
        ftp.retrlines('LIST', process_lines)

    return collection


def do_dir_walk(server, path, login, password):
    ftp = FTP(server)
    ftp.login(login, password) 
    col = {}
    print json.dumps(dir_walk(ftp, path, col), indent=2)


if __name__ == '__main__':
    if sys.argv[1].strip().lower() == 'dir':
        do_dir_walk(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])