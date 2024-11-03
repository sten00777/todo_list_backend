import os
import json


class Entry:
    def __init__(self, title: str, parent=None, entries=None):
        if entries is None:
            entries = []
        self.title = title
        self.parent = parent
        self.entries = entries

    def __str__(self):
        return self.title

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def print_entries(self, indent=0):
        self.print_with_indent(str(self), indent)
        for entry in self.entries:
            entry.print_entries(indent + 1)

    def print_with_indent(self, value: str, indent=0):
        print('\t' * indent + value)

    def json(self):
        return {
            'title': self.title,
            'entries': [entry.json() for entry in self.entries]
        }

    @classmethod
    def from_json(cls, value):
        res = cls(value['title'])
        for entry in value.get('entries', []):
            res.add_entry(cls.from_json(entry))
        return res

    def save(self, path):
        with open(os.path.join(path, f'{self.title}.json'), 'w') as file:
            file.write(json.dumps(self.json()))

    @classmethod
    def load(cls, filename):
        with open(filename, 'r') as file:
            res = json.load(file)
            return cls.from_json(res)


class EntryManager:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.entries = []

    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)

    def load(self):
        for file in os.listdir(self.data_path):
            if file.endswith('.json'):
                entry = Entry.load(os.path.join(self.data_path, file))
                self.entries.append(entry)

    def add_entry(self, title: str):
        new_entry = Entry(title)
        self.entries.append(new_entry)