#!/usr/bin/env python3
import io
import struct
import wave

from functools import partial

if __name__ == '__main__':
    import argparse

    from . import sputm

    parser = argparse.ArgumentParser(description='read smush file')
    parser.add_argument('filename', help='filename to read from')
    args = parser.parse_args()

    with open(args.filename, 'rb') as res:
        tlkb = sputm.assert_tag('TLKB', sputm.untag(res))
        assert res.read() == b''
        chunks = (sputm.assert_tag('TALK', chunk) for chunk in sputm.drop_offsets(sputm.read_chunks(tlkb)))
        for idx, chunk in enumerate(chunks):
            sound = b''
            for _, (tag, data) in sputm.read_chunks(chunk):
                if tag == 'HSHD':
                    print(len(data))
                    print(tag, data)
                    with io.BytesIO(data) as hshd:
                        unk1 = struct.unpack('<H', hshd.read(2))[0]  # 0
                        unk2 = struct.unpack('<H', hshd.read(2))[0]  # 32896
                        unk3 = struct.unpack('<H', hshd.read(2))[0]  # 65535
                        sample_rate = struct.unpack('<H', hshd.read(2))[0]
                        unk4 = struct.unpack('<H', hshd.read(2))[0]
                        unk5 = struct.unpack('<H', hshd.read(2))[0]
                        unk6 = struct.unpack('<H', hshd.read(2))[0]
                        unk7 = struct.unpack('<H', hshd.read(2))[0]
                    print(unk1, unk2, unk3, sample_rate, unk4, unk5, unk6, unk7)
                    continue
                if tag == 'SBNG':
                    continue
                if tag == 'SDAT':
                    print(len(data))
                    sound = data
                    continue
            # save raw
            # with open(f'OUT/TALK_SDAT_{idx:04d}.RAW', 'wb') as aud:
            #     # aud.write(b'\x80' * frame_audio_size[12] * frame_no)
            #     aud.write(sound)
            with wave.open(f'OUT/TALK_SDAT_{idx:04d}.WAV', 'w') as wav:
                # aud.write(b'\x80' * frame_audio_size[12] * frame_no)
                wav.setnchannels(1)
                wav.setsampwidth(1) 
                wav.setframerate(sample_rate)
                wav.writeframesraw(sound)
            print('==========')
