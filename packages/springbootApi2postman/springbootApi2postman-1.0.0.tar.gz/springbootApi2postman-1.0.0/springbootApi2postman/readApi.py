#！/bin/bash

'''
该模块主要用于读取SpringBoot项目中controller层
将接口信息编辑成json文件，用于postman进行接口测试
'''
import re,time,os


'''
获取文件中的接口信息
'''
def getApis(dir,dispath='',protocla='http',host='',clloction_name='Read4j',headers=None,filter=[],scripts=None) -> dict:
    '''
    :param file:  文件绝对路径
    :return: 返回一个dict
    '''

    # 扫描目录获取java文件
    ab_path = os.path.abspath(dir)
    files = os.listdir(dir)

    # 声明一个postman格式的dict，包含指定信息
    pm_data_dict = {
        "info": {
            "name": clloction_name,
            "schema": "https://schema.getpostman.com/json/collection/v2.0.0/collection.json"
        },
        "item": []
    }

    # 遍历文件
    for file in files:
        with open(os.path.join(ab_path,file), 'r', encoding='UTF-8') as fp:
            txt = fp.read()
        if not txt:return pm_data_dict
        if not txt:continue
        # 匹配接口路径
        api_base_list = re.findall('@(RequestMapping|GetMapping|PostMapping)(.*?)(\))', txt)
        api_params_list = re.findall('(public)([a-z,A-Z,0-9,<,>\s]*)\(([a-zA-z\s,@\(="\)]*){', txt)
        api_names_list = [ params_tuple[1].strip().split(' ')[-1].strip() for params_tuple in api_params_list ]
        # 判断如果两个list长度，不想等说明匹配有遗漏或者错误
        if len(api_base_list) != len(api_params_list): return pm_data_dict

        # 遍历list 进行组装
        for key,api in enumerate(api_base_list):
            new_item = opt_model(api,api_params_list[key],api_names_list[key],dispath=dispath,host=host,filter=filter,headers=headers,scripts=scripts)
            pm_data_dict['item'].append(new_item)

    return pm_data_dict

'''
处理postman model
'''
def opt_model(api_tuple,params_tuple,name,dispath='',protocla='http',host='',filter=[],headers=[],scripts=None):

    # postman GET请求模版
    get_model = {
        "name": None,
        "event":[],
        "request": {
            "method":"GET",
            "header":headers,
            "url": {
                "raw": None,
                "protocal":protocla,
                "host":host.split('.'),
                "path":None,
                "query":[]
            }
        },
        "response": []
    }
    # postman POST请求模版
    post_model = {
        "name": None,
        "event":[],
        "request": {
            "method": "POST",
            "header":headers,
            "body":{
                "mode": "urlencoded",
                "urlencoded": []
            },
            "url": None
        },
        "response": []
    }

    # 处理通用脚本
    if scripts is not None:
        script_dict = 	{
            "listen": "test",
            "script": {
                "exec": scripts,
                "type": "text/javascript"
            }
		}
        get_model['event'].append(script_dict)
        post_model['event'].append(script_dict)
    # 解析请求方式
    requst_method = "POST" if api_tuple[0].strip()=="PostMapping" else "GET"
    # 解析接口名称
    request_name = name
    # 解析请求路径
    request_path = dispath + api_tuple[1].split("\"")[1]
    if requst_method == "GET":
        get_model['name'] = name
        get_model['request']['url']['host'] = host.split('.')
        get_model['request']['url']['path'] = request_path.split('/')
    else:
        post_model['name'] = name
        post_model['request']['url'] = '{0}://{1}/{2}'.format(protocla,host,request_path)


    # 解析接口参数
    request_params = [param.strip() for param in params_tuple[-1].strip().strip(')').split(',')]
    for key,params_str in enumerate(request_params):
        if '@RequestParam' in params_str:
            real_param_name = re.findall('@RequestParam\((value\s=\s*)*[\"|\']\s*([a-zA-Z]*)',params_str)[0][-1]
            temp_list = params_str.split(')')[-1].split(' ')
            temp_list[-1] = real_param_name
            real_param_str = ' '.join(temp_list)
            request_params[key] = real_param_str

    # 过滤和初始化
    get_params_str = '?'
    for item in request_params:

        param_dict = dict()
        # 获取数据类型
        data_kv = item.split(' ')
        data_type = data_kv[0]
        data_name = data_kv[-1]

        # 如果是过滤函数类型，直接跳过
        data_val = ''   # 无法判断类型
        if data_type in filter:continue
        # 判断数据类型
        if data_type in ('Integer','int'):
            data_val = "1"
        if data_type in ('Float','float'):
            data_val = "0.8"
        if data_type in ('Double','double'):
            data_val = "0.08"
        if data_type in ('long','Long'):
            data_val = "%d" % int(time.time()*1000)
        if data_type == 'Boolean':
            data_val = "true"
        if data_type == "String":
            data_val = "test"
        param_dict['key'] = data_name
        param_dict['value'] = data_val
        param_dict['type'] = 'text'

        kv_str = '{0}={1}&'.format(data_name,data_val)
        get_params_str+=kv_str

        if requst_method == "GET":
            get_model['request']['url']['query'].append(param_dict)
        else:
            post_model['request']['body']['urlencoded'].append(param_dict)


    # 组装get请求的raw
    get_request_raw = "{0}://{1}/{2}{3}".format(protocla,host,request_path,get_params_str.strip('&')).strip('?')
    get_model['request']['url']['raw'] = get_request_raw

    return get_model if requst_method == "GET" else post_model

