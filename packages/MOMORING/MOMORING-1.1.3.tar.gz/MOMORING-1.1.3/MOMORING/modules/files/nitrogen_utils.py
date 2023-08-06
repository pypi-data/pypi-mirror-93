def nitrogen_utils():
    txt = '''\
import os
import shutil
import math


def get_path():
    datapath = os.environ.get('DATAPATH')
    savedpath = os.environ.get('SAVEDPATH')
    stashpath = os.environ.get('STASHPATH')
    return datapath, savedpath, stashpath
    

def get_cpu_num():
    """Get n_cpu, return NUM_CPU if user specified, else os.cpu_count()"""
    n_cpu = os.getenv('NUM_CPU')
    all_cpu = os.cpu_count()-1 if os.cpu_count() > 1 else 1

    if not n_cpu:
        n_cpu = all_cpu
    else:
        n_cpu = int(n_cpu)
        if n_cpu > all_cpu:
            n_cpu = all_cpu

    limit = os.getenv('CPU')
    if limit:
        n_cpu = math.ceil(int(limit)*2/3)

    print(f'n_cpu:{n_cpu}, limit:{limit}')
    return n_cpu


def create_workdir(dir_name='workdir'):
    stashpath = os.getenv('STASHPATH')
    if stashpath:
        # xbcp
        workdir = os.path.join(stashpath, dir_name)
    else:
        # local
        workdir = os.path.join('/home/', dir_name)

    if os.path.exists(workdir):
        shutil.move(workdir, workdir.replace(dir_name, 'trash'))
    os.mkdir(workdir)
    return workdir


def get_env_param(env_str, default_value=None, type_func=str):
    value = os.getenv(env_str)
    if (value == True or value == False) and type_func == eval:
        return value
    if value:
        value = type_func(value)
    else:
        value = default_value
    print('ENV:', env_str, '| VALUE:', value, '| TYPE:', type(value))
    return value
    
    
class GetInputData:
    def __init__(self):
        self.datapath = '/job/data/'
        self.files = [os.path.join(self.datapath, i) for i in os.listdir(self.datapath)]
        
    def by_extension(self, ext):
        return [i for i in self.files if i.endswith(ext)]

    def by_name(self, file_name):
        return [i for i in self.files if os.path.basename(i) == file_name or i == file_name][0]
'''
    return txt
