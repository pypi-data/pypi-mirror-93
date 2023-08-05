## {{api_name}}

{{api_desc}}

### 请求地址

```
{{api_method}} {{api_uri}}
```

### 请求参数说明

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
{% for param in api_params %}|{{'-' if param.name == None else param.name}}|{{param.type}}|{{param.must}}|{{param.remark}}|
{% endfor %}


{% for param in additional_params %}
### {{param.name}}参数说明
| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
{% for inner_param in param.params %}|{{'-' if inner_param.name == None else inner_param.name}}|{{inner_param.type}}|{{inner_param.must}}|{{inner_param.remark}}|
{% endfor %}
{% endfor %}

**{{api_method}} 数据示例：**

```
{{api_param_example}}
```

### 返回参数说明

| 参数 | 类型 | 说明 |
| --- | --- | --- |
{% for resp in api_response %}|{{'-' if resp.name == None else resp.name}}|{{resp.type}}|{{resp.remark}}|
{% endfor %}


{% for resp in additional_responses %}
### {{resp.name}}参数说明
| 参数 | 类型 | 说明 |
| --- | --- | --- | --- |
{% for inner_resp in resp.params %}|{{'-' if inner_resp.name == None else inner_resp.name }}|{{inner_resp.type}}|{{inner_resp.remark}}|
{% endfor %}
{% endfor %}


**返回结果示例：**

```
{{api_response_example}}
```