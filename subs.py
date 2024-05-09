import pvleopard
from typing import *

picovoice_key = "LLTl+AsCZt4NbozMs0fV57FZI/5AOZ2b/WP6oqoPpr1sbUZ8eDw6cA=="
leopard = pvleopard.create(access_key = picovoice_key)

def second_to_timecode(x: float) -> str:
    hour, x = divmod(x, 3600)
    minute, x = divmod(x, 60)
    second, x = divmod(x, 1)
    millisecond = int(x * 1000.)

    return '%.2d:%.2d:%.2d,%.3d' % (hour, minute, second, millisecond)

def to_srt(words: Sequence[pvleopard.Leopard.Word], endpoint_sec: float = 1., length_limit: Optional[int] = 16) -> str:
    def _helper(end: int) -> None:
        lines.append("%d" % section)
        lines.append(
            "%s --> %s" %
            (second_to_timecode(words[start].start_sec), second_to_timecode(words[end].end_sec)))
        lines.append(' '.join(x.word for x in words[start:(end + 1)]))
        lines.append('')

    lines = list()
    section = 0
    start = 0
    for k in range(1, len(words)):
        if ((words[k].start_sec - words[k - 1].end_sec) >= endpoint_sec) or \
                (length_limit is not None and (k - start) >= length_limit):
            _helper(k - 1)
            start = k
            section += 1
    _helper(len(words) - 1)

    return '\n'.join(lines)

def get_str_file(file_name):
    transcript, words = leopard.process_file(f'assets/{file_name}.mp3')
    with open('assets/subs.srt', 'w') as f:
        # noinspection PyUnboundLocalVariable
        f.write(to_srt(words))
        f.write('\n')
    return words