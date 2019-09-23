
class Transposer():

    SEMITONES = {
        0: ["C"],
        1: ["C#", "Db"],
        2: ["D"],
        3: ["D#", 'Eb'],
        4: ["E"],
        5: ["F"],
        6: ["F#", "Gb"],
        7: ["G"],
        8: ["G#", "Ab"],
        9: ["A"],
        10: ["A#", "Bb"],
        11: ["B"]
    }
    INSTRUMENTS = {
        "French Horn": "F",
        "Trumpet": "Bb",
        "Clarinet": "Bb",
        "Bass Clarinet": "Bb",
        "Alto Saxophone": "Eb",
        "Tenor Saxophone": "Bb",
        "Baritone Saxophone": "Eb",
        "Soprano Saxophone": "Bb",
    }

    def __init__(self, tokey=None, instrument=None, from_instrument=None, text=None):
        self.key = tokey
        self.to_instrument = instrument
        self.from_instrument = from_instrument
        self.text = text
    
    def transpose(self, fr=None, to=None, text=None):
        if to:
            key = to
        elif self.to_instrument:
            key = Transposer.INSTRUMENTS.get(self.to_instrument, 'C')
        else:    
            key = self.key
        if fr:
            frm = fr
        elif self.from_instrument:
            frm = Transposer.INSTRUMENTS.get(self.from_instrument, 'C')
        else:    
            frm = 'C'
        if text:
            return self.transpose_helper(frm, key, text)
        else:
            return self.transpose_helper(frm, key, self.text)
        
    def transpose_helper(self, fr, to, text):
        if not fr or not to:
            raise ValueError("No from key or to key")
        if not text:
            raise ValueError("No text to transpose")
        key_distance = self.get_semitone_distance(fr, to)
        text_list = list(self.processText(text))
        new_notes = []
        for note in text_list:
            new = self.get_wraparound(sorted(Transposer.SEMITONES.keys()), self.get_note_dex(note), key_distance)
            if "b" in note or "b" in to: # We want to match the flat or sharp of the original note
                try:
                    new_note = new[1]
                except IndexError:
                    new_note = new[0]
            else:
                new_note = new[0]
            new_notes.append(new_note)
                #TODO Fix
        return new_notes

    def processText(self, text):
        new_list = []
        i = len(text) - 1
        while i >= 0:
            if text[i] == 'b' or text[i] == '#':
                new_list.append(text[i-1] + text[i])
                i -= 2
            else:
                new_list.append(text[i])
                i -= 1
        return reversed(new_list)


    def get_note_dex(self, note):
        for dex, semitone in Transposer.SEMITONES.items():
            if note in semitone:
                return dex
        return -1
    
    def get_semitone_distance(self, fr, to):
        fr_dex = self.get_note_dex(fr)
        to_dex = self.get_note_dex(to)
        if fr_dex == -1 or to_dex == -1:
            raise ValueError()
        count = 0
        while fr_dex != to_dex:
            fr_dex += 1
            count += 1
            if fr_dex == len(Transposer.SEMITONES.keys()):
                fr_dex = 0
        return -1 * count

    def get_wraparound(self, itr, dex, addition):
        new_dex = dex + addition
        if new_dex > len(itr) - 1:
            new_dex = new_dex % len(itr)
        elif new_dex < 0:
            new_dex = len(itr) + new_dex
        return Transposer.SEMITONES[itr[new_dex]]

if __name__ == '__main__':
    t = Transposer(instrument='French Horn', from_instrument="NA")
    print(t.transpose(fr='Bb', to='C', text='DGFECDFG'))
    print(t.transpose(fr='F', to='C', text='EbGGFABb'))
    print(t.transpose(fr='C', to='F', text='AbCCBbDEb'))
    print(t.transpose(fr='C', to='Eb', text='BbFAbEbGDEbFFFFEEbEbEbC'))
    print(t.transpose(text="CDEFGAB"))