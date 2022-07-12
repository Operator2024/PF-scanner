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
> docker build -t PF-checker:latest .
> docker run -ti --rm  --privileged --env INVMODE='Power Supply' PF-checker
```
**Example #2**:
```bash
> docker build -t PF-checker:latest .
> docker run -ti --rm  --privileged --env INVMODE='Fan' PF-checker
```

## License

See the [LICENSE](LICENSE) file for license rights and limitations (MIT).

