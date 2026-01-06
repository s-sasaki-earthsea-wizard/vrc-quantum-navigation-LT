# vrc-quantum-navigation-LT

## 概要

原子干渉計を用いた量子航法（Quantum Navigation）に関するプレゼンテーション資料です。GPS不要の高精度慣性航法システムの原理と実用化について解説しています。

## コンテンツ

- **スライド**: reveal.jsによるプレゼンテーション
- **YouTube台本**: 解説動画用のスクリプト
- **Manimアニメーション**: 物理概念を視覚化するアニメーション

## 開発環境

[reveal.js](https://github.com/hakimel/reveal.js) によってスライドの作成をしています。
Node.js, npmが利用できる環境で、以下のコマンドで開発環境の構築ができます:

```bash
npm install
```

### Manimアニメーション

アニメーション作成には [Manim Community](https://www.manim.community/) を使用しています。

```bash
pip install manim
```

## 使い方

### スライド作成

以下のコマンドでローカルサーバーを起動:

```bash
cd slides-jp
npm start
```

ブラウザで [http://localhost:8000](http://localhost:8000) にアクセスすると、スライドをプレビューできます。

### スライドをpdfでエクスポート

`decktape`を使ってスライドをPDFにエクスポートできます。

1. `decktape`のインストール

```bash
npm install -g decktape
```

2. PDFエクスポート

以下のコマンドで`html`で書いたスライドをpdfにエクスポートできます:

``` bash
# 16:9のスライドの場合
decktape --size 1920x1080 index.html slides.pdf

# 4:3のスライドの場合
decktape --size 1600x1200 index.html slides.pdf
```

### Manimアニメーションのレンダリング

```bash
# 低画質プレビュー
manim -pql scripts/<filename>.py <SceneName>

# 高画質レンダリング
manim -pqh scripts/<filename>.py <SceneName>
```

## アニメーションスクリプト一覧

| ファイル | 内容 |
|---------|------|
| `distance_formula_animation.py` | 移動距離の公式 (x = vt) |
| `double_integral_animation.py` | 加速度の二重積分、誤差蓄積問題 |
| `de_broglie_wavelength_animation.py` | ド・ブロイ波長と物質波 |
| `particle_wave_animation.py` | 粒子運動と波動の重ね合わせ |
| `laser_cooling_animation.py` | レーザー冷却、ドップラー選択的冷却 |
| `raman_transition_animation.py` | ラマン遷移による状態制御 |
| `precision_comparison_animation.py` | MEMS vs 原子干渉計の精度比較 |
| `mach_zehnder_animation.py` | マッハ・ツェンダー型原子干渉計 |
| `maxwell_boltzmann_animation.py` | マクスウェル・ボルツマン分布 |
| `vt_graph_animation.py` | 速度-時間グラフ |

## 免責事項

- 本スライドの内容に従ったいかなる結果において著者は一切の責任を負いません

## LICENSE

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

This project uses [reveal.js](https://github.com/hakimel/reveal.js) which is also licensed under the MIT License.
