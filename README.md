# Validation Role

## 1.0.0

### Variables

| Variable | Defaults | Description |
| -------- | -------- | ----------- |
| validations | | List of validation rules |


### Rules

- ipv4
- ipv6
- port
- email
- host
- integer
- float
- number

### Install

`ansible-galaxy install git+git@github.com:revl-ca/validation-role.git -p roles`

### Usage

roles/&lt;role&gt;/vars/main.yml:

```
---
machine:
  host: 192.168.1.2
  port: 1234
  email: steve@revl.ca
  long:
    path:
      possible: true

<role>_validations:
- path: machine.host
  match: ipv4
- path: machine.port
  match: port
- path: machine.email
  match: email
- path: machine.long.path.possible

```

roles/&lt;role&gt;/meta/main.yml:

```
---
dependencies:
- role: validation-role
  validations: "{{ <role>_validations }}"
  tags:
  - validate
```

### Example output

```
TASK [validation-role : debug]
fatal: [localhost]: FAILED! => {"msg": "Variable 23.112.45.95 is not a valid ipv6."}
```

### Possible issues

```
TASK [validation-role : debug]
fatal: [localhost]: FAILED! => {"msg": "Unexpected failure during module execution."}
```

Solution: `pip install --user -r roles/validation-role/requirements.txt`
