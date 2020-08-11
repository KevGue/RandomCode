import random, string, shutil, os

os.chdir('F:\\other_music')

extension = '.mp3'

for folder, subfolder, files in os.walk(os.getcwd()):
    for file in files:
        
        newString = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for i in range(10))
        if newString not in os.listdir():
            shutil.move(os.path.join(folder,file), os.path.join(folder,newString) + str(extension))
        else:
            continue
