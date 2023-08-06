import os
import shutil

def ask(text):
    r = ''
    while r.lower() not in ['y','n']:
        r = input(text+' [Y/N]: ')
        continue
    
    return r.lower() == 'y'

def mkpath(path):
    print('Making path "{}"'.format(path))
    try:
        if os.path.exists(path):
            if ask('"{}" directory found. Overwrite?'.format(path)):
                shutil.rmtree(path)
            else:
                return False
        os.makedirs(path, exist_ok=True)
        return True
    except OSError as e:
        print('Can`t make path "{}": {}'.format(path, str(e)))
        return False

def mkfile(path, content):
    print('Making file "{}"'.format(path))
    if os.path.exists(path):
        if ask('"{}" file found. Overwrite?'.format(path)):
            os.remove(path)
        else:
            return False
    
    with open(path, 'w+', encoding='utf-8') as file:
        file.write(content)
        file.close()
