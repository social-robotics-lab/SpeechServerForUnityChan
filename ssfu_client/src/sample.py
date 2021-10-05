import argparse
import time
import jtalk
import serverio as io
from pydub import AudioSegment


def say_text(ip:str, text:str, port=13000, speed=1.0, emotion='normal', voice_name='mei') -> float:
    """
    OpenJTalkを使って発話する。
    """
    output_file = '{}.wav'.format(text[:10])
    jtalk.make_wav(text, speed, emotion, output_file, output_dir='wav', voice_name='mei')
    with open('wav/' + output_file, 'rb') as f:
        data = f.read()
        io.send(ip, port, data)
    sound = AudioSegment.from_file('wav/' + output_file, 'wav')
    return sound.duration_seconds


def play_wav(ip:str, wav_file:str, port=13000) -> float:
    """
    音声ファイルを再生する。
    """
    with open(wav_file, 'rb') as f:
        data = f.read()
        io.send(ip, port, data)
    sound = AudioSegment.from_file(wav_file, 'wav')
    return sound.duration_seconds


if __name__ == '__main__':
    # Commadline option
    parse = argparse.ArgumentParser()
    parse.add_argument('--host', required=True)
    parse.add_argument('--port', default=13000, type=int)
    args = parse.parse_args()

    # Global variables
    HOST = args.host
    PORT = args.port


    # 文字列を音声合成しSpeechSereverForUnityChanに送信する。
    text = 'おはようございます。私はユニティちゃんです。どうぞよろしくお願いします。'
    t = say_text(HOST, text)
    print(text, 'time:', t)
    time.sleep(t + 3)

    # サンプルのWavファイルをSpeechSereverForUnityChanに送信する。
    text = 'サンプルのWavファイルを再生します。'
    t = play_wav(HOST, 'sample.wav')
    print('Sample.wav', 'time:', t)
    time.sleep(t + 3)

    # キーボードから入力した文字列をSpeechSereverForUnityChanに送信する。
    while True:
        print('文字列を入力してください。qを押したら終了します。')
        text = input('> ')
        if text == 'q':
            break
        t = say_text(HOST, text)
        print(text, 'time:', t)
        time.sleep(t + 3)


