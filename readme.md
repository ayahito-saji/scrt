# Scrt

Scrt(ソクラト)は命題論理の論理証明システムです．

現在，一階述語論理(FOL)への拡張およびダブロー法による証明の実装を試みています．

## できること

* 命題論理式で表された任意の問題の充足可能性をチェックできます．（CNFに変換してDPLLアルゴリズムで調べる）


## 問題例

### 充足可能性チェック
「充足可能性問題」というのは「与えられた命題論理式を満たすような変数割当が存在するか調べよ．また割当が存在する場合はそのうちの一つを出力せよ．」という問題です．

簡単に言うと，「PとかQとかの変数で作られた論理式がTrueになることはあるでしょうか？あるならその時のPとかQとかの変数の値を教えてください」という問題です．

* 「Pかつ（Pではない）」という命題論理式をTrueにするようなPはあるか？

PがTrueでもFalseでも，与えられた命題論理式をTrueにすることはできないのでFalseを返します．

* 「Pかつ(PならばQ)」という命題論理式をTrueにするようなP, Qはあるか？

P=True, Q=Trueで与えられた命題論理式をTrueにできるのでTrueを返します．また，この時のPとQを返します．


## 使い方
以下はサンプルプログラムです．
```
from scrt.logic import LogicalAtom
from scrt.satsolver import SatSolver

p = LogicalAtom('p')
q = LogicalAtom('q')

expr = (p >> q) & p

print(expr)
result, allocation = SatSolver.solve(expr)
print(result, allocation)
```
論理式の変数は`LogicalAtom()`で宣言します．
サンプルプログラムでは変数`p`と`q`を定義しています．

論理式は`&`（かつ），`|`（または），`~`（否定），`>>`（左ならば右）`<<`（右ならば左），`()`（括弧）でつないで式にできます．
サンプルプログラムでは「pかつ（pならばq）」という命題論理式を`expr`に代入しています．

`SatSolver.solve(命題論理式)`と呼び出すことで命題論理式の充足可能性をDPLLアルゴリズムで調べることができます．

充足可能性を調べるためにSATソルバを使っていますが，これはPythonのみで実装されており速度は期待できません．
外部ソルバを使って充足可能性を調べることもできます．
`SatSolver.solve(命題論理式, external_solver="外部ソルバコマンド")`

例としてMiniSatをインストールして用いる場合は，`minisat`コマンドが利用できる状態で次のように記述します．
`SatSolver.solve(命題論理式, external_solver="minisat")`
これでMiniSatを利用して高速に解くことができるようになります．