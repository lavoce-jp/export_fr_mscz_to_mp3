# 開発者はLaVoce23期Web担当です。わからないことがあれば聞いてください。
from lxml import etree
import subprocess
from zipfile import ZipFile
import os

file_list = os.listdir()
mscz_list = [] # ファイル名のリスト
for x in file_list:
    if x.endswith('.mscz'):
        mscz_list.append(x)

# コンピュータ内のmscoreの場所を保持
mscore = '/Applications/MuseScore 3.app/Contents/MacOS/mscore'

for mscz in mscz_list:
    title = mscz.replace('.mscz', '')
    tmp = title + '/.tmp'
    subprocess.run(['mkdir', '-p', tmp])

    # pdfを出力
    subprocess.run([
        mscore,
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
            mscore,
            part_list[i],
            '-o',
            title + '/' + title + '_' + parts[i] + '.mp3'
        ])
        proc_list.append(proc)
        if i + 1 == length:
            for subproc in proc_list:
                subproc.wait()

    # tmpディレクトリを削除
    subprocess.run(['rm', '-r', tmp])
    subprocess.run(['mv', mscz, title])
    # subprocess.run(['zip', '-r', title + '.zip', title])
    # subprocess.run(['rm', '-r', title])
