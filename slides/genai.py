import vertexai
from vertexai.language_models import TextGenerationModel
import textwrap
from .loading import Loading

class GenAI:
    def __init__(self):
        vertexai.init(
            project='gen-hk-olympic-team',
            location='us-central1'
        )

        self.parameters = {
            'temperature': 0.2,
            'max_output_tokens': 1024,
            'top_p': 0.8,
            'top_k': 40
        }

        self.model = TextGenerationModel.from_pretrained('text-bison@001')
    

    def get_response(self, prompt):
        model = TextGenerationModel.from_pretrained('text-bison@001')
        parameters = {
            'temperature': 0.2,
            'max_output_tokens': 1024,
            'top_p': 0.8,
            'top_k': 40
        }
        response = model.predict(prompt, **parameters)
        return response.text

    def generate_subtitles(self, topic, quantity):
        
        def extract_subtitle(full_title, topic):
            subtitle = full_title
            if subtitle.startswith(topic):
                subtitle = subtitle.replace(topic, '')
            subtitle = subtitle.strip()

            if subtitle.startswith(':'):
                subtitle = subtitle.replace(':', '')
            subtitle = subtitle.strip()
            return subtitle

        loading = Loading('Generating subtitles')

        prompt = 'Generate the sub-title for the title \"{}\" with no formatting. {}: '.format(topic, topic)

        response = self.get_response(prompt)
        
        subtitle = extract_subtitle(response, topic)
        subtitles = [subtitle]

        if quantity > 1:
            prompt = textwrap.dedent("""\
                Generate {} sub-titles for the title \"{}\":
                - {}: {}
                - {}: """.format(quantity, topic, topic, subtitle, topic))
            response = self.get_response(prompt)
            lines = response.split('\n')
            subtitles.append(lines[0].replace('{}: '.format(topic), ''))
            subtitles = subtitles + [extract_subtitle(line[2:], topic) for line in lines[1:]]
        
        loading.complete()
        return subtitles
        
    def generate_headings(self, topic, subtitle):
        loading = Loading('Generating headings')

        prompt = textwrap.dedent("""\
            Complete this list of titles of each slides for a presentation deck titled \"{}: {}\":
            - Table of Contents
            - Introduction""".format(topic, subtitle))

        response = self.model.predict(
            prompt,
            **self.parameters
        )

       
        headings = response.text.split('\n')
        introduction = 'Introduction ' + headings[0]
        headings = [introduction] + [s[2:] for s in headings[1:]]

        loading.complete()

        return headings

    def generate_content(self, topic, subtitle, headings):
        loading = Loading('Generating content')
        prompt = 'For a presentation deck titled \"{}: {}\" with the table of content of\n'.format(topic, subtitle)
        for heading in headings:
            prompt += heading + '\n'
        prompt += textwrap.dedent("""\
            Prepare the content for the presentation in the Markdown format.\n
            # {}

            *   """.format(headings[0]))
        content = self.get_response(prompt) 
        content = textwrap.dedent("""\
            # {}

            *   """.format(headings[0])) + content
        
        loading.complete()

        return content

    def bold_keywords(self, content):
        prompt = textwrap.dedent(f"""\
            {content}
            

            Without changing the content above, bold important keywords, and complete the markdown:  

            {content.splitlines()[0]}

            """)
        
        response = self.get_response(prompt)
       
        content = content.splitlines()[0] + '\n\n' + response

        return content

    def title_keyword(self, topic, subtitle):
        loading = Loading('Generating keyword for cover image')

        prompt = 'Provide only keyword of a cover image for the title \"{}: {}\". Do not provide explaination. Keyword: '.format(topic, subtitle)

        response = self.get_response(prompt)    
        loading.complete()

        return response
    
    def slide_keyword(self, content):
        loading = Loading('Generating keyword for content')

        prompt = textwrap.dedent(f"""\
            {content}
            
            Based on the content above, provide only keyword of an image. Do not provide explaination. Keyword: """)

        response = self.get_response(prompt)    
        loading.complete()

        return response
           
    def modify_slide(self, md, instruction):
        prompt = textwrap.dedent("""\
            {}

            Based on the above markdown, {}, and complete the markdown with the same heading

            {}""".format(md, instruction, md.splitlines()[0]))
        
        new_content = self.get_response(prompt)

        new_md = md.splitlines()[0] + '\n\n' + new_content
        return new_md