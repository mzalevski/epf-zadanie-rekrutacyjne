# get-monitor-data-util

specs: <https://epf.org.pl/pl/wp-content/uploads/sites/2/2019/12/zadanie-programistyczne-1.pdf>

I've used the `requests` library, because there is no built-in http library in python. Hence in order to run the script, one has to install the before-mentioned library. Best practice is to use pipenv to manage dependencies, but I'm also providing instructions for the good' old pip install way for convenience of the casual user. Also, even tough it was not requested, I've added the possibility to save the output data to a file.

***

## pipenv

1. run `pipenv install`

2. run `pipenv run python get_monitor_data.py {year} {optional: -s / --save}`

***

## without pipenv

1. run `pip install requests`

2. run `python get_monitor_data.py {year} {optional: -s / --save}`

***

## additional info

- if Linux or MacOS is used, the user should use `python3` instead of `python` in all the commands

- optionally add the script's location to the PATH in order to make the script globally invokable
