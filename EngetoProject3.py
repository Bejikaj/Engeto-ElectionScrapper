"""

projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Jan Benáček

email: Jan.Benacek@seznam.cz

discord: Bejikaj#2628

"""

import requests
from bs4 import BeautifulSoup
import sys
import csv

def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.content, "html.parser")

def id_munic(soup):
    id_municip = []
    ids = soup.find_all("td", "cislo")
    for i in ids:
        id_municip.append(i.text)
    return id_municip

def name_munic(soup):
    name_municip = []
    names = soup.find_all("td", "overflow_name")
    for i in names:
        name_municip.append(i.text)
    return name_municip

def get_links(soup):
    soup_aux = []
    links_search = soup.find_all("td", "cislo", "href")
    for i in links_search:
        i = i.a["href"]
        link = f"https://volby.cz/pls/ps2017nss/{i}"
        response_link = requests.get(link)
        response_link = response_link.content
        soup_link = BeautifulSoup(response_link, "html.parser")
        soup_aux.append(soup_link)
    return soup_aux

def voters(soup_list):
    no_of_voters = []
    for i in soup_list:
        voters = i.find_all("td", class_="cislo")[3]
        voters = voters.text
        no_of_voters.append(voters.replace("\xa0", " "))
    return no_of_voters

def envelopes(soup_list):
    no_of_envelopes = []
    for i in soup_list:
        envelopes = i.find_all("td", class_="cislo")[4]
        envelopes = envelopes.text
        no_of_envelopes.append(envelopes.replace("\xa0", " "))
    return no_of_envelopes

def valid_votes(soup_list):
    no_of_valid_votes = []
    for i in soup_list:
        valid_votes = i.find_all("td", class_="cislo")[7]
        valid_votes = valid_votes.text
        no_of_valid_votes.append(valid_votes.replace("\xa0", " "))
    return no_of_valid_votes

def get_parties_list(soup_list):
    parties_list = []
    for soup in soup_list:
        tables = soup.find_all("td", class_="overflow_name")
        for td in tables:
            party_name = td.text.strip()
            if party_name not in parties_list:  # Ensure uniqueness before adding
                parties_list.append(party_name)
    return parties_list

def votes_munip(soup_list):
    votes_in_munip = []
    for i in soup_list:
        votes = i.find_all("td", class_="cislo")[10::3]
        temporary = []
        for v in votes:
            temporary.append(v.text)
        votes_in_munip.append(temporary)
    return votes_in_munip

def csv_structure(id_municip, name_municip, no_of_voters, no_of_envelopes, no_of_valid_votes, votes_in_munip):
    rows = []
    for i in range(len(id_municip)):
        row = [id_municip[i], name_municip[i], no_of_voters[i], no_of_envelopes[i], no_of_valid_votes[i]] + votes_in_munip[i]
        rows.append(row)
    return rows

def csv_creation(file, header, content):
    with open(file, mode="w", newline='') as f:
        f_writer = csv.writer(f)
        f_writer.writerow(header)
        f_writer.writerows(content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Please provide the URL of the website and the output file name.")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2]

    try:
        soup = get_soup(url)
        id_municip = id_munic(soup)
        name_municip = name_munic(soup)
        soup_list = get_links(soup)
        no_of_voters = voters(soup_list)
        no_of_envelopes = envelopes(soup_list)
        no_of_valid_votes = valid_votes(soup_list)
        parties_set = get_parties_list(soup_list)
        votes_in_munip = votes_munip(soup_list)
        header = ["Code", "Location", "Registered", "Envelopes", "Valid"] + parties_set
        content = csv_structure(id_municip, name_municip, no_of_voters, no_of_envelopes, no_of_valid_votes, votes_in_munip)
        csv_creation(output_file, header, content)
        print("CSV file has been created.")
    except Exception as e:
        print("An error occurred:", e)
