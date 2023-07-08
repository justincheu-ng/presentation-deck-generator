from slides import GenAI, Deck, Unsplash, Loading
import os

os.system('clear')
print('Thanks for you Presentation Deck Generator. Please input a topic to start:')
print()
topic = input('Topic: ')
gen_ai = GenAI()
print()

# Subtitle

subtitles = gen_ai.generate_subtitles(topic, 5)
os.system('clear')
print('Pick one of the suggested subtitles, or create your own.\n')
for i in range(len(subtitles)):
    print('{}. {}'.format(i+1, subtitles[i]))
print('{}. Create your own subtitle\n'.format(len(subtitles)+1))
valid_input = False
while (not valid_input):
    the_input = input('Input (1-{}): '.format(len(subtitles)+1))
    if the_input in [str(i+1) for i in range(len(subtitles))]:
        valid_input = True
        subtitle = subtitles[int(the_input)-1]
    if the_input == str(len(subtitles) + 1):
        valid_input = True
        subtitle = input('Subtitle: ')
print()


# Headings
generated_headings = gen_ai.generate_headings(topic, subtitle)
os.system('clear')
print('Use the suggested table of content, or create your own:\n')
print('1. Use the suggested table of content:')
for i in range(len(generated_headings)):
    print('  - {}'.format(generated_headings[i]))
print('2. Create your own table of content\n')

valid_input = False
while (not valid_input):
    the_input = input('Input (1-2): ')
    if the_input == '1':
        valid_input = True
        headings = generated_headings
    if the_input == '2':
        valid_input = True
        headings = []
        print('Input your heading for each slide. Input nothing to finish.')
        the_input = 'not_empty'
        while the_input != '':
            the_input = input('{}. '.format(len(headings)+1))
            headings.append(the_input)
print()

# Content
content = gen_ai.generate_content(topic, subtitle, headings)
# content = gen_ai.bold_keywords(content)
deck = Deck(topic, subtitle, headings, content)

# Formatting
loading = Loading('Formatting')

for slide in deck.slides[1:]:
    if slide.get_content_line_number() > 6:
        slide.md = gen_ai.modify_slide(slide.md, 'simplify the content')
    slide.md = gen_ai.bold_keywords(slide.md)
loading.complete()

# Cover
keyword = gen_ai.title_keyword(topic, subtitle)
deck.slides[0].add_image(keyword)



md = deck.to_marp()

with open('./marp-cli/output.md', 'w') as file:
    file.write(md)

deck.export()

while True:
    # Choose a page
    print("Choose a page to modify, or exit to finish:\n")

    for i in range(len(deck.slides)):
        print(f'{i+1}: {deck.slides[i].title}')
    print(f'{len(deck.slides)+1}: Exit')
    print()
    valid_input = False
    number = -1
    while not valid_input:
        the_input = input(f'Input (1-{len(deck.slides) + 1}): ')
        if the_input == str(len(deck.slides) + 1):
            exit()
        if the_input in [str(i+1) for i in range(len(deck.slides))]:
            slide_number = int(the_input) - 1
            valid_input = True
    os.system('clear')
    
    # Choose an action
    print("Choose an action to perform, or exit to finish:\n")
    print('1. Modify the content')
    print('2. Add/Change image')
    print('3. Exit')
    print()
    valid_input = False
    while not valid_input:
        the_input = input('Input (1-3): ')
        if the_input in ['1', '2', '3']:
            valid_input = True
            action = int(the_input)
    
    # Exit
    if action == 3:
        exit()

    # Modify the content
    if action == 1:
        os.system('clear')
        print('Please provide an instruction to modify the content\n')
        instruction = input('Input: ')
        deck.slides[slide_number].md = gen_ai.modify_slide(deck.slides[slide_number].md, instruction)
    
    if action == 2:
        os.system('clear')
        keyword = gen_ai.slide_keyword(deck.slides[slide_number].md)
        print('Choose the generated keyword for the image, or input your own.')
        print(f'1. {keyword}')
        print('2. Input your own keyword\n')
        valid_input = False
        while not valid_input:
            the_input = input("Input (1-2): ")
            valid_input = the_input in ['1', '2']
        if the_input == '2':
            keyword = input("Keyword: ")
        deck.slides[slide_number].add_image(keyword)

    deck.export()
