from auto_generation_pytest.combination.combination_case import Comb
from auto_generation_pytest.get_case import CaseData
import os
import json
import random
from proxy.res_filter import filter_response
from jsondiff import diff
import string
from string import Template

def grpc_request_format(d, case):
    params = '''\t\tRequest = BaseRpc(\'{}\', \'{}\')\n\t\tr = Request.send(\'{}\',\'{}\',{})\n'''.format(d['url'], d['proto'], d['server'], d['request'], 'params')
    return params.replace('{', '##+##').replace('}', '##-##')

def http_request_format(d, case):
    if 'url' in d and d['url'] != '':
        params = '''\t\tRequest = HttpRequest()\n\t\tr = Request.send(\'{}\', \'{}\', {}, {}, url=\'{}\')\n'''.format(
            d['api'], d['method'], 'params', d['head'], d['url'])
    else:
        params = '''\t\tRequest = HttpRequest()\n\t\tr = Request.send(\'{}\', \'{}\', {}, {})\n'''.format(
            d['api'], d['method'], 'params', d['head'])
    return params.replace('{', '##+##').replace('}', '##-##')

def combination_requeset(d, case):
    if d['method'] == 'grpc':
        return grpc_request_format(d, case)
    else:
        return http_request_format(d, case)

def comb_data(data):
    output = []
    for temporary in data:
        i = temporary.copy()
        # 获取当前数据的组合方式
        comb_method = i.pop('comb')
        # 根据变量的组合方式，进行变量组合
        comb = Comb(i)
        if comb_method in ['allpairs', 'multiply', 'normal']:
            i['var'] = getattr(comb, comb_method)()
            output += comb.fusion(i)
        elif comb_method in ['random']:
            output += comb.random()
        elif i['data']:
            output.append(i['data'])
    if output == ['']:
        output = [{}]
    return output

def add_file(path):
    try:
        if not os.path.exists(path):
            os.mkdir(path)
    except Exception as e:
        print('创建' + path + '目录失败' + str(e))

def init_py(path, pyname):
    path += pyname + '.py'
    try:
        if not os.path.exists(path):
            fd = open(path, "w", encoding="utf-8")
            fd.close()
    except Exception as e:
        print('创建' + path + ' ' +pyname + '失败' + str(e))

def load_josn(name):
    with open(name, 'r') as f:
        data = json.load(f)
    return data

def set_config(v, data):
    if v == '':
        return data

    data = json.dumps(data)
    config = {}

    if isinstance(v,list):
        for i in v:
            config[i[0]] = i[1]
    else:
        config = v

    for key, value in config.items():
        name = '$' + key

        if isinstance(value,str):
            if 'env(' in value:
                value = value.replace('env(','').replace(')','').strip('\'').strip('"')
                value = os.getenv(value)
        if isinstance(value,str):
            data = data.replace(name,str(value))
        else:
            random_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
            value = random_str + str(value).replace('\'','"') +random_str
            data = data.replace(name,str(value))
            data = data.replace('"'+random_str,'').replace(random_str+'"','')

    data = json.loads(data)
    return data

def r_json(load,data):
    for x in data:
        try:
            x = int(x)
            load += '[{}]'.format(x)
        except Exception :
            load += '[\'{}\']'.format(x)
    return load

def get_extract(key):
    v = os.getenv(key)
    t = os.getenv(key+'-type')
    if t:
        t = str(t).replace('<class \'','').replace('\'>','')
        v = eval(str(t)+'('+str(v)+')')
    return v

def set_extract(key, value):
    os.environ[key] = str(value)
    key += '-type'
    t = type(value)
    os.environ[key] = str(t)

def replace_extract(data):
    config = {}
    for i in list(os.environ.keys()):
        if '-type' in i:
            continue
        if '#' == i[0]:
            continue
        config[i] = get_extract(i)
    data = set_config(config,data)
    return data

def response_diff(name, index, url, method, new):
    old = CaseData().get_record(name + '_record.json', index)
    old = replace_extract(old)
    info_init = "old: " + str(old) + '\n' + 'new: ' + str(new) + '\ndiff: '
    new = filter_response(url,method,new)

    info = str(diff(new, old))
    if info == '{}':
        info = ''
    else:
        info = info_init + info
    return info


def set_env():
    path = os.getcwd()+'/.env'
    env = {}
    if os.path.exists(path):
        with open(path, "r") as f:
            for i in f:
                if "=" in i:
                    key, value = i.split("=")
                    os.environ[key] = value.strip()