'''
Name: 命令生成
Author: 六记
Date: 2021-04-17 08:46:58
Descripttion: 命令生成器，%program% -f %inputFiles% -o %outputFiles%
version:
LastEditTime: 2021-04-27 12:48:36
LastEditors: Please set LastEditors
FilePath: \\年会开场程序c:\\Users\\10436\\Desktop\\新建文件夹\\ComGen.py
'''
import configparser
import os
import sys
import re
from prettytable import PrettyTable
configs = {
    'confPath': './Command.config',  # 配置文件
    'confFormat': {  # 命令生成格式
        'default': {
            'format':'我考了{分数}分',
            'example':'我考了100分'
        }
    },
    'parms': [],  # 参数
    'select': 'default'  # 选择模板
}


def saveConf():
    '''保存配置文件'''
    path = configs['confPath']
    conf = configparser.ConfigParser()
    for key in configs['confFormat'].keys():
        if not conf.has_section(key):
            conf.add_section(key)
        if isinstance(configs['confFormat'][key], dict):
            conf[key]['format'] = configs['confFormat'][key]['format']
            conf[key]['example'] = configs['confFormat'][key]['example']
    with open(path, 'w', encoding='utf-8') as f:
        conf.write(f)


def readFormat():
    '''读取配置文件:获取命令格式化'''
    global configs
    path = configs['confPath']
    conf = configparser.ConfigParser()
    conf.read(path, encoding='utf-8')
    keys = conf.sections()
    for key in keys:
        nDict = dict()
        if 'format' in conf.options(key):
            nDict['format'] = conf.get(key, 'format')  # 提取命令格式
            configs['confFormat'][key] = nDict
        if 'example' in conf.options(key):
            nDict['example'] = conf.get(key, 'example')  # 提取命令格式的例子
            configs['confFormat'][key] = nDict


def select(key, argv):
    '''选择格式'''
    global configs
    index = argv.index(key)
    key = argv[index+1]
    configs['select'] = key


def formats(key, argv):
    '''修改配置：格式'''
    global configs
    index = argv.index(key)
    formatString = argv[index+1]
    if formatString:
        # 用于区分读取的例子，读取的例子为字典，而临时的则为字符串
        configs['confFormat']['default']['format'] = formatString
        configs['confFormat']['default']['format'] = None


def slist(*argv):
    ''''''
    formats = configs['confFormat']
    # print(formats)
    # msg = ''
    tb = PrettyTable()
    tb.field_names = ['选项', '格式', '例子']
    tb.align['格式'] = 'l'
    tb.align['例子'] = 'l'
    for key in formats:
        tb.add_row([key, formats[key]['format'], formats[key]['example']])
    print(tb)


def helpme(*argv):
    '''帮助信息'''
    Thelp = """
    ComGen.exe [] []...
    命令生成器\n
    -h,-help\t\t获取帮助信息
    -l,-list,list\t获取格式列表
    -p,-parms\t\t添加参数 例子: -p 参数1 参数2 参数3
    -f,-format\t\t临时格式样式 例子: -f 我{外号},是个{称号}\n\t\t\t\t-f "我{外号} 是个{称号}"
    -c,-conf\t\t配置文件信息 例子: -conf 配置文件位置
    -s,-select\t\t选择模板
    """
    print(Thelp)


def parms(key, argv):
    '''修改配置:参数'''
    global configs
    index = argv.index(key)
    while True:
        try:
            index += 1
            parm = argv[index]
            if parm in commadKeys.keys():
                return
            configs['parms'].append(parm)
        except:
            return


def conf(key, argv):
    '''修改配置:配置文件位置'''
    global configs
    index = argv.index(key)
    filePath = argv[index+1]
    if os.path.exists(filePath) and os.path.isfile(filePath):
        configs['confPath'] = os.path.abspath(filePath)


def readCom(argv):
    '''命令读取'''
    returnList = ['-h', '-l', '-help', '-list', 'list']  # 不继续执行的命令
    if(os.path.exists(configs['confPath'])):
        readFormat()
        commandCount = 0  # 是否含有命令
        for key in commadKeys:
            if key in argv:
                commandCount += 1
                commadKeys[key](key, argv)
                if key in returnList:
                    return
        if commandCount == 0:  # 不存在任何命令指令
            return

        if '-p' in argv or '-parms' in argv:
            parm = configs['parms']
            confFormat = configs['confFormat']
            s = configs['select']
            formatText = confFormat[s]
            if isinstance(formatText, dict):
                formatText = formatText['format']
            keys = re.findall('{(.*?)}', formatText)
            if len(keys) > len(configs['parms']):
                print(f'错误:参数不全,一共需要{len(keys)}个参数({",".join(keys)})')
                return
            f = dict()
            for index, key in enumerate(keys):
                f[key] = parm[index]
            print(formatText.format(**f))
        else:
            print('错误:缺少相关参数')
    saveConf()


commadKeys = {
    '-h': helpme,
    '-help': helpme,
    '-l': slist,
    '-list': slist,
    'list': slist,
    '-s': select,
    '-select': select,
    '-p': parms,
    '-parms': parms,
    '-c': conf,
    '-conf': conf,
    '-f': formats,
    '-format': formats
}


if __name__ == '__main__':
    readCom(sys.argv)
