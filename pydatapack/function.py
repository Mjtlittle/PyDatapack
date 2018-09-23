import re

class Function:
    def __init__(self,target,*tags):
        self.target = target
        self.tags = tags
        self.lines = []

    @property
    def name(self):
        # remove namespace if provided
        target = self.target
        if ':' in target:
            target = target.split(':')[1]

        if '/' in target:
            return target.split('/')[-1]
        else:
            return target
    
    # getting the reference to the function
    @property
    def call(self):
        return f'function {self.target}'
    
    def __call__(self):
        return self.call

    
    @property
    def namespace(self):
        if ':' in self.target:
            return self.target.split(':')[0]
        else:
            return None

    @property
    def entity_tags_used(self):
        tags = []
        for line in self.lines:
            match = re.search(r'tag (?:\w+)|(?:@\w+\S*) add (.*)',line)
            if match != None:
                tags.append(match.groups()[0])
        return tags

    @namespace.setter
    def namespace(self,value):
        if ':' in self.target:
            self.target = value+':'+self.target.split(':')[1]
        else:
            self.target = value+':'+self.target
        return True

    @property
    def parentStructure(self):
        # remove namespace if provided
        target = self.target
        if ':' in target:
            target = target.split(':')[1]

        if '/' in target:
            return '/'.join(target.split('/')[:-1])
        else:
            return None

    @property
    def created_objectives(self):
        objectives = []
        lookup = 'scoreboard objectives add '
        for line in self.lines:
            i = line.find(lookup)
            if i != -1:
                objectives.append(line[i+len(lookup):].split(' ')[0])
        return objectives
    
    def append(self,command):
        return self.addCommand(command)
    
    def addCommand(self,command):
        if '\n' in command:
            for sub_command in command.split('\n'):
                if sub_command.strip() != '':
                    self.lines.append(sub_command.strip())
        else:
            self.lines.append(command.strip())
        return None

    def __str__(self):
        return '\n'.join(self.lines)
