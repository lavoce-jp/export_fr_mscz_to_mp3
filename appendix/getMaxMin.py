from lxml import etree
import operator
import os

# # Measure = 小節 を取得
# Measures_2 = tree.xpath('//Staff[@id="2"]/Measure')
# Measure_24 = Measures_2[4]

# print(type(Measure_24))
# # voice_240 = Measure_24.findall('voice')[0]
# voice_240 = Measure_24[0]
# Chord_2400 = voice_240[0]
# Chord_2401 = voice_240[1]
# Chord_2402 = voice_240[2]
# rest_2403 = voice_240[3]

# Note_24000 = Chord_2400.findall('Note')[0]
# Pitch_240000 = Note_24000[0]

# print(Pitch_240000)
# print(Pitch_240000.text)

# Chords_240 = voice_240.findall('Chord')
# print( Chords_240[0] == Chord_2400 )
# print( Chords_240[1] == Chord_2401 )
# print( Chords_240[2] == Chord_2402 )

# pitchesTexts_240 = []

# for i, Chord_240i in enumerate( Chords_240 ) :
#     Note_240i0 = Chord_240i.findall('Note')[0]
#     pitch_240i00 = Note_240i0[0]
#     pitchesTexts_240.append(pitch_240i00.text)

def MeasureMaxMin(Measure):

    #声部1を取得 idx=0
    # voice_nn0 = Measure.find('voice')[0]
    voice_nn0 = Measure[0]
    Chords_nn0 = voice_nn0.findall('Chord')
    if Chords_nn0 == []:
        return {'isAllRest':True}
    pitchesInts_nn0 = [] # 最大最小を格納

    #各Chord内部でのNote>pitchの値を格納
    for i, Chord_nn0i in enumerate( Chords_nn0 ) :
        Note_nn0i0 = Chord_nn0i.findall('Note')[0]
        pitch_nn0i00 = Note_nn0i0[0]
        try:
            pitchInt_nn0i00 = int(pitch_nn0i00.text)
        except ValueError as e :
            # print(e)
            # print(type(e))
            # print(f'pitch_nn0i00.text = {pitch_nn0i00.text}')
            pass
        else :
            pitchesInts_nn0.append(pitchInt_nn0i00)
        
    if pitchesInts_nn0 == []:
        return {'isAllRest':True,'Min':None,'Max':None}

    pitchesSorted = sorted(pitchesInts_nn0)
    
    Min = pitchesSorted[0]
    Max = pitchesSorted[-1]

    return {'isAllRest':False,'Min':Min,'Max':Max}

# # Measure = 小節 を取得
# Measures_2 = tree.xpath('//Staff[@id="2"]/Measure')

# barPitchMinMax_2 = []
# for i, Measure_2n in enumerate(Measures_2):
#     #　辞書の結合書式**を使ってbarを加える
#     barPitchMinMax_2.append({**MeasureMaxMin(Measure_2n), 'bar':i})

# barPitchMinMax_2_OmitAllRest = list(filter(lambda x: x['isAllRest'] == False,barPitchMinMax_2))
# barPitchMin_2 = sorted(barPitchMinMax_2_OmitAllRest,key=operator.itemgetter('Min'))
# barPitchMax_2 = sorted(barPitchMinMax_2_OmitAllRest,key=operator.itemgetter('Max'))

def StaffMaxMin(tree,id):
    # Measure = 小節 を取得
    Measures_n = tree.xpath(f'//Staff[@id="{id}"]/Measure')

    barPitchMinMax_n = []
    for i, Measure_nn in enumerate(Measures_n):
        #　辞書の結合書式**を使ってbarを加える
        barPitchMinMax_n.append({**MeasureMaxMin(Measure_nn), 'bar':i+1})

    barPitchMinMax_n_OmitAllRest = list(filter(lambda x: x['isAllRest'] == False,barPitchMinMax_n))
    # 全休符の小節を除いた小節を音程低い・高い順に並びかえ 
    barPitchMin_n = sorted(barPitchMinMax_n_OmitAllRest, key=operator.itemgetter('Min'))
    barPitchMax_n = sorted(barPitchMinMax_n_OmitAllRest, key=operator.itemgetter('Max'))

    # 最低音程と該当の小節複数 
    minPitch = barPitchMin_n[0]['Min']
    minPitchText = mapPitchNum_to_text(minPitch)
    # minPitchText = minPitch
    minBars = [barPitchMin_n[0]['bar']]
    counter_i = 1
    while barPitchMin_n[counter_i]['Min'] == minPitch:
        minBars.append(barPitchMin_n[counter_i]['bar'])
        counter_i += 1
    
    # 最高音程と該当の小節複数 
    maxPitch = barPitchMax_n[-1]['Max']
    maxPitchText = mapPitchNum_to_text(maxPitch)
    # maxPitchText = maxPitch
    maxBars = [barPitchMax_n[-1]['bar']]
    # counter_i initせず
    while barPitchMax_n[counter_i]['Max'] == maxPitch:
        maxBars.append(barPitchMax_n[counter_i]['bar'])
        counter_i -= 1
    # counterif = assert(counter_i==1)
    
    pitchMM_and_barNum = dict(StaffMin=minPitchText,StaffMinBars=minBars,StaffMax=maxPitchText,StaffMaxBars=maxBars)

    
    # return {'StaffMin':barPitchMin_n,'StaffMax':barPitchMax_n}
    # return [barPitchMin_n,barPitchMax_n]
    return pitchMM_and_barNum

def mapPitchNum_to_text(pitchNum): # Cis4 = 49,Fis4 = 54,G4 = 55,Cis5=61 D6 = 71
    
    # pitchOct,toneNum = divmod(pitchNum, 12)
    pitchOct = (pitchNum//12) - 1
    toneNum = pitchNum - 12*(pitchOct+1)
    toneText = 'X'
    if toneNum <= 5:
        if toneNum <= 2:
            if toneNum==0:
                toneText='C'
            elif toneNum==1:
                toneText='C#'
            elif toneNum==2:
                # toneNum case 2
                toneText='D'
            else:
                pass

        elif toneNum >= 2:
            if toneNum==3:
                toneText='E♭/D#'
            elif toneNum==4:
                toneText='E'
            elif toneNum==5: # case 5:
                toneText='F'
            else:
                pass
              
        else:
            pass
    elif toneNum>=6:
        # toneNum >= 6
        if toneNum <= 8:
            if toneNum==6:
                toneText='F#'
            elif toneNum==7:
                toneText='G'
            elif toneNum==8:
                # case 8:
                toneText='A♭/G#'
            else:
                pass
        elif toneNum >= 9:
            if toneNum==9:
                toneText='A'
            elif toneNum==10:
                toneText='B♭'
            elif toneNum==11:
                # case 11:
                toneText='B'
            else:
                pass
        else:
            pass
    else:
        pass

    toneText += str(pitchOct)
    return toneText


if __name__ == '__main__':
    mscx = './getMaxMin/Oz.楽譜案_0211.mscx'
    tree = etree.parse(mscx)
    root = tree.getroot()
    print(StaffMaxMin(tree,2))


