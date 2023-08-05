#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import re
import traceback

from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader(searchpath="./doclever2md/tpl"))
api_tpl = env.get_template('api_template.md')


def fetch_api(api_json):
    apis = []
    for data in api_json["data"]:
        if not "type" in data:
            apis.append(data)
        else:
            if 1 == data["type"] and not "data" in data:
                apis.append(data)
            elif 0 == data["type"]:
                apis.extend(fetch_api(data))
    return apis


def fetch_mock(param, additional_params):
    pf = re.findall(r'.*详见\[(\w+?)参数说明\]\(#\w+参数说明\)$', param["remark"], re.MULTILINE | re.IGNORECASE)
    if pf:
        if param["type"] in ("object", 4):
            for additional_param in additional_params:
                if additional_param["name"] == pf[0]:
                    mock_param2 = {}
                    for param_item in additional_param["params"]:
                        mock_param2[param_item["name"]] = fetch_mock(param_item, additional_params)
                    return mock_param2
        elif param["type"] in ("array", 3):
            for additional_param in additional_params:
                if additional_param["name"] == pf[0] and "params" in additional_param and additional_param["params"]:
                    mock_param2 = {}
                    for param_item in additional_param["params"]:
                        mock_param2[param_item["name"]] = fetch_mock(param_item, additional_params)
                    return [mock_param2, ]
            return ""

        else:
            return 1 if param["type"] in (1, "number") else ""
    else:
        return (1 if param["type"] in (1, "number") else "") if "mock" not in param else param["mock"]


def fetch_addtional_params(param_json, name, type):
    params = []
    params2 = []
    for child_param_json in param_json["data"]:
        child_param = {"type": type_map[child_param_json["type"]], "must": must_map[child_param_json["must"]],
                       "name": child_param_json["name"], "remark": child_param_json["remark"],
                       "mock": child_param_json["mock"]}
        params2.append(child_param)
        if child_param_json["type"] in (4, 3):
            if child_param_json["name"] is None:
                child_param_json["name"] = name + "数组元素"
            child_param["remark"] += ("," if child_param_json["remark"] else "") + "详见[" + child_param_json[
                "name"] + "参数说明](#" + \
                                     child_param_json["name"] + "参数说明)"
    params.append({"name": name, "params": params2, "type": type})
    for child_param_json in param_json["data"]:
        if child_param_json["type"] in (4, 3):
            params.extend(fetch_addtional_params(child_param_json, child_param_json["name"], child_param_json["type"]))
    return params


def remove_none_key(mock_json):
    for i, v in mock_json.items():
        if v and isinstance(v, list):
            if len(v) == 1:
                if isinstance(v[0], dict) and len(v[0].keys()) == 1 and list(v[0].keys())[0] is None:
                    v[0] = list(v[0].values())[0]
                else:
                    remove_none_key(v[0])
            else:
                for vv in v:
                    if isinstance(vv, dict):
                        remove_none_key(vv)

        elif isinstance(v, dict):
            remove_none_key(v)


"""
0是字符串 1是数 3是数组 2是boolean 4是obj
"""

type_map = {
    0: "string",
    1: "number",
    2: "bool",
    3: "array",
    4: "object",
    5: "mixed",
    'multipart/form-data': 'multipart/form-data'
}

must_map = {
    0: "否",
    1: "是"
}


def main():
    import argparse
    parser = argparse.ArgumentParser("--file指定doclever输出的json文件路径,--output_dir指定markdown输出的文件夹")
    parser.add_argument('--file', type=str, help='doclever输出的json文件路径')
    parser.add_argument('--output_dir', type=str, help='markdown输出文件夹')
    args = parser.parse_args()
    api_json = json.load(open(args.file))
    apis = fetch_api(api_json)
    for api in apis:
        try:
            api_name = api["name"].strip()
            api_params = api["param"][0]["restParam"] if api["param"][0]["restParam"] else \
                [{"name": "file", "type": "multipart/form-data", "remark": "上传的文件", "must": 1, "mock": ""}] \
                    if api["param"][0]["bodyInfo"]["rawType"] == 1 \
                    else api["param"][0]["bodyInfo"]["rawJSON"]
            api_responses = api["param"][0]["outParam"]
            additional_params, additional_responses = [], []
            mock_param = {}
            mock_resp = {}
            for api_param in api_params:

                api_param["type"] = "" if "type" not in api_param else type_map[api_param["type"]]
                api_param["must"] = "是" if "must" not in api_param else must_map[api_param["must"]]
                if api_param["type"] in ("object", "array"):
                    api_param["remark"] += ("," if api_param["remark"] else "") + "详见[" + api_param["name"] + (
                        "数组元素" if api_param["type"] == "array" else "") + "参数说明](#" + \
                                           api_param["name"] + "参数说明)"
                    additional_params.extend(fetch_addtional_params(api_param, api_param["name"], api_param["type"]))

            for api_resp in api_responses:
                api_resp["type"] = type_map[api_resp["type"]]
                if api_resp["type"] in ("object", "array"):
                    api_resp["remark"] += ("," if api_resp["remark"] else "") + "详见[" + api_resp["name"] + (
                        "数组元素" if api_resp["type"] == "array" else "") + "参数说明](#" + \
                                          api_resp["name"] + "参数说明)"
                    additional_responses.extend(fetch_addtional_params(api_resp, api_resp["name"], api_resp["type"]))

            # 生成参数及响应的json范例
            for api_param in api_params:
                mock_param[api_param["name"]] = fetch_mock(api_param, filter(
                    lambda x: x["type"] != "array" or x['name'].endswith("数组元素"), additional_params))
            for api_resp in api_responses:
                mock_resp[api_resp["name"]] = fetch_mock(api_resp, filter(
                    lambda x: x["type"] != "array" or x['name'].endswith("数组元素"), additional_responses))

            remove_none_key(mock_param)
            remove_none_key(mock_resp)
            print(mock_resp)
            api_meta = {
                "api_name": api_name,
                "api_desc": "" if "remark" not in api else api["remark"],
                "api_method": api["method"],
                "api_uri": api["url"],
                "api_params": api_params,
                "additional_params": additional_params,
                "api_param_example": json.dumps(mock_param, indent=4, sort_keys=True),
                "api_response": api_responses,
                "additional_responses": additional_responses,
                "api_response_example": json.dumps(mock_resp, indent=4, sort_keys=True)

            }
            with open("%s/%s.md" % (args.output_dir, api_name), "w+") as rf:
                rf.write(api_tpl.render(api_meta))

        except Exception as err:
            traceback.print_exc()
            print(api["param"])
            print("err,", api["name"], api["url"])
            continue


if __name__ == '__main__':
    main()
