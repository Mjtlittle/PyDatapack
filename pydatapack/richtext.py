from .internals import TextSegment

class RichTextFormat:
    class StringGenerator:
        def __init__(self,text):
            self.n = 0
            self.text = text

        @property
        def current(self):
            return self[self.n]

        @property
        def shadow_next(self):
            return self[self.n+1]

        def __getitem__(self,i):
            if i >= len(self.text) or i < 0:
                return False
            return self.text[i]

        def next(self,n = 1):
            self.n += n
            return self.current

    wildcards = ['&', '\u00A7']
    escapeable = wildcards + list('[]<>(){}@')
    selector_letters = list('aerps')

    colors={
        '0':'black',
        '1':'dark_blue',
        '2':'dark_green',
        '3':'dark_aqua',
        '4':'dark_red',
        '5':'dark_purple',
        '6':'gold',
        '7':'gray',
        '8':'dark_grey',
        '9':'blue',
        'a':'green',
        'b':'aqua',
        'c':'red',
        'd':'light_purple',
        'e':'yellow',
        'f':'white'}

    formatting={
        'k':'obfuscated',
        'l':'bold',
        'm':'strikethrough',
        'n':'underlined',
        'o':'italic'}

    def __init__(self,raw_text):
        self.raw_text = raw_text
        self.output = []

    def __str__(self):
        return self.render()

    def __repr__(self):
        return self.render()

    def __add__(self, value):
        return value + self.render()

    def render(self):
        self.output = []
        parts = self.parse(self.raw_text)
        return '['+','.join(map(str,parts))+']'


    def parse(self,text):
        parts = [TextSegment()]
        text = RichTextFormat.StringGenerator(text)

        while True:
            # escape chars
            if text.current in self.escapeable and self.escapeable.index(text.current) == text.shadow_next:
                parts[-1].append(text.next())
            
            # colors and formatting
            elif text.current in self.wildcards:
                # move to code
                text.next()
                
                # new segment if last has text
                if not parts[-1].empty:
                    parts.append(TextSegment())

                # colors
                if text.current in self.colors.keys():
                    parts[-1].color = self.colors[text.current]

                # formatting
                elif text.current in self.formatting.keys():
                    setattr(parts[-1],self.formatting[text.current],True)

                # reset
                elif text.current == 'r':
                    pass
                    
            # player selectors
            elif text.current == '@' and text.shadow_next in self.selector_letters:
                text.next()
                parts[-1].append('@'+text.current)
                parts[-1].selector = True

                if text.shadow_next == '[':
                    parts[-1].append('[')
                    text.next()
                    while text.shadow_next != ']':
                        parts[-1].append(text.next())
                    #parts[-1].append(']')

                parts.append(TextSegment())

            # other text properties
            elif text.current == '[':

                # new segment
                parts.append(TextSegment())

                # add text to buffer
                buffer = []
                text.next()
                while text.current != ']' and text.current != None:
                    buffer.append(text.current)
                    text.next()
                parsed = self.parse(''.join(buffer))
                parts_in_brackets = len(parsed)
                parts += parsed

                # add brakets back if not valid afterwards
                if text.shadow_next not in list('<[({'):
                    parts[-1].insert(0,'[')
                    parts[-1].append(']')

                #! bodge way
                for _ in range(2):

                    # hover text
                    if text.shadow_next == '(':
                        buffer = []
                        text.next(2)
                        while text.current != ')' and text.current != None:
                            buffer.append(text.current)
                            text.next()

                        # all parts within brackets
                        for i in range(parts_in_brackets):
                            parts[-(i+1)].hover_text = ''.join(buffer)
                    
                    # click command
                    elif text.shadow_next == '{':
                        buffer = []
                        text.next(2)
                        while text.current != '}' and text.current != None:
                            buffer.append(text.current)
                            text.next()

                        # all parts within brackets
                        for i in range(parts_in_brackets):
                            parts[-(i+1)].click_command = ''.join(buffer)

                # reset the end
                parts.append(TextSegment())

            # any other character
            else:
                parts[-1].append(text.current)
            
            # last next and halt if end 
            text.next()
            if text.current == False:
                break
        
        return parts
        
def toRichText(richtext):
    return str(RichTextFormat(richtext).render())

def tellRichText(richtext,target='@a'):
    return f'tellraw {target} {toRichText(richtext)}'