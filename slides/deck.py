import datetime
import os
import shutil
import subprocess
import textwrap
from .slide import Slide



class Deck:
    def __init__(self, topic, subtitle, headings, content):
        self.topic = topic
        self.subtitle = subtitle
        self.headings = headings
        self.slides = [
            Slide(textwrap.dedent(f"""\
                <!-- _class: titlepage -->
                <!-- paginate: false -->
                                        
                # {self.topic}

                {self.subtitle}
                """))
        ]

        lines = content.splitlines(True)
        section = lines[0]
        for line in lines[1:]: 
            if line.startswith('# '):
                self.slides.append(Slide(section))
                section = ''
            section += line
         

    def to_marp(self):
        md = textwrap.dedent(f"""\
            ---
            title: {self.topic}: {self.subtitle}
            marp: true
            paginate: true
            theme: theme
            """)
        
        for slide in self.slides:
            md += '\n\n---\n\n'
            md += slide.to_md()

        return md
    
    def export(self):
        os.system('clear')
        with open('./marp-cli/output.md', 'w') as file:
            file.write(self.to_marp())

        subprocess.run(
            ['docker', 'compose', '-f', './docker-compose.yml', 'run', 'marp-cli']
        )

        shutil.copyfile('./marp-cli/output.pdf', './output.pdf')
        os.system('clear')