# PF-Scanner

## How it works

```bash
usage: PF-scanner [-h] [--type TYPE] [--version]

optional arguments:
  -h, --help            show this help message and exit
  --type TYPE, -T TYPE  The type of device you want to get information about (possible: Fan, Power Supply)
  --version, -V         This key allows you to get the current version
```

**Example #1**:

```bash
> docker build -t pf-scanner .
> docker run -ti --rm  --privileged --env INVMODE='Power Supply' pf-scanner
```

```json
{
  "PF-scanner": [
    "Could not open device at /dev/ipmi0 or /dev/ipmi/0 or /dev/ipmidev/0: No such file or directory\n"
  ]
}
```

**Example #2**:

```bash
> docker build -t pf-scanner .
> docker run -ti --rm  --privileged --env INVMODE='Fan' pf-scanner
```

```json
{
  "PF-scanner": [
    {
      "FAN1": {
        "SensorName": "41h",
        "State": "ok",
        "Instance": "29.1",
        "Speed": "13200 RPM"
      },
      "FAN2": {
        "SensorName": "42h",
        "State": "ok",
        "Instance": "29.2",
        "Speed": "13400 RPM"
      },
      "FAN3": {
        "SensorName": "43h",
        "State": "ok",
        "Instance": "29.3",
        "Speed": "13500 RPM"
      },
      "FAN4": {
        "SensorName": "44h",
        "State": "ok",
        "Instance": "29.4",
        "Speed": "13400 RPM"
      },
      "FAN5": {
        "SensorName": "45h",
        "State": "ns",
        "Instance": "29.5",
        "Speed": "No Reading"
      },
      "FANA": {
        "SensorName": "47h",
        "State": "ns",
        "Instance": "29.7",
        "Speed": "No Reading"
      }
    }
  ]
}
```

**Example #3**:

```bash
>  docker build --tag pf-scanner
> docker run -ti --rm  --privileged pf-scanner
```

```json
{
  "PF-scanner": [
    {
      "PSU_total": 2,
      "1": {....},
      "2": {....}
    }
  ]
}
```

## Code style

⚠️ To format and lint already modified code, run **[./format.sh](format.sh)**, but set **flake8** and **yapf** before running if necessrary

## License

See the [LICENSE](LICENSE) file for license rights and limitations (MIT).
