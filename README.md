## How it works

```
usage: PF-Checker [-h] [--type TYPE] [--version]

options:
  -h, --help            show this help message and exit
  --type TYPE, -T TYPE  The type of device you want to get information about (possible: Fan, Power Supply)
  --version, -V         This key allows you to get the current version
```

**Example #1**:
```bash
> docker build -t pf-checker:0.1.0 .
> docker run -ti --rm  --privileged --env INVMODE='Power Supply' pf-checker
```
**Example #2**:
```bash
> docker build -t pf-checker:0.1.0 .
> docker run -ti --rm  --privileged --env INVMODE='Fan' pf-checker
```

**Example #3**:
```bash
>  docker build --tag pf-checker:0.1.0  https://github.com/Operator2024/PF-checker.git
> docker run -ti --rm  --privileged --env INVMODE='Fan' pf-checker
```

## License

See the [LICENSE](LICENSE) file for license rights and limitations (MIT).

