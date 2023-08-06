""" A simple API wrapper for FTPing files 

    you should be able to this:

    from ftpretty import ftpretty
    f = ftpretty(host, user, pass, secure=False, timeout=10)
    f.get(remote, local)
    f.put(local, remote)
    f.list(remote)
    f.cd(remote)
    f.delete(remote)
    f.close()
    
"""
from ftplib import FTP, FTP_TLS
import os
import cStringIO
import re
import datetime

class ftpretty(object):
    conn = None

    def __init__(self, host, user, password, secure=False, **kwargs): 
        if secure:
            self.conn = FTP_TLS(host=host, user=user, passwd=password, **kwargs)
            self.conn.prot_p()
        else:
            self.conn = FTP(host=host, user=user, passwd=password, **kwargs)
        
    def __getattr__(self, name):
        """ Pass anything we don't know about, to underlying ftp connection """
        def wrapper(*args, **kwargs):
            method = getattr(self.conn, name)
            return method(*args, **kwargs)
        return wrapper


    def get(self, remote, local=None):
        """ Gets the file from FTP server

            local can be:
                a string: path to output file
                a file: opened for writing
                None: contents are returned
        """       
        if isinstance(local, file):
            local_file = local
        elif local is None:
            local_file = cStringIO.StringIO()
        else:   
            local_file = open(local, 'wb')

        self.conn.retrbinary("RETR %s" % remote, local_file.write)

        if isinstance(local, file):
            local_file = local
        elif local is None:
            contents = local_file.getvalue()
            local_file.close()
            return contents
        else:   
            local_file.close()

        return None


    def put(self, local, remote, contents=None):
        """ Puts a local file (or contents) on to the FTP server 

            local can be:
                a string: path to inpit file
                a file: opened for reading
                None: contents are pushed
        """       
        remote_dir = os.path.dirname(remote)
        remote_file = os.path.basename(remote)
        if contents:
            # local is ignored if contents is set
            local_file = cStringIO.StringIO(contents)
        elif isinstance(local, file):
            local_file = local
        else:
            local_file = open(local, 'rb')
        current = self.conn.pwd()
        self.descend(remote_dir, force=True)
        self.conn.storbinary('STOR %s' % remote_file, local_file)
        local_file.close()
        self.conn.cwd(current)
        return self.conn.size(remote)


    def list(self, remote='.', extra=False):
        """ Return directory list """
        if not extra:
            return self.conn.nlst(remote)
        self.tmp_output = []
        self.conn.dir(remote, self._collector)
        return self.split_file_info(self.tmp_output)


    def _collector(self, line):
        self.tmp_output.append(line)


    def descend(self, remote, force=False):
        """ Descend, possibly creating directories as needed """
        remote_dirs = remote.split('/')
        for dir in remote_dirs:
            try:
                self.conn.cwd(dir)
            except:
                if force:
                    self.conn.mkd(dir)
                    self.conn.cwd(dir)
        return self.conn.pwd()


    def delete(self, remote):
        return self.conn.delete(remote)


    def cd(self, remote):
        self.conn.cwd(remote)
        return self.pwd()


    def pwd(self):
        return self.conn.pwd()


    def close(self):
        try:
            self.conn.quit()
        except:
            self.conn.close()


    def split_file_info(self, fileinfo):
        """ Parse sane directory output usually ls -l
            Adapted from https://gist.github.com/tobiasoberrauch/2942716 
        """
        current_year = datetime.datetime.now().strftime('%Y')
        files = []        
        for line in fileinfo:
            parts = re.split(
                '^([\\-dbclps])' +                # Directory flag [1]
                '([\\-rwxs]{9})\\s+' +            # Permissions [2]
                '(\\d+)\\s+' +                    # Number of items [3]
                '(\\w+)\\s+' +                    # File owner [4]
                '(\\w+)\\s+' +                    # File group [5]
                '(\\d+)\\s+' +                    # File size in bytes [6]
                '(\\w{3}\\s+\\d{1,2})\\s+' +       # 3-char month and 1/2-char day of the month [7]
                '(\\d{1,2}:\\d{1,2}|\\d{4})\\s+' + # Time or year (need to check conditions) [+= 7]
                '(.+)$'                       # File/directory name [8]
                , line)
            files.append({
                'directory': parts[1],
                'perms': parts[2],
                'items': parts[3],
                'owner': parts[4],
                'group': parts[5],
                'size': parts[6],
                'date': parts[7],
                'time': parts[8] if ':' in parts[8] else '00:00',
                'year': parts[8] if ':' not in parts[8] else current_year,
                'name': parts[9]
                }) 
        return files

