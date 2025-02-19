# Can I charge?

It's a question you might have asked yourself before if you have a BEV/PHEV.
This utility allows you to check if your favorite charging stations are available
for your car to charge, right from the warmth of your terminal! No need to go
outside and physically check if the charging station is available, and possibly
return disappointed because it was occupied.

## How to install

```bash
pip install can-i-charge
```

## How to use

The CLI can be used in the following ways:

```bash
# Using arguments
can-i-charge --station <SERIAL1> --station <SERIAL2> --station <SERIAL3>
# Using env variables
export STATIONS="<SERIAL1> <SERIAL2>"
can-i-charge
```

You can pass as many stations as you want. At least one valid is needed however
to actually return some data. The serials for the charging stations can be found
on the charging station or on websites like [shellrecharge](https://www.shell.co.uk/electric-vehicle-charging/find-an-ev-charge-point.html).

## See it in action

![GIF of an example session interacting with the cli](demo.gif)

## Acknowledgments

This library uses the excellent [python-shellrecharge](https://github.com/cyberjunky/python-shellrecharge) package.
