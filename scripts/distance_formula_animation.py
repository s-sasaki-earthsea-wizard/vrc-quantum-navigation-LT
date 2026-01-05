"""
移動距離の公式アニメーション

「移動距離 = 速さ × 時間」と「x = vt」を表示する

使用方法:
    manim -pql distance_formula_animation.py DistanceFormula
    manim -pqh distance_formula_animation.py DistanceFormula  # 高画質
"""

from manim import *


class DistanceFormula(Scene):
    """移動距離の公式を示すアニメーション"""

    def construct(self):
        # 色の設定
        TEXT_COLOR = WHITE
        FORMULA_COLOR = YELLOW

        # 日本語テキスト「移動距離 = 速さ × 時間」
        japanese_text = Text(
            "移動距離 = 速さ × 時間",
            font_size=48,
            color=TEXT_COLOR,
        )

        # 数式「x = vt」
        math_formula = MathTex(
            r"x = vt",
            font_size=72,
            color=FORMULA_COLOR,
        )

        # 日本語テキストを表示
        self.play(Write(japanese_text), run_time=1.5)
        self.wait(1)

        # 数式に変換
        self.play(Transform(japanese_text, math_formula), run_time=1)
        self.wait(2)

        # フェードアウト
        self.play(FadeOut(japanese_text))


class DistanceFormulaDetailed(Scene):
    """移動距離の公式を詳細に示すアニメーション（各要素を分解）"""

    def construct(self):
        # 色の設定
        DISTANCE_COLOR = GREEN
        VELOCITY_COLOR = BLUE
        TIME_COLOR = RED

        # 日本語テキスト（各要素に色付け）
        distance_jp = Text("移動距離", font_size=42, color=DISTANCE_COLOR)
        equals_jp = Text(" = ", font_size=42, color=WHITE)
        velocity_jp = Text("速さ", font_size=42, color=VELOCITY_COLOR)
        times_jp = Text(" × ", font_size=42, color=WHITE)
        time_jp = Text("時間", font_size=42, color=TIME_COLOR)

        japanese_group = VGroup(
            distance_jp, equals_jp, velocity_jp, times_jp, time_jp
        ).arrange(RIGHT, buff=0.1)

        # 数式（各要素に色付け）
        x_math = MathTex("x", font_size=72, color=DISTANCE_COLOR)
        eq_math = MathTex("=", font_size=72, color=WHITE)
        v_math = MathTex("v", font_size=72, color=VELOCITY_COLOR)
        t_math = MathTex("t", font_size=72, color=TIME_COLOR)

        math_group = VGroup(x_math, eq_math, v_math, t_math).arrange(RIGHT, buff=0.2)

        # 日本語テキストを1つずつ表示
        self.play(Write(distance_jp), run_time=0.5)
        self.play(Write(equals_jp), run_time=0.3)
        self.play(Write(velocity_jp), run_time=0.5)
        self.play(Write(times_jp), run_time=0.3)
        self.play(Write(time_jp), run_time=0.5)
        self.wait(1)

        # 各要素を対応する数式に変換
        self.play(
            Transform(distance_jp, x_math),
            Transform(equals_jp, eq_math),
            Transform(velocity_jp, v_math),
            Transform(times_jp, MathTex("", font_size=72)),  # × は消える
            Transform(time_jp, t_math),
            run_time=1.5,
        )
        self.wait(2)

        # フェードアウト
        self.play(
            FadeOut(distance_jp),
            FadeOut(equals_jp),
            FadeOut(velocity_jp),
            FadeOut(times_jp),
            FadeOut(time_jp),
        )


class DistanceFormulaWithVisual(Scene):
    """移動距離の公式と視覚的な説明を含むアニメーション"""

    def construct(self):
        # 色の設定
        DISTANCE_COLOR = GREEN
        VELOCITY_COLOR = BLUE
        TIME_COLOR = RED

        # タイトル
        title = Text("慣性航法の基本原理", font_size=36, color=WHITE).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # 日本語テキスト
        japanese_text = Text(
            "移動距離 = 速さ × 時間",
            font_size=42,
            color=WHITE,
        )

        # 数式
        math_formula = MathTex(
            r"x = vt",
            font_size=64,
            color=YELLOW,
        )

        # 日本語テキストを表示
        self.play(Write(japanese_text), run_time=1.5)
        self.wait(1)

        # 日本語テキストを上に移動
        self.play(japanese_text.animate.shift(UP * 1.5))

        # 数式を下に表示
        math_formula.next_to(japanese_text, DOWN, buff=0.8)
        self.play(Write(math_formula), run_time=1)
        self.wait(0.5)

        # 変数の説明を追加
        x_label = MathTex("x", color=DISTANCE_COLOR, font_size=36)
        x_desc = Text(": 移動距離", font_size=28, color=WHITE)
        x_group = VGroup(x_label, x_desc).arrange(RIGHT, buff=0.1)

        v_label = MathTex("v", color=VELOCITY_COLOR, font_size=36)
        v_desc = Text(": 速さ（速度）", font_size=28, color=WHITE)
        v_group = VGroup(v_label, v_desc).arrange(RIGHT, buff=0.1)

        t_label = MathTex("t", color=TIME_COLOR, font_size=36)
        t_desc = Text(": 時間", font_size=28, color=WHITE)
        t_group = VGroup(t_label, t_desc).arrange(RIGHT, buff=0.1)

        legend = VGroup(x_group, v_group, t_group).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        legend.next_to(math_formula, DOWN, buff=0.8)

        self.play(
            Write(x_group),
            Write(v_group),
            Write(t_group),
            run_time=1.5,
        )
        self.wait(2)

        # フェードアウト
        self.play(
            FadeOut(title),
            FadeOut(japanese_text),
            FadeOut(math_formula),
            FadeOut(legend),
        )
