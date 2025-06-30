# Can I charge?

It's a question you might have asked yourself before if you have a BEV/PHEV.
This utility allows you to check if your favorite charging stations are available
for your car to charge, right from the warmth of your terminal! No need to go
outside and physically check if the charging station is available, and possibly
return disappointed because it was occupied.

## How to install

### Using pip

```bash
$ pip install can-i-charge
```

### AUR

A PKGBUILD has been created for this package, available on the [AUR](https://aur.archlinux.org/packages/python-can-i-charge).

```bash
paru -S python-can-i-charge
```

## How to use

### CLI

The CLI can be used in the following ways:

```bash
# Using arguments
$ can-i-charge --station <SERIAL1> --station <SERIAL2> --station <SERIAL3>
# Using env variables
$ export STATIONS="<SERIAL1> <SERIAL2>"
$ can-i-charge
# The script can also be called using it's abbreviation
$ cic
```

You can pass as many stations as you want. At least one valid is needed however
to actually return some data. The serials for the charging stations can be found
on the charging station or on websites like [shellrecharge](https://ui-map.shellrecharge.com/).

### Prometheus Exporter

This utility can also be used as a Prometheus exporter:

```bash
# Using arguments
$ can-i-charge --station <SERIAL1> --station <SERIAL2> --station <SERIAL3> --exporter --port <default is 9041> --interval <default is 60 seconds>
# Using env variables
$ export STATIONS="<SERIAL1> <SERIAL2>"
$ export EXPORTER=1
# Optionally also overwrite default interval and port
$ export EXPORTER_PORT=9000
$ export EXPORTER_INTERVAL=120
$ can-i-charge
```

## See it in action

![GIF of an example session interacting with the cli](demo.gif)

## Container

### Build
```bash
$ docker build -t boosterl/can-i-charge:dev .
```

### Run
```bash
# Default
$ docker run --rm -e STATIONS='BE-TCB-P104146' boosterl/can-i-charge:dev

# Using exporter
$ docker run --rm -e STATIONS='BE-TCB-P104146' -e EXPORTER='1' -p 9041:9041 boosterl/can-i-charge:dev

# Using docker-compose
$ docker-compose up -d
```

### [dgoss](https://github.com/goss-org/goss/blob/master/extras/dgoss/README.md)
```bash
$ dgoss run boosterl/can-i-charge:dev
 INFO: Starting docker container
 INFO: Container ID: 97851a83
 INFO: Sleeping for 0.2
 INFO: Container health
 INFO: Running Tests
 User: can-i-charge: exists: matches expectation: true
 INFO: Deleting container
```

## Acknowledgments

This library uses the excellent [python-shellrecharge](https://github.com/cyberjunky/python-shellrecharge) package.
