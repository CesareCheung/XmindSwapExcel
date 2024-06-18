def fileExtract(para):
    paraList={}
    with open('excelPara.ini', 'r', encoding='utf-8') as f:
        data = f.readlines()
        for line in data:
            if "=" in line:
                key, value = line.strip('\r\n').split("=", 1)
            elif ":" in line:
                key, value = line.strip('\r\n').split(":", 1)
            paraList[key]=value
    return paraList[para]

if __name__ == '__main__':
    print(fileExtract('prodectName'))