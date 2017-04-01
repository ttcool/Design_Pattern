import xml.etree.ElementTree as etree
from io import open
import json


class JSONConnector:
    def __init__(self, filepath):
        self.data = dict()
        with open(filepath, mode='r', encoding='utf8') as f:
            self.data = json.load(f)

    @property
    def parsed_data(self):
        return self.data

class XMLConnector:
    def __init__(self, filepath):
        self.tree = etree.parse(filepath)

    @property
    def parsed_data(self):
        return self.tree

def connection_factory(filepath):
    if filepath.endswith('json'):
        connector = JSONConnector
    elif filepath.endswith('xml'):
        connector = XMLConnector
    else:
        raise ValueError('Cannot connect to {}'.format(filepath))
    return connector(filepath)


def connect_to(filepath):
    factory = None
    try:
        factory = connection_factory(filepath)
    except ValueError as ve:
        print(ve)
    return factory


def main():
    sqlite_factory = connect_to('data/person.sq3')

    xml_factory = connect_to('person.xml')
    xml_data = xml_factory.parsed_data
    persons = xml_data.getroot()
    print('found: {} persons'.format(len(persons)))
    for person in persons:
        print('first name: {}'.format(person.find('firstName').text))
        print('last name: {}'.format(person.find('lastName').text))
        print [(p.find('number').text) for p in person.find('phoneNumbers').findall('phoneNumber')]

    json_factory = connect_to('donut.json')
    json_data = json_factory.parsed_data
    print('found: {} donuts'.format(len(json_data)))


if __name__ == '__main__':
    main()
