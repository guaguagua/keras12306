def renamePicture(start):
    #start = 20000
    for filename in glob.glob(r'./*.png'):
        print(filename)
        os.rename(filename,r'./%s.png' % (start))
        start += 1
        #break
    print('rename end...')