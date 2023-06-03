from gtts import gTTS


def create_voice(text, number, theme):
    audio_wrong = gTTS(text=text, lang='en', slow=False)
    audio_wrong.save(f"static/scripts/{theme}/{number}.ogg")


if __name__ == '__main__':
    theme = input('theme: ')
    for i in range(6):
        create_voice(input('text: '), i + 1, theme)
