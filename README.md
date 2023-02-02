# export_fr_mscz_to_mp3

　このPython3スクリプトは、 `.mscz` ファイルから各声部の音域を`.txt`の形式で書き出すためのプログラムです。さらに、オプション引数を指定すれば`.pdf`形式での楽譜の出力、各パート音源の`.mp3`での出力も可能です。

## preparation

実行するためには、 python3の実行環境とパッケージが必要です。


## required packages

要求されるパッケージは [`requirement.txt`](requirement.txt)に記載してあります。

現在の所`lxml`のみが要求されます。
`pip install lxml`を走らせることでインストールできます。
`pip install -r requirement.txt`としても構いません。

pip がインストールされていない場合、`brew install pip`でインストールできるかと思います。

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
