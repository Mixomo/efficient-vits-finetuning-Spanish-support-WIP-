import argparse
import re
import text
from utils import load_filepaths_and_text
from phonemizer import phonemize
from phonemizer.backend import EspeakBackend

def clean_text(text):
    text = re.sub(r"[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ'\-.,?!]+", ' ', text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def text_to_phonemes(text, backend='espeak'):
    cleaned_text = clean_text(text)
    backend_obj = EspeakBackend() if backend == 'espeak' else FestivalBackend()
    phonemes = phonemize(cleaned_text, language='es', backend=backend_obj)
    return phonemes

def spanish_cleaners(text):
    return text_to_phonemes(text, backend='espeak')

def _clean_text(text, text_cleaners):
    if "spanish_cleaners" in text_cleaners:
        cleaned_text = spanish_cleaners(text)
    else:
        cleaned_text = text._clean_text(text, text_cleaners)
    return cleaned_text

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--out_extension", default="cleaned")
    parser.add_argument("--text_index", default=1, type=int)
    parser.add_argument("--filelists", nargs="+", default=["filelists/ljs_audio_text_val_filelist.txt", "filelists/ljs_audio_text_test_filelist.txt"])
    parser.add_argument("--text_cleaners", nargs="+", default=["english_cleaners2", "spanish_cleaners"])

    args = parser.parse_args()

    for filelist in args.filelists:
        print("START:", filelist)
        filepaths_and_text = load_filepaths_and_text(filelist)
        for i in range(len(filepaths_and_text)):
            original_text = filepaths_and_text[i][args.text_index]
            cleaned_text = _clean_text(original_text, args.text_cleaners)
            filepaths_and_text[i][args.text_index] = cleaned_text

        new_filelist = filelist + "." + args.out_extension
        with open(new_filelist, "w", encoding="utf-8") as f:
            f.writelines(["|".join(x) + "\n" for x in filepaths_and_text])