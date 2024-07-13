import argparse
import os
from openai import OpenAI
from deep_translator import GoogleTranslator
import re
from tqdm import tqdm

client = OpenAI(api_key="WRITE_YOUR_KEY_HERE")


def translate_text(text, src_lang, target_lang):
    try:
        translated = GoogleTranslator(source=src_lang, target=target_lang).translate(text=text)
        return translated
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        return text

def refine_translation_with_chatgpt(text, chat_history):
    try:
        prompt=f"Refine the following translation based on the previous context: {text}\n\nChat History: {chat_history}"
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            # prompt=text,
            messages=[
                {"role": "user", "content": text}
            ],
            temperature=2,
            max_tokens=500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred during connection: {e}")
        return text

def get_time_in_seconds(time_str):
    h, m, s = map(float, time_str.split(':'))
    return h * 3600 + m * 60 + s

def process_srt(file_path, source_lang, target_lang, refine=False, use_chatgpt_only=False, reset_interval=600, output_file=None):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    translated_lines = []
    chat_history = ""
    last_timestamp = 0

    if not output_file:
        output_file = f"{os.path.splitext(file_path)[0]}_translated.srt"

    for line in tqdm(lines, desc="Translating"):
        if line.strip().isdigit() or '-->' in line:
            translated_lines.append(line)
            if '-->' in line:
                start_time = re.search(r'(\d{2}:\d{2}:\d{2},\d{3})', line).group(1)
                current_timestamp = get_time_in_seconds(start_time.replace(',', '.'))
                if current_timestamp - last_timestamp > reset_interval:
                    chat_history = ""
                last_timestamp = current_timestamp
        else:
            if use_chatgpt_only:
                chat_history += f"{line}\n"
                translated_text = refine_translation_with_chatgpt(line, chat_history)
            else:
                translated_text = translate_text(line, source_lang, target_lang)
                if refine:
                    chat_history += f"{translated_text}\n"
                    translated_text = refine_translation_with_chatgpt(translated_text, chat_history)
            translated_lines.append(translated_text + '\n')

    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(translated_lines)

    return output_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Translate SRT file to a specified language.")
    parser.add_argument('srt_file', help="Path to the SRT file")
    parser.add_argument('--source_lang', default='ru', help="Source language for translation")
    parser.add_argument('--target_lang', default='en', help="Target language for translation")
    parser.add_argument('--refine', action='store_true', help="Refine translation using ChatGPT")
    parser.add_argument('--use_chatgpt_only', action='store_true', help="Translate and refine entirely using ChatGPT")
    parser.add_argument('--reset_interval', type=int, default=600, help="Interval (in seconds) after which chat history is reset")
    parser.add_argument('--output_file', help="Output file name for the translated SRT")

    args = parser.parse_args()

    output_file = process_srt(args.srt_file, args.source_lang, args.target_lang, args.refine, args.use_chatgpt_only, args.reset_interval, args.output_file)

    print(f"Translation completed. Output file: {output_file}")
