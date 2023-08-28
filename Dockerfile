FROM ubuntu:20.04
# apt-getコマンドを使うことで、ubuntuでパッケージのインストールやアップデート、削除などを簡単にできる。
RUN apt-get update
# -yを指定することでパッケージをインストールするたびに出る確認プロンプトに自動でyesと答えてくれる
# bash: GNU Bashシェル（Unixシェルの一種）であり、コマンドラインインターフェースを提供します。
# coreutils: Linuxで一般的に使用される基本的なコマンド群を提供します。例えば、ls、cp、mv、rmなどのコマンドが含まれます。
# grep: ファイル内の文字列を検索するためのコマンドです。
# iproute2: Linuxカーネルのネットワーク構成ツールで、ネットワークインターフェースやルーティングテーブルの設定に使用されます。
# iputils-ping: ネットワークデバイスの到達性をテストするために使用されるpingコマンドの一部です。
# traceroute: パケットが通る経路をトレースし、ネットワークの経路情報を表示するために使用されます。
# tcpdump: ネットワークトラフィックをキャプチャして表示するためのパケット解析ツールです。
# bind9-dnsutils: BIND DNSサーバーのユーティリティツールを提供します。
# dnsmasq-base: DHCPサーバーやDNSキャッシュを提供する軽量で高速なネットワークサービスを提供するdnsmasqのベース部分です。
# netcat-openbsd: ネットワーク接続を作成・監視・操作するためのユーティリティツールです。
# python3: Pythonプログラミング言語のバージョン3のランタイムとライブラリを提供します。
# curl: コマンドラインからURLを操作し、データの送受信を行うためのツールです。
# wget: コマンドラインからファイルをダウンロードするためのツールです。
# iptables: Linuxのファイアウォール機能を管理するためのツールです。
# procps: プロセスに関連する情報を表示・操作するためのツール群です。
# isc-dhcp-client: DHCPクライアントを提供します。
# DHCPは「コンピュータにIPアドレスを自動割り当てする仕組み」
# DHCPサーバは、人間様の代わりに、コンピュータにIPアドレスを割り当てる仕事をやるコンピュータのこと
# DHCPクライアントとは、DHCPサーバとやり取りしてIPアドレスを割り当ててもらう側のコンピュータのこと。
# https://wa3.i-3-i.info/word18660.html
RUN apt-get -y install bash coreutils grep iproute2 iputils-ping traceroute tcpdump bind9-dnsutils \
    dnsmasq-base netcat-openbsd python3 curl wget iptables procps isc-dhcp-client