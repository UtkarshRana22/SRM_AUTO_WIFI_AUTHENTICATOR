import os,shutil
if os.path.exists(os.getcwd()+"\\temp"): shutil.rmtree(os.getcwd()+"\\temp")
if os.path.exists("_internal") and os.path.exists("AWA.exe") and os.path.exists("_internal.zip"):
    os.makedirs(os.getcwd()+"\\"+"temp",exist_ok=True)
    print("made directory......")
    if  os.path.exists("temp"):
        shutil.move(os.getcwd()+"\\_internal",os.getcwd()+"\\temp")
        shutil.move(os.getcwd()+"\\AWA.exe",os.getcwd()+"\\temp")
        print("making backup.....")
    try:
        print("unpacking......")
        shutil.unpack_archive("_internal.zip",os.getcwd())
        print("cleaning up.......")
        shutil.rmtree(os.getcwd()+"\\temp")
        os.remove(os.getcwd()+"\\_internal.zip")
        os.execl("AWA.exe","AWA.exe")
    except Exception as e:
        print(e,"rolling back.......")
        shutil.move(os.getcwd()+"\\temp\\_internal",os.getcwd())
        shutil.move(os.getcwd()+"\\temp\\AWA.exe",os.getcwd())
        

