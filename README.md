# export_fr_mscz_to_mp3

　このPython3スクリプトは、 `.mscz` ファイルから各声部の音域を`.txt`の形式で書き出すためのプログラムです。さらに、オプション引数を指定すれば`.pdf`形式での楽譜の出力、各パート音源の`.mp3`での出力も可能です。

## preparation

実行するためには、 python3の実行環境とパッケージが必要です。
Terminalで
`python -V`や`python3 -V `と打って、pythonのバージョンが3であることを確かめてください。

もしインストールされていない場合は、
[参考サイト1](https://it-syoya-engineer.com/mac-python-default-change/#:~:text=mac%E3%81%AF%E3%83%87%E3%83%95%E3%82%A9%E3%83%AB%E3%83%88%E3%81%A7python16%E3%81%8C%E5%85%A5%E3%81%A3%E3%81%A6%E3%81%84%E3%81%BE%E3%81%99%E3%80%82)などに従ってPython3をインストールしてください。


## required packages

要求されるパッケージは [`requirement.txt`](requirement.txt)に記載してあります。

現在の所`lxml`のみが要求されます。
`pip install lxml`を走らせることでインストールできます。
`pip install -r requirement.txt`としても構いません。

pip がインストールされていない場合、
[参考サイト](https://yumarublog.com/python/pip-install/)によると、
terminalで
`curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`
を走らせ、そのの次に
`python get-pip.py`
を走らせるとインストールできるようです。

もしもできなければ、`python3 -m install pip`でインストールできるかと思います。

## usage

`python3 export_main.py -f example.mscz`
（または
`python export_main.py -f example.mscz`）
を実行してください。するとこのコマンドは、このコマンドを実行したディレクトリ中に`example.mscz`がある場合はそのファイルから各パートの音域の情報を抜き出して、`example/example_pitchinfo.txt`を生成します。

`python3 export_main.py ` とすると、同じ操作をディレクトリ中の全ての`.mscz`ファイルに対して実行します。

`python3 export_main.py -f example.mscz --pdf` とすると楽譜のPDFファイルが書き出され、
`python3 export_main.py -f example.mscz --mp3` とすると各パートの`.mp3`音源が書き出されます。

`python3 export_main.py --mp3 --pdf ` とすることもできます。

## help for each arguments

`--pdf`             :if selected, export score as a pdf file.

`--mp3`             :if selected, export a mp3 file for each part.

`-f` or `--file`      :if file name is specified, export files only for that file.

`-m` or `--mv-mscz`   :if selected, delete the original mscz file and create copy in the child directory.
