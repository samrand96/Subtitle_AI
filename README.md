# SRT Translator

This Python script translates SRT subtitle files into a specified target language (default is English). It can also optionally refine the translation using OpenAI's GPT-3 or translate and refine entirely using GPT-3. Additionally, the script can reset the chat history after a specified time interval to save credits.

## Installation

First, install the required libraries:

```sh
pip install deep-translator openai python-dotenv tqdm
```

## Usage

1. **Translate without refinement**:
    ```sh
    python translate_srt.py path/to/file.srt
    ```

2. **Translate with refinement**:
    ```sh
    python translate_srt.py path/to/file.srt --refine
    ```

3. **Translate entirely using ChatGPT**:
    ```sh
    python translate_srt.py path/to/file.srt --use_chatgpt_only
    ```

4. **Translate to a different target language**:
    ```sh
    python translate_srt.py path/to/file.srt --target_lang fr
    ```

5. **Translate to a different target language with refinement**:
    ```sh
    python translate_srt.py path/to/file.srt --target_lang fr --refine
    ```

6. **Translate to a different target language entirely using ChatGPT**:
    ```sh
    python translate_srt.py path/to/file.srt --target_lang fr --use_chatgpt_only
    ```

7. **Translate with a specified chat history reset interval**:
    ```sh
    python translate_srt.py path/to/file.srt --reset_interval 300
    ```

8. **Specify an output file name**:
    ```sh
    python translate_srt.py path/to/file.srt --output_file path/to/output.srt
    ```

## Command-line Arguments

- `srt_file`: Path to the SRT file.
- `--source_lang`: Source language for translation (default is 'ru').
- `--target_lang`: Target language for translation (default is 'en').
- `--refine`: Refine translation using ChatGPT.
- `--use_chatgpt_only`: Translate and refine entirely using ChatGPT.
- `--reset_interval`: Interval (in seconds) after which chat history is reset (default is 600 seconds).
- `--output_file`: Output file name for the translated SRT. If not provided, the output file will be named with `_translated.srt` appended to the original filename.

## Open AI Integration

Don't forget to put your key for using OPENAI API

```
client = OpenAI(api_key="PUT_YOUR_KEY_HERE")
```
```

### Explanation

1. **Functions**:
    - `translate_text(text, src_lang, target_lang)`: Translates text from the source language to the target language using `GoogleTranslator`.
    - `refine_translation_with_chatgpt(text, chat_history)`: Refines the translation using ChatGPT, incorporating previous chat history for context.
    - `get_time_in_seconds(time_str)`: Converts a time string in the format `HH:MM:SS,mmm` to seconds.
    - `process_srt(file_path, source_lang, target_lang, refine=False, use_chatgpt_only=False, reset_interval=600, output_file=None)`: Processes the SRT file, translates its content, and optionally refines the translation. If `use_chatgpt_only` is True, it translates and refines entirely using ChatGPT while maintaining context. The `reset_interval` parameter specifies the time interval (in seconds) after which the chat history is reset to save credits. The `output_file` parameter specifies the name of the output file. If not provided, it will use the original filename with `_translated.srt` appended.

2. **Main Program**:
    - Parses command-line arguments to get the SRT file path, source language, target language, whether to refine the translation, whether to use ChatGPT exclusively for translation, the chat history reset interval, and the output file name.
    - Calls `process_srt` to perform the translation and refinement.
    - Outputs the path of the translated file.
