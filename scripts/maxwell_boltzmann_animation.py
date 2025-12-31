"""
Maxwell-Boltzmann分布の温度依存性アニメーション

温度が低くなるにつれて速度分布が狭くなる様子を示す

使用方法:
    manim -pql maxwell_boltzmann_animation.py MaxwellBoltzmannCooling
    manim -pqh maxwell_boltzmann_animation.py MaxwellBoltzmannCooling  # 高画質
"""

from manim import *
import numpy as np


class MaxwellBoltzmannCooling(Scene):
    """温度低下に伴うMaxwell-Boltzmann分布の変化"""

    def construct(self):
        # 定数（適当にスケール）
        m = 1.0  # 質量（任意単位）
        k_B = 1.0  # ボルツマン定数（任意単位）

        # 軸の作成
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 1.5, 0.5],
            x_length=10,
            y_length=5,
            axis_config={
                "color": WHITE,
                "include_tip": True,
                "tip_length": 0.2,
            },
        )

        # 軸ラベル
        x_label = axes.get_x_axis_label(
            MathTex("v", font_size=36), edge=RIGHT, direction=RIGHT
        )
        y_label = axes.get_y_axis_label(
            MathTex("f(v)", font_size=36), edge=UP, direction=UP
        )

        # タイトル
        title = Text("Maxwell-Boltzmann 速度分布", font_size=32).to_edge(UP)

        # Maxwell-Boltzmann分布関数（1次元簡略版）
        def maxwell_boltzmann(v, T):
            if T <= 0:
                return 0
            # f(v) ∝ v² exp(-mv²/(2k_B T))
            # 正規化係数を調整して見やすくする
            prefactor = (m / (k_B * T)) ** 1.5
            return prefactor * v**2 * np.exp(-m * v**2 / (2 * k_B * T))

        # 初期温度
        T_start = 2.0
        T_end = 0.3

        # 温度トラッカー
        T_tracker = ValueTracker(T_start)

        # 温度表示
        temp_label = always_redraw(
            lambda: MathTex(
                f"T = {T_tracker.get_value():.2f}",
                font_size=42,
                color=self.get_temp_color(T_tracker.get_value(), T_start, T_end),
            ).to_corner(UR)
        )

        # 分布曲線（動的に更新）
        distribution = always_redraw(
            lambda: axes.plot(
                lambda v: maxwell_boltzmann(v, T_tracker.get_value()),
                x_range=[0.01, 5],
                color=self.get_temp_color(T_tracker.get_value(), T_start, T_end),
                stroke_width=3,
            )
        )

        # 面積（分布の下）
        area = always_redraw(
            lambda: axes.get_area(
                axes.plot(
                    lambda v: maxwell_boltzmann(v, T_tracker.get_value()),
                    x_range=[0.01, 5],
                ),
                x_range=[0.01, 5],
                color=self.get_temp_color(T_tracker.get_value(), T_start, T_end),
                opacity=0.3,
            )
        )

        # アニメーション開始
        self.play(Write(title))
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(Create(distribution), FadeIn(area), Write(temp_label))
        self.wait(1)

        # 冷却アニメーション（温度を下げる）
        self.play(
            T_tracker.animate.set_value(T_end),
            run_time=5,
            rate_func=smooth,
        )
        self.wait(1)

        # 説明テキスト
        explanation = Text(
            "温度が下がると速度分布が狭くなる",
            font_size=28,
            color=YELLOW,
        ).next_to(axes, DOWN, buff=0.5)

        self.play(Write(explanation))
        self.wait(2)

        # フェードアウト
        self.play(
            FadeOut(distribution),
            FadeOut(area),
            FadeOut(temp_label),
            FadeOut(explanation),
            FadeOut(title),
            FadeOut(axes),
            FadeOut(x_label),
            FadeOut(y_label),
        )

    def get_temp_color(self, T, T_max, T_min):
        """温度に応じた色を返す（熱い=赤、冷たい=青）"""
        ratio = (T - T_min) / (T_max - T_min)
        ratio = max(0, min(1, ratio))  # 0-1にクランプ
        return interpolate_color(BLUE, RED, ratio)


class MaxwellBoltzmannComparison(Scene):
    """複数の温度でのMaxwell-Boltzmann分布を比較"""

    def construct(self):
        m = 1.0
        k_B = 1.0

        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 1.5, 0.5],
            x_length=10,
            y_length=5,
            axis_config={"color": WHITE, "include_tip": True},
        )

        x_label = axes.get_x_axis_label(MathTex("v"), edge=RIGHT)
        y_label = axes.get_y_axis_label(MathTex("f(v)"), edge=UP)

        title = Text("温度による速度分布の変化", font_size=32).to_edge(UP)

        def maxwell_boltzmann(v, T):
            if T <= 0:
                return 0
            prefactor = (m / (k_B * T)) ** 1.5
            return prefactor * v**2 * np.exp(-m * v**2 / (2 * k_B * T))

        # 3つの温度
        temperatures = [2.0, 1.0, 0.4]
        colors = [RED, ORANGE, BLUE]
        labels = ["高温", "中温", "低温"]

        self.play(Write(title), Create(axes), Write(x_label), Write(y_label))

        curves = []
        legend_items = []

        for T, color, label in zip(temperatures, colors, labels):
            curve = axes.plot(
                lambda v, T=T: maxwell_boltzmann(v, T),
                x_range=[0.01, 5],
                color=color,
                stroke_width=3,
            )
            curves.append(curve)

            # 凡例アイテム
            legend_line = Line(ORIGIN, RIGHT * 0.5, color=color, stroke_width=3)
            legend_text = Text(f"{label} (T={T})", font_size=20, color=color)
            legend_item = VGroup(legend_line, legend_text).arrange(RIGHT, buff=0.2)
            legend_items.append(legend_item)

        # 凡例を配置
        legend = VGroup(*legend_items).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        legend.to_corner(UR).shift(DOWN * 0.5)

        # 順番に表示
        for curve, legend_item in zip(curves, legend_items):
            self.play(Create(curve), Write(legend_item), run_time=1)

        self.wait(2)

        # ハイライト説明
        arrow = Arrow(
            axes.c2p(0.5, 1.2),
            axes.c2p(0.8, 0.8),
            color=YELLOW,
            buff=0.1,
        )
        note = Text("低温ほど\n分布が鋭い", font_size=24, color=YELLOW).next_to(
            arrow, UP
        )

        self.play(GrowArrow(arrow), Write(note))
        self.wait(2)


class Rb87LaserCooling(Scene):
    """⁸⁷Rbの100μKから5μKまでの冷却アニメーション（絶対速度軸）"""

    def construct(self):
        # 物理定数
        m_Rb87 = 87 * 1.66054e-27  # ⁸⁷Rbの質量 [kg]
        k_B = 1.38065e-23  # ボルツマン定数 [J/K]

        # 温度範囲
        T_start = 100e-6  # 100 μK
        T_end = 5e-6  # 5 μK

        # 最確速度 v_p = sqrt(2 k_B T / m)
        def most_probable_velocity(T):
            return np.sqrt(2 * k_B * T / m_Rb87)

        # Maxwell-Boltzmann分布（実速度、cm/s単位）
        def maxwell_boltzmann(v_cm, T):
            """v_cm: 速度 [cm/s], T: 温度 [K]"""
            v = v_cm / 100  # m/s に変換
            if T <= 0 or v <= 0:
                return 0
            prefactor = 4 * np.pi * (m_Rb87 / (2 * np.pi * k_B * T)) ** 1.5
            return prefactor * v**2 * np.exp(-m_Rb87 * v**2 / (2 * k_B * T))

        # 初期温度での最確速度 [cm/s]
        v_p_start = most_probable_velocity(T_start) * 100  # cm/s
        v_max = v_p_start * 4  # 軸の最大値

        # タイトル
        title = VGroup(
            Text("⁸⁷Rb原子の速度分布", font_size=32),
            Text("レーザー冷却: 100 μK → 5 μK", font_size=24, color=YELLOW),
        ).arrange(DOWN, buff=0.2).to_edge(UP)

        # 軸（絶対速度 cm/s）
        axes = Axes(
            x_range=[0, v_max, v_max / 4],
            y_range=[0, 1.2, 0.3],
            x_length=9,
            y_length=4.5,
            axis_config={"color": WHITE, "include_tip": True},
        ).shift(DOWN * 0.3)

        x_label = Text("v [cm/s]", font_size=24).next_to(axes.x_axis, RIGHT)
        y_label = MathTex(r"f(v)", font_size=28).next_to(axes.y_axis, UP)

        # 温度トラッカー（対数スケール）
        log_T_tracker = ValueTracker(np.log10(T_start))

        def get_current_T():
            return 10 ** log_T_tracker.get_value()

        # 温度表示
        temp_label = always_redraw(
            lambda: Text(
                f"T = {get_current_T()*1e6:.1f} μK",
                font_size=36,
                color=self.get_temp_color(get_current_T(), T_start, T_end),
            ).to_corner(UR)
        )

        # 最確速度の表示
        velocity_label = always_redraw(
            lambda: Text(
                f"v_p = {most_probable_velocity(get_current_T())*100:.2f} cm/s",
                font_size=28,
                color=GRAY,
            ).next_to(temp_label, DOWN, aligned_edge=RIGHT)
        )

        # 正規化用のピーク値（初期温度で計算、固定）
        peak_at_start = maxwell_boltzmann(v_p_start, T_start)

        # 分布曲線（動的に更新）
        distribution = always_redraw(
            lambda: axes.plot(
                lambda v: maxwell_boltzmann(v, get_current_T()) / peak_at_start,
                x_range=[0.1, v_max],
                color=self.get_temp_color(get_current_T(), T_start, T_end),
                stroke_width=3,
            )
        )

        # 面積
        area = always_redraw(
            lambda: axes.get_area(
                axes.plot(
                    lambda v: maxwell_boltzmann(v, get_current_T()) / peak_at_start,
                    x_range=[0.1, v_max],
                ),
                x_range=[0.1, v_max],
                color=self.get_temp_color(get_current_T(), T_start, T_end),
                opacity=0.3,
            )
        )

        # アニメーション
        self.play(Write(title))
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(Create(distribution), FadeIn(area))
        self.play(Write(temp_label), Write(velocity_label))
        self.wait(1)

        # 対数スケールで温度を下げる（100μK → 5μK）
        self.play(
            log_T_tracker.animate.set_value(np.log10(T_end)),
            run_time=6,
            rate_func=smooth,
        )
        self.wait(1)

        # 最終説明
        explanation = VGroup(
            Text("温度が下がると:", font_size=24),
            Text("• 速度分布の幅が狭くなる", font_size=22, color=BLUE),
            Text("• ピークが高く鋭くなる", font_size=22, color=BLUE),
            Text("• 波長が揃い、干渉計に使える", font_size=22, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        explanation.next_to(axes, DOWN, buff=0.4)

        self.play(Write(explanation))
        self.wait(3)

    def get_temp_color(self, T, T_max, T_min):
        """温度に応じた色（対数スケール）"""
        if T <= 0 or T_min <= 0:
            return BLUE
        log_ratio = (np.log10(T) - np.log10(T_min)) / (
            np.log10(T_max) - np.log10(T_min)
        )
        log_ratio = max(0, min(1, log_ratio))
        return interpolate_color(BLUE, RED, log_ratio)


class Rb87ThreeTemperatures(Scene):
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


class Rb87AbsoluteScale(Scene):
    """⁸⁷Rbの実際の速度スケールでの分布変化"""

    def construct(self):
        # 物理定数
        m_Rb87 = 87 * 1.66054e-27
        k_B = 1.38065e-23

        # Maxwell-Boltzmann分布（実速度）
        def maxwell_boltzmann_real(v, T):
            if T <= 0 or v <= 0:
                return 0
            prefactor = 4 * np.pi * (m_Rb87 / (2 * np.pi * k_B * T)) ** 1.5
            return prefactor * v**2 * np.exp(-m_Rb87 * v**2 / (2 * k_B * T))

        # 3つの温度での比較
        temperatures = [
            (300, "常温 (300 K)", RED),
            (1e-3, "1 mK", ORANGE),
            (5e-6, "5 μK", BLUE),
        ]

        title = Text("⁸⁷Rb 速度分布の比較", font_size=36).to_edge(UP)
        self.play(Write(title))

        # 各温度での分布を順番に表示
        info_text = None

        for i, (T, label, color) in enumerate(temperatures):
            v_p = np.sqrt(2 * k_B * T / m_Rb87)
            v_max = v_p * 4

            # 軸を温度に応じて作成
            if T >= 1:
                x_label_text = "v [m/s]"
                v_scale = 1
            elif T >= 1e-3:
                x_label_text = "v [cm/s]"
                v_scale = 100
            else:
                x_label_text = "v [mm/s]"
                v_scale = 1000

            axes = Axes(
                x_range=[0, v_max * v_scale, v_max * v_scale / 4],
                y_range=[0, 1.2, 0.3],
                x_length=8,
                y_length=4,
                axis_config={"color": WHITE, "include_tip": True},
            ).shift(DOWN * 0.5)

            x_label = Text(x_label_text, font_size=24).next_to(axes.x_axis, RIGHT)
            y_label = MathTex(r"f(v)", font_size=24).next_to(axes.y_axis, UP)

            # 正規化した分布（ピークを1に）
            peak_value = maxwell_boltzmann_real(v_p, T)

            def mb_normalized(v_scaled, T=T, v_scale=v_scale, peak=peak_value):
                v = v_scaled / v_scale
                return maxwell_boltzmann_real(v, T) / peak

            curve = axes.plot(
                mb_normalized,
                x_range=[0.01, v_max * v_scale],
                color=color,
                stroke_width=3,
            )

            area = axes.get_area(
                curve,
                x_range=[0.01, v_max * v_scale],
                color=color,
                opacity=0.3,
            )

            # 情報テキスト
            new_info = VGroup(
                Text(label, font_size=32, color=color),
                Text(f"最確速度: {v_p*v_scale:.2f} {x_label_text.split()[0][2:]}", font_size=24),
            ).arrange(DOWN).to_corner(UR)

            if i == 0:
                self.play(Create(axes), Write(x_label), Write(y_label))
                self.play(Create(curve), FadeIn(area), Write(new_info))
            else:
                self.play(
                    FadeOut(info_text),
                    ReplacementTransform(axes, axes),
                    run_time=0.5,
                )
                self.play(
                    Create(curve),
                    FadeIn(area),
                    Write(new_info),
                )

            info_text = new_info
            self.wait(2)

            if i < len(temperatures) - 1:
                self.play(FadeOut(curve), FadeOut(area), FadeOut(axes), FadeOut(x_label), FadeOut(y_label))

        self.wait(2)


class DeBroglieWavelength(Scene):
    """温度とド・ブロイ波長の関係"""

    def construct(self):
        # タイトル
        title = Text("温度と熱的ド・ブロイ波長", font_size=36).to_edge(UP)

        # 数式
        formula = MathTex(
            r"\lambda_{\text{th}} \sim \frac{h}{\sqrt{m k_B T}}",
            font_size=48,
        ).shift(UP * 1)

        # 説明
        explanations = VGroup(
            MathTex(r"T \uparrow", font_size=36, color=RED),
            MathTex(r"\Rightarrow", font_size=36),
            MathTex(r"\lambda_{\text{th}} \downarrow", font_size=36, color=RED),
            Text("波長が短い", font_size=24, color=RED),
        ).arrange(RIGHT, buff=0.3)

        explanations2 = VGroup(
            MathTex(r"T \downarrow", font_size=36, color=BLUE),
            MathTex(r"\Rightarrow", font_size=36),
            MathTex(r"\lambda_{\text{th}} \uparrow", font_size=36, color=BLUE),
            Text("波長が長い", font_size=24, color=BLUE),
        ).arrange(RIGHT, buff=0.3)

        VGroup(explanations, explanations2).arrange(DOWN, buff=0.5).shift(DOWN * 1)

        # 結論
        conclusion = Text(
            "冷却すると波長が揃い、干渉しやすくなる",
            font_size=28,
            color=YELLOW,
        ).to_edge(DOWN, buff=1)

        # アニメーション
        self.play(Write(title))
        self.play(Write(formula))
        self.wait(1)
        self.play(Write(explanations))
        self.play(Write(explanations2))
        self.wait(1)
        self.play(Write(conclusion))
        self.wait(2)
