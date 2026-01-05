"""
ド・ブロイ波長のアニメーション

物質波の波長 λ = h/(mv) を視覚的に示す

使用方法:
    manim -pql de_broglie_wavelength_animation.py DeBroglieWavelength
    manim -pqh de_broglie_wavelength_animation.py DeBroglieWavelength  # 高画質
"""

from manim import *
import numpy as np


class DeBroglieWavelength(Scene):
    """ド・ブロイ波長の式を示すアニメーション"""

    def construct(self):
        # 色の設定
        WAVELENGTH_COLOR = BLUE
        PLANCK_COLOR = GREEN
        MASS_COLOR = ORANGE
        VELOCITY_COLOR = RED

        # タイトル
        title = Text("原子の波動性（ド・ブロイ波）", font_size=36, color=WHITE).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # 導入テキスト
        intro = Text(
            "すべての物質は波としての性質を持つ",
            font_size=32,
            color=YELLOW,
        ).shift(UP * 1.5)

        self.play(Write(intro))
        self.wait(1)

        # メインの数式
        formula = MathTex(
            r"\lambda_{\text{dB}}", r"=", r"\frac{h}{mv}",
            font_size=72,
        )
        formula[0].set_color(WAVELENGTH_COLOR)  # λ
        formula[2][0].set_color(PLANCK_COLOR)   # h
        formula[2][2].set_color(MASS_COLOR)     # m
        formula[2][3].set_color(VELOCITY_COLOR) # v

        self.play(Write(formula), run_time=2)
        self.wait(1)

        # 数式を上に移動
        self.play(
            intro.animate.scale(0.8).to_edge(UP, buff=0.6),
            formula.animate.shift(UP * 0.5),
            FadeOut(title),
        )

        # 変数の説明
        legend_items = VGroup(
            self._create_legend_item(r"\lambda_{\text{dB}}", "ド・ブロイ波長", WAVELENGTH_COLOR),
            self._create_legend_item("h", "プランク定数", PLANCK_COLOR),
            self._create_legend_item("m", "質量", MASS_COLOR),
            self._create_legend_item("v", "速度", VELOCITY_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        legend_items.shift(DOWN * 1.5)

        self.play(Write(legend_items), run_time=1.5)
        self.wait(2)

        # フェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def _create_legend_item(self, symbol, description, color):
        """凡例アイテムを作成"""
        sym = MathTex(symbol, font_size=36, color=color)
        desc = Text(f": {description}", font_size=24, color=WHITE)
        return VGroup(sym, desc).arrange(RIGHT, buff=0.15)


class DeBroglieWithWave(Scene):
    """ド・ブロイ波長と波の視覚化"""

    def construct(self):
        WAVELENGTH_COLOR = BLUE
        FAST_COLOR = RED
        SLOW_COLOR = GREEN

        # タイトル
        title = Text("ド・ブロイ波長", font_size=36, color=WHITE).to_edge(UP)
        self.play(Write(title))

        # 数式
        formula = MathTex(
            r"\lambda_{\text{dB}} = \frac{h}{mv}",
            font_size=56,
            color=YELLOW,
        ).shift(UP * 2)

        self.play(Write(formula))
        self.wait(0.5)

        # ===== 速い粒子（短い波長）=====
        fast_label = Text("速い粒子 (大きい v)", font_size=24, color=FAST_COLOR)
        fast_label.shift(UP * 0.3 + LEFT * 3)

        # 短い波長の波
        fast_wave = self._create_wave(wavelength=0.5, color=FAST_COLOR)
        fast_wave.next_to(fast_label, DOWN, buff=0.3)

        fast_wavelength = MathTex(r"\lambda \downarrow", font_size=28, color=FAST_COLOR)
        fast_wavelength.next_to(fast_wave, RIGHT, buff=0.3)

        # ===== 遅い粒子（長い波長）=====
        slow_label = Text("遅い粒子 (小さい v)", font_size=24, color=SLOW_COLOR)
        slow_label.shift(DOWN * 1.5 + LEFT * 3)

        # 長い波長の波
        slow_wave = self._create_wave(wavelength=1.5, color=SLOW_COLOR)
        slow_wave.next_to(slow_label, DOWN, buff=0.3)

        slow_wavelength = MathTex(r"\lambda \uparrow", font_size=28, color=SLOW_COLOR)
        slow_wavelength.next_to(slow_wave, RIGHT, buff=0.3)

        # アニメーション
        self.play(Write(fast_label))
        self.play(Create(fast_wave), Write(fast_wavelength))
        self.wait(0.5)

        self.play(Write(slow_label))
        self.play(Create(slow_wave), Write(slow_wavelength))
        self.wait(1)

        # 結論
        conclusion = Text(
            "速度を下げる → 波長が揃う → コヒーレンス向上",
            font_size=26,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.5)

        self.play(Write(conclusion))
        self.wait(2)

        # フェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def _create_wave(self, wavelength, color, length=4):
        """正弦波を作成"""
        wave = FunctionGraph(
            lambda x: 0.3 * np.sin(2 * np.pi * x / wavelength),
            x_range=[0, length],
            color=color,
            stroke_width=3,
        )
        return wave


class DeBroglieVelocitySpread(Scene):
    """速度分布と波長のばらつきの関係"""

    def construct(self):
        HOT_COLOR = RED
        COLD_COLOR = BLUE

        # タイトル
        title = Text("速度分布と波長の関係", font_size=36, color=WHITE).to_edge(UP)
        self.play(Write(title))

        # 数式
        formula = MathTex(
            r"\lambda_{\text{dB}} = \frac{h}{mv}",
            font_size=48,
            color=YELLOW,
        ).shift(UP * 2.2)

        self.play(Write(formula))
        self.wait(0.5)

        # ===== 左側: 高温（速度ばらつき大）=====
        hot_title = Text("高温（冷却前）", font_size=24, color=HOT_COLOR)
        hot_title.shift(LEFT * 3.5 + UP * 0.8)

        # 広い速度分布
        hot_axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 1, 0.5],
            x_length=3,
            y_length=1.5,
            axis_config={"include_tip": False},
        ).shift(LEFT * 3.5)

        hot_curve = hot_axes.plot(
            lambda v: 0.8 * np.exp(-((v - 2.5) ** 2) / 2),
            x_range=[0, 5],
            color=HOT_COLOR,
            stroke_width=3,
        )

        hot_v_label = MathTex("v", font_size=24).next_to(hot_axes, DOWN, buff=0.1)

        # 結果: 波長がばらつく
        hot_result = Text("→ 波長がばらつく", font_size=20, color=HOT_COLOR)
        hot_result.next_to(hot_axes, DOWN, buff=0.5)

        # ぼやけた波
        hot_waves = VGroup()
        for offset in [-0.15, 0, 0.15]:
            wave = FunctionGraph(
                lambda x, off=offset: 0.15 * np.sin(2 * np.pi * x / (0.8 + off * 2)),
                x_range=[0, 3],
                color=HOT_COLOR,
                stroke_width=2,
                stroke_opacity=0.5,
            ).shift(LEFT * 3.5 + DOWN * 2.5 + UP * offset)
            hot_waves.add(wave)

        hot_wave_label = Text("干渉縞がぼやける", font_size=18, color=HOT_COLOR)
        hot_wave_label.next_to(hot_waves, DOWN, buff=0.2)

        # ===== 右側: 低温（速度ばらつき小）=====
        cold_title = Text("低温（冷却後）", font_size=24, color=COLD_COLOR)
        cold_title.shift(RIGHT * 3.5 + UP * 0.8)

        # 狭い速度分布
        cold_axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 1, 0.5],
            x_length=3,
            y_length=1.5,
            axis_config={"include_tip": False},
        ).shift(RIGHT * 3.5)

        cold_curve = cold_axes.plot(
            lambda v: 0.95 * np.exp(-((v - 2.5) ** 2) / 0.3),
            x_range=[0, 5],
            color=COLD_COLOR,
            stroke_width=3,
        )

        cold_v_label = MathTex("v", font_size=24).next_to(cold_axes, DOWN, buff=0.1)

        # 結果: 波長が揃う
        cold_result = Text("→ 波長が揃う", font_size=20, color=COLD_COLOR)
        cold_result.next_to(cold_axes, DOWN, buff=0.5)

        # くっきりした波
        cold_wave = FunctionGraph(
            lambda x: 0.2 * np.sin(2 * np.pi * x / 0.8),
            x_range=[0, 3],
            color=COLD_COLOR,
            stroke_width=3,
        ).shift(RIGHT * 3.5 + DOWN * 2.5)

        cold_wave_label = Text("干渉縞がくっきり", font_size=18, color=COLD_COLOR)
        cold_wave_label.next_to(cold_wave, DOWN, buff=0.2)

        # 矢印
        arrow = Arrow(LEFT * 0.8, RIGHT * 0.8, color=YELLOW, stroke_width=4)
        arrow_label = Text("冷却", font_size=24, color=YELLOW).next_to(arrow, UP, buff=0.1)

        # アニメーション
        self.play(Write(hot_title), Write(cold_title))
        self.play(
            Create(hot_axes), Create(cold_axes),
            Write(hot_v_label), Write(cold_v_label),
        )
        self.play(Create(hot_curve), Create(cold_curve))
        self.play(Write(hot_result), Write(cold_result))
        self.wait(0.5)

        self.play(GrowArrow(arrow), Write(arrow_label))
        self.wait(0.5)

        self.play(Create(hot_waves), Create(cold_wave))
        self.play(Write(hot_wave_label), Write(cold_wave_label))
        self.wait(2)

        # フェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects])
