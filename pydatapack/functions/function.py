from ..internals import NamespaceAdressable
import re

class Function(NamespaceAdressable):
    def __init__(self, target):
        super().__init__(target)
        self.lines = []

    def call_command(self):
        return f'function {self.target}'
    
    def __call__(self):
        return self.call_command()

    @property
    def entity_tags_used(self):
        tags = []
        for line in self.lines:
            match = re.search(r'tag (?:\w+)|(?:@\w+\S*) add (.*)',line)
            if match != None:
                tags.append(match.groups()[0])
        return tags

    @property
    def created_objectives(self):
        objectives = []
        lookup = 'scoreboard objectives add '
        for line in self.lines:
            i = line.find(lookup)
            if i != -1:
                objectives.append(line[i+len(lookup):].split(' ')[0])
        return objectives
    
    def append(self, command):
        return self.add_command(command)

    def __iadd__(self, command):
        self.add_command(command)

    def add_command(self, command):
        if '\n' in command:
            for sub_command in command.split('\n'):
                if sub_command.strip() != '':
                    self.lines.append(sub_command.strip())
        else:
            self.lines.append(command.strip())
        return self

    def raw_text(self):
        return '\n'.join(self.lines)
