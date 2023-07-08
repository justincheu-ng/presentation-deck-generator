from .unsplash import Unsplash

class Slide:
    def __init__(self, md, img = None):
        self.md = md
        self.img = ''
        for line in md.splitlines():
            if line.startswith('# '):
                self.title = line.replace('# ', '')

    def add_image(self, query):
        img = 'img/' +  str(hash(self.md)) + '.jpg'
        Unsplash.save_image(query, './marp-cli/'+img)
        self.img = img

    def get_content_line_number(self):
        lines = self.md.splitlines()
        count = 0
        for line in lines:
            if line != "" and  not line.startswith('#'):
                count += 1

        return count

    def to_md(self):
        md = ""
        if self.img:
            md = f"![bg left:33% brightness:0.9]({self.img})\n\n"
        md += self.md

        return md