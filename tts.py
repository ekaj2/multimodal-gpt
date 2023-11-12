import threading
from time import sleep
import os
import sounddevice as sd
import soundfile as sf
import queue
import sys
import threading

from openai import OpenAI

from settings import FILES_DIR

client = OpenAI()
speech_file_path = FILES_DIR / "speech.flac"


def stream_audio_to_file(text):
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
        response_format="flac"
    )
    response.stream_to_file(speech_file_path)


def say(text):
    try:
        os.remove(speech_file_path)
    except FileNotFoundError:
        pass
    # Start streaming in a separate thread
    t = threading.Thread(target=stream_audio_to_file, args=(text,))
    t.start()
    t.join()

    blocksize = 128
    buffersize = 20

    # TODO: make this actually stream the file before it's finished writing
    # This is largely borrowed from:
    # https://python-sounddevice.readthedocs.io/en/0.4.6/examples.html#play-a-very-long-sound-file
    q = queue.Queue(maxsize=buffersize)
    event = threading.Event()

    def callback(outdata, frames, time, status):
        assert frames == blocksize
        if status.output_underflow:
            print('Output underflow: increase blocksize?', file=sys.stderr)
            raise sd.CallbackAbort
        assert not status
        try:
            data = q.get_nowait()
        except queue.Empty as e:
            print('Buffer is empty: increase buffersize?', file=sys.stderr)
            raise sd.CallbackAbort from e
        if len(data) < len(outdata):
            outdata[:len(data)] = data
            outdata[len(data):] = b'\x00' * (len(outdata) - len(data))
            raise sd.CallbackStop
        else:
            outdata[:] = data

    try:
        with sf.SoundFile(speech_file_path) as f:
            for _ in range(buffersize):
                data = f.buffer_read(blocksize, dtype='float32')
                if not data:
                    break
                q.put_nowait(data)  # Pre-fill queue
            stream = sd.RawOutputStream(
                samplerate=f.samplerate, blocksize=blocksize,
                channels=f.channels, dtype='float32',
                callback=callback, finished_callback=event.set)
            with stream:
                timeout = blocksize * buffersize / f.samplerate
                while data:
                    data = f.buffer_read(blocksize, dtype='float32')
                    q.put(data, timeout=timeout)
                print("Done...")
                event.wait()  # Wait until playback is finished
    except KeyboardInterrupt:
        exit('\nInterrupted by user')
    except queue.Full:
        print("queue full")
    except Exception as e:
        pass


if __name__ == "__main__":
    say("""
A Fox one day spied a beautiful bunch of ripe grapes hanging from a vine trained along the branches of a tree. The grapes seemed ready to burst with juice, and the Fox's mouth watered as he gazed longingly at them.

The bunch hung from a high branch, and the Fox had to jump for it. The first time he jumped he missed it by a long way. So he walked off a short distance and took a running leap at it, only to fall short once more. Again and again he tried, but in vain.

Now he sat down and looked at the grapes in disgust.

"What a fool I am," he said. "Here I am wearing myself out to get a bunch of sour grapes that are not worth gaping for."

And off he walked very, very scornfully.

There are many who pretend to despise and belittle that which is beyond their reach.
""")
