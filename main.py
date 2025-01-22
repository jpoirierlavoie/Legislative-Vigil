import os
import requests
from flask import Flask, render_template
from lxml import etree

app = Flask(__name__)

@app.route("/members")
def members():
    url = "https://www.ourcommons.ca/Members/en/search/XML"
    response = requests.get(url)
    root = etree.fromstring(response.content)

    # Parse the XML data and extract relevant information
    # about the members of parliament.
    members = []
    for member_element in root.xpath("//ArrayOfMemberOfParliament/MemberOfParliament"):
        first_name_element = member_element.xpath("PersonOfficialFirstName/text()")
        first_name = first_name_element[0] if first_name_element else ""
        last_name_element = member_element.xpath("PersonOfficialLastName/text()")
        last_name = last_name_element[0] if last_name_element else ""
        party_element = member_element.xpath("CaucusShortName/text()")
        party = party_element[0] if party_element else ""
        district_element = member_element.xpath("ConstituencyName/text()")
        district = district_element[0] if district_element else ""
        province_element = member_element.xpath("ConstituencyProvinceTerritoryName/text()")
        province = province_element[0] if province_element else ""

        members.append({"first_name": first_name, "last_name": last_name, "party": party, "district": district, "province": province})
    return render_template("members.html", members=members)

@app.route("/bills")
def bills():
    url = "https://www.parl.ca/legisinfo/en/bills/xml"
    response = requests.get(url)
    root = etree.fromstring(response.content)

    bills = []
    for bill_element in root.xpath("//Bills/Bill"):
        number_element = bill_element.xpath("BillNumberFormatted/text()")
        number = number_element[0] if number_element else ""

        bills.append({"number": number, })
    return render_template("bills.html", bills=bills)

def main():
    app.run(port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    main()