#!/usr/bin/python

import requests, re, json, sys

HOST_URL = "https://ems.ms.gov.pl"
PATH = "/msig/przegladaniemonitorow.latawydaniaform"


def parse_year_data(raw_year_data):

    # get the body of the page
    body_start_idx = raw_year_data.text.index('<div class="body">')
    body_end_idx = raw_year_data.text.index('<div id="footer">')
    body = raw_year_data.text[body_start_idx:body_end_idx]

    # create a list of p tags
    p_tags = [p[0] for p in re.finditer("<p>.*", body)]

    # get the titles & urls together
    titles_and_urls = [p for p in p_tags if f"{p[3]}{p[4]}" == "<a"]

    # get the titles
    titles = [
        re.findall("\\d{1,3} / \\d{4}", title_and_url)[0]
        for title_and_url in titles_and_urls
    ]

    # get the urls
    urls = [
        HOST_URL + re.findall("/msig.*\$N", title_and_url)[0]
        for title_and_url in titles_and_urls
    ]

    # get the dates
    dates = [p[3:-4] for p in p_tags if p[3] in ["0", "1", "2", "3"]]

    # get the sizes
    sizes = [
        str(int(float(p[4:-8].replace(",", ".")) * 1000000))
        for p in p_tags if p[3] == "["
    ]

    # zip the above data to a list of lists
    parsed_year_data_zip = list(zip(titles, urls, dates, sizes))

    # transform the zipped data to a list of dictionaries
    parsed_year_data_dicts = [
        {"title": title, "url": url, "date": date, "size": size}
        for title, url, date, size in parsed_year_data_zip
    ]

    # return the json data
    return parsed_year_data_dicts


def get_MSiG_data_per_year(year):

    # prepare data to be passed to the MSiG form
    form_data = {
        "t:formdata": "H4sIAAAAAAAAAJXOMU4CQRSA4QeJ1XYm3kAN1WwDDVY"
                    + "0VkhINsb67exjGDM7b/LmwQKH4QTGS1DYeQcPYGtFgY"
                    + "QT0P7N93/8wk03gMc2e1fOZUcuYIPR0wtHryzcjQMqd"
                    + "ttzxCwwYnEGE9olGcVEWWU7MpaFgq9NjZnMpP6PaPXZ"
                    + "U2juK9JVeng9FD93X8c+9KZQWI4qHGbYksLt9B3XWAa"
                    + "MrqxUfHRPm6RQnNm3C3vV4OTawbmwpZyrVd36nD3Hw2"
                    + "czXPztv/sAm3QCliqXmyEBAAA=",

        "lataWydania": year,
    }

    # get raw data
    raw_year_data = requests.post(HOST_URL + PATH, form_data)

    # parse the data
    parsed_year_data = parse_year_data(raw_year_data)

    # dump the list of dictionaries to JSON
    parsed_json_year_data = json.dumps(parsed_year_data)

    # return parsed JSON
    return parsed_json_year_data


def main(args):

    # check if there is not too many args
    if len(args) > 3:
        print("Zbyt wiele argumentów!")

    # check if there is not too few args
    elif len(args) < 2:
        print("Podaj rok, który Cię interesuje!")

    # check if the passed first arg is a valid integer
    elif not re.match("\d\d\d\d", args[1]):
        print("Wybierz rok od 1996 do 2019!")

    # check if the passed year is in a valid range
    elif int(args[1]) < 1996 or int(args[1]) > 2019:
        print("Wybierz rok od 1996 do 2019!")

    else: # the first arg is valid therefore we procede further

        # if the user passed the second argument
        if len(args) == 3:

            # check wheter the second arg is valid
            if re.match("\d\d\d\d", args[2]):
                print("Nie możesz podać dwóch roczników!")

            elif args[2] not in ["--save", "-s"]:
                print("Dodaj flagę '--save' albo '-s', jeżeli"
                    + " jeżeli chcesz zapisać wynik do pliku.")

            else: # user passed the -s / --save flag

                with open(f"{args[1]}-MSiG.json", "w") as file:
                    file.write(get_MSiG_data_per_year(year=args[1]))

                print(f"Zapisano w {args[1]}-MSiG.json")


        else: # user did not pass the 2nd arg & the 1st arg is valid
            print(get_MSiG_data_per_year(year=args[1]))


if __name__== "__main__":
    main(args=sys.argv)