"""
Maxwell-Boltzmann分布の温度比較アニメーション

100μK, 50μK, 5μKの分布を重ね合わせて比較表示

使用方法:
    manim -pql mb_temperature_comparison.py TemperatureComparison
    manim -pqh mb_temperature_comparison.py TemperatureComparison  # 高画質
"""

from manim import *
import numpy as np


class TemperatureComparison(Scene):
    """⁸⁷Rbの100μK, 50μK, 5μKでの分布を重ね合わせ表示"""

    def construct(self):
        # 物理定数
        m_Rb87 = 87 * 1.66054e-27  # ⁸⁷Rbの質量 [kg]
        k_B = 1.38065e-23  # ボルツマン定数 [J/K]

        # 最確速度 v_p = sqrt(2 k_B T / m)
        def most_probable_velocity(T):
            return np.sqrt(2 * k_B * T / m_Rb87)

        # Maxwell-Boltzmann分布（cm/s単位）
        def maxwell_boltzmann(v_cm, T):
            v = v_cm / 100  # m/s に変換
            if T <= 0 or v <= 0:
                return 0
            prefactor = 4 * np.pi * (m_Rb87 / (2 * np.pi * k_B * T)) ** 1.5
            return prefactor * v**2 * np.exp(-m_Rb87 * v**2 / (2 * k_B * T))

        # 3つの温度設定
        temperatures = [
            (100e-6, "100 μK", RED),
            (50e-6, "50 μK", ORANGE),
            (5e-6, "5 μK", BLUE),
        ]

        # 軸の範囲は100μKに合わせる
        T_max = 100e-6
        v_p_max = most_probable_velocity(T_max) * 100  # cm/s
        v_max = v_p_max * 4

        # 正規化用のピーク値（100μKで計算）
        peak_100uK = maxwell_boltzmann(v_p_max, T_max)

        # タイトル
        title = Text("⁸⁷Rb原子の速度分布（温度比較）", font_size=32).to_edge(UP)

        # 軸
        axes = Axes(
            x_range=[0, v_max, v_max / 4],
            y_range=[0, 5, 1],  # 5μKはピークが高くなるので余裕を持たせる
            x_length=9,
            y_length=4.5,
            axis_config={"color": WHITE, "include_tip": True},
        ).shift(DOWN * 0.3)

        x_label = Text("v [cm/s]", font_size=24).next_to(axes.x_axis, RIGHT)
        y_label = MathTex(r"f(v)", font_size=28).next_to(axes.y_axis, UP)

        # アニメーション開始
        self.play(Write(title))
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(0.5)

        # 凡例用のグループ
        legend_items = []
        curves = []
        areas = []

        # 各温度の分布を順番に追加
        for T, label, color in temperatures:
            # 分布曲線
            curve = axes.plot(
                lambda v, T=T: maxwell_boltzmann(v, T) / peak_100uK,
                x_range=[0.1, v_max],
                color=color,
                stroke_width=3,
            )

            # 面積
            area = axes.get_area(
                curve,
                x_range=[0.1, v_max],
                color=color,
                opacity=0.2,
            )

            # 凡例アイテム
            legend_line = Line(ORIGIN, RIGHT * 0.5, color=color, stroke_width=3)
            legend_text = Text(label, font_size=20, color=color)
            legend_item = VGroup(legend_line, legend_text).arrange(RIGHT, buff=0.2)
            legend_items.append(legend_item)

            curves.append(curve)
            areas.append(area)

            # 分布を追加
            self.play(Create(curve), FadeIn(area), run_time=1)
            self.wait(0.3)

        # 凡例を配置
        legend = VGroup(*legend_items).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        legend.to_corner(UR).shift(DOWN * 0.5)
        self.play(Write(legend))
        self.wait(1)

        # 説明テキスト
        explanation = VGroup(
            Text("温度が下がると:", font_size=24),
            Text("• 分布の幅が狭くなる", font_size=22, color=BLUE),
            Text("• ピークが高くなる", font_size=22, color=BLUE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        explanation.next_to(axes, DOWN, buff=0.4)

        self.play(Write(explanation))
        self.wait(3)
