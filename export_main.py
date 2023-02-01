from lxml import etree
import subprocess
from zipfile import ZipFile
import os
import operator
import argparse

# コンピュータ内のmscoreの場所を保持(MacOS)
MSCORE = '/Applications/MuseScore 3.app/Contents/MacOS/mscore'
# コンピュータ内のmscoreの場所を保持(Windows)
# MSCORE = 'C:\Program Files\MuseScore 3\bin\MuseScore3.exe'
# コンピュータ内のmscoreの場所を保持(WSL:Windows Subsystem for Linux)
# MSCORE = '/mnt/c/Program Files/MuseScore 3/bin/MuseScore3.exe'

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


def export_pitch_info(tree,parts,title):
    length = len(parts)

    # 音域出力
    # 音域情報の記録ファイルを定義
    pitchRangeRecordFile = f'{title}/{title}_pitchinfo.txt'
    pitchRange = ''
    for i in range(1,length+1):
        # MaxMin = {'StaffMin':['min'],'StaffMax':['max']}
        MaxMin = StaffMaxMin(tree,i)
        pitchRange += f'partID:{i},partName:{parts[i-1]},\tMin:{MaxMin["StaffMin"]},\tMinbars={MaxMin["StaffMinBars"]},\tMax:{ MaxMin["StaffMax"]},\tMaxbars={MaxMin["StaffMaxBars"]}\n'
        # pitchRange += f'partID:{i},partName:{parts[i]}'
    with open(pitchRangeRecordFile,mode = 'w') as f:
        f.write(pitchRange)
    
    print(f'\t{title}\t:pitchinfo export complete')


def export_mp3(tree,parts,title):
    
    length = len(parts)
    tmp = title + '/.tmp'

    # フェーダー情報
    controllers = tree.xpath('//Part/Instrument/Channel/controller[@ctrl="7"]')

    # 一旦フェーダーの要素を全て削除する
    for x in controllers:
        x.getparent().remove(x)
    
    # 全Partに対しフェーダー情報をセットし、ctrlに7を設定
    for i in range(length):
        tree.xpath('//Part[' + str(i + 1) + ']/Instrument/Channel')[0].append(etree.Element('controller'))
        child = tree.xpath('//Part[' + str(i + 1) + ']/Instrument/Channel/controller')[0]
        child.attrib['ctrl'] = '7'

    # 再び変数に代入
    controllers = tree.xpath('//Part/Instrument/Channel/controller[@ctrl="7"]')

    # パートのmscxをリストで保存
    part_list = []

    # 音源を出力
    for i in range(length):
        # フェーダー情報の書き換え
        for j in range(length):
            if j == i:
                controllers[j].attrib['value'] = '100'
            else:
                controllers[j].attrib['value'] = '50'

        # mscxの出力
        part = tmp + '/' + str(i) + '.mscx'
        tree.write(
            part,
            pretty_print = True,
            xml_declaration = True,
            encoding = 'utf-8'
        )
        part_list.append(part)

    proc_list = []

    for i in range(length):
        # mp3の出力
        proc = subprocess.Popen([
            MSCORE,
            part_list[i],
            '-o',
            title + '/' + title + '_' + (i+1) + '_' + parts[i] + '.mp3'
        ])
        proc_list.append(proc)
        if i + 1 == length:
            for subproc in proc_list:
                subproc.wait()
    
    print(f'\t{title}\t:mp3 export complete')


def sub_function(mscz,args):
    '''
        各msczに対して実行する。
        title生成、tmpディレクトリ生成、
    
    '''


    title = mscz.replace('.mscz', '')
    tmp = title + '/.tmp'
    subprocess.run(['mkdir', '-p', tmp])

    if args.pdf :
        # pdfを出力
        subprocess.run([
            MSCORE,
            mscz,
            '-o',
            title +'/' + title + '.pdf'
        ])

    # msczをunzipし、mscxをtmpディレクトリに格納
    with ZipFile(mscz, 'r') as mscx_zip:
        file_names = mscx_zip.namelist()
        for file_name in file_names:
            if file_name.endswith('.mscx'):
                mscx_zip.extract(file_name, tmp)
                break

    # mscxをリネーム（パス付き）
    mscx = tmp + '/' + title + '.mscx'
    os.rename(tmp + '/' + file_name, mscx)

    # mscxをparse
    tree = etree.parse(mscx)
    root = tree.getroot()

    # workTitleをtitleに変更
    workTitle = tree.xpath('//metaTag[@name="workTitle"]')
    workTitle[0].text = title

    # パート名を出力
    parts = tree.xpath('//longName')
    parts = [parts[i].text for i in range(len(parts))]
    length = len(parts)

    # pitch info出力
    export_pitch_info(tree,parts,title)
    # mp3の出力
    if args.mp3:
        export_mp3(tree,parts,title)

    # tmpディレクトリを削除
    subprocess.run(['rm', '-r', tmp])
    if args.mv_mscz:
        subprocess.run(['mv', mscz, title])
    # subprocess.run(['zip', '-r', title + '.zip', title])
    # subprocess.run(['rm', '-r', title])





def main_function(args):
    '''python実行時必ず呼び出される'''
    


    currentDirectory = os.getcwd()
    print(f'Current working directory:{currentDirectory}')

    file_list = os.listdir()
    mscz_list = [] # ファイル名のリスト
    for x in file_list:
        if x.endswith('.mscz'):
            mscz_list.append(x)

    print(f'mscx_list={mscz_list}')
    
    # file指定の有無で呼び出す回数を変える。
    if args.file is None :
        for mscz in mscz_list:
            print('target file:',mscz,'\t','args:',args)
            sub_function(mscz,args)
    else:
        sub_function(args.file,args)





if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）') # 2. パーサを作る

    # 3. parser.add_argumentで受け取る引数を追加していく
    # parser.add_argument('arg1', help='この引数の説明（なくてもよい）') # 必須の引数を追加
    # parser.add_argument('arg2', help='foooo')
    # parser.add_argument('--arg3') # オプション引数（指定しなくても良い引数）を追加
    # parser.add_argument('-a', '--arg4') # よく使う引数なら省略形があると使う時に便利

    parser.add_argument('--pdf',action='store_true', help='if selected, export score as a pdf file.')
    parser.add_argument('--mp3',action='store_true', help='if selected, export a mp3 file for each part.')
    parser.add_argument('-f', '--file', help='if file name is specified, export files only for that file.')
    parser.add_argument('-m', '--mv-mscz', action='store_true', help = 'if selected, delete the original mscz file and create copy in the Child file.')


    args = parser.parse_args() # 4. 引数を解析

    # print('arg1='+args.arg1)
    # print('arg2='+args.arg2)
    # print('arg3='+args.arg3)
    print('file=',args.file)


    main_function(args)
    print('all files export complete.')