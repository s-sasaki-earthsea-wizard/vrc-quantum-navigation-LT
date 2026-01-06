"""
MEMSと原子干渉計の精度比較アニメーション

10時間飛行後の誤差：
- MEMS: 6.5km
- 原子干渉計: 65cm

使用方法:
    manim -pql precision_comparison_animation.py PrecisionComparison
    manim -pqh precision_comparison_animation.py PrecisionComparison  # 高画質
"""

from manim import *
import numpy as np


class PrecisionComparison(Scene):
    """MEMSと原子干渉計の精度差を視覚的に比較"""

    def construct(self):
        MEMS_COLOR = RED
        ATOMIC_COLOR = BLUE

        # タイトル
        title = Text("加速度計の精度比較", font_size=36, color=WHITE).to_edge(UP)
        self.play(Write(title))

        # サブタイトル
        subtitle = Text("10時間飛行後の位置誤差", font_size=28, color=YELLOW)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(Write(subtitle))
        self.wait(0.5)

        # ===== MEMS側 =====
        mems_label = Text("MEMS加速度計", font_size=24, color=MEMS_COLOR)
        mems_label.shift(LEFT * 3.5 + UP * 1)

        mems_error = Text("誤差: 6.5 km", font_size=32, color=MEMS_COLOR)
        mems_error.next_to(mems_label, DOWN, buff=0.3)

        # MEMSの誤差を棒グラフで表現（大きいので画面幅いっぱい）
        mems_bar = Rectangle(
            width=6, height=0.8,
            fill_color=MEMS_COLOR, fill_opacity=0.7,
            stroke_color=MEMS_COLOR, stroke_width=2,
        )
        mems_bar.next_to(mems_error, DOWN, buff=0.4)

        mems_value = Text("6.5 km", font_size=20, color=WHITE)
        mems_value.move_to(mems_bar.get_center())

        # ===== 原子干渉計側 =====
        atomic_label = Text("原子干渉計", font_size=24, color=ATOMIC_COLOR)
        atomic_label.shift(LEFT * 3.5 + DOWN * 1.5)

        atomic_error = Text("誤差: 65 cm", font_size=32, color=ATOMIC_COLOR)
        atomic_error.next_to(atomic_label, DOWN, buff=0.3)

        # 原子干渉計の誤差を棒グラフで表現（6.5km : 0.65m = 10000 : 1）
        # 比率を視覚化: 6.5km / 65cm = 10000倍
        atomic_bar = Rectangle(
            width=0.0006,  # 6 / 10000 = 0.0006 だが見えないので最小サイズに
            height=0.8,
            fill_color=ATOMIC_COLOR, fill_opacity=0.7,
            stroke_color=ATOMIC_COLOR, stroke_width=2,
        )
        # 実際には見えないので、視覚的に表現
        atomic_bar_visual = Rectangle(
            width=0.06, height=0.8,
            fill_color=ATOMIC_COLOR, fill_opacity=0.7,
            stroke_color=ATOMIC_COLOR, stroke_width=2,
        )
        atomic_bar_visual.next_to(atomic_error, DOWN, buff=0.4)
        atomic_bar_visual.align_to(mems_bar, LEFT)

        atomic_value = Text("65 cm", font_size=16, color=WHITE)
        atomic_value.next_to(atomic_bar_visual, RIGHT, buff=0.2)

        # アニメーション
        self.play(Write(mems_label), Write(atomic_label))
        self.play(Write(mems_error), Write(atomic_error))
        self.wait(0.5)

        self.play(
            GrowFromEdge(mems_bar, LEFT),
            Write(mems_value),
        )
        self.wait(0.3)

        self.play(
            GrowFromEdge(atomic_bar_visual, LEFT),
            Write(atomic_value),
        )
        self.wait(1)

        # 比率の強調
        ratio_text = MathTex(
            r"\frac{6.5 \text{ km}}{65 \text{ cm}} = 10000 \times",
            font_size=40,
            color=YELLOW,
        )
        ratio_text.to_edge(RIGHT, buff=1).shift(UP * 0.5)

        ratio_box = SurroundingRectangle(ratio_text, color=YELLOW, buff=0.2)

        self.play(Write(ratio_text), Create(ratio_box))
        self.wait(1)

        # 結論
        conclusion = Text(
            "原子干渉計は1万倍高精度",
            font_size=28,
            color=GREEN,
        ).to_edge(DOWN, buff=0.5)

        self.play(Write(conclusion))
        self.wait(2)

        # フェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class PrecisionComparisonVisual(Scene):
    """スケール比較による視覚化"""

    def construct(self):
        MEMS_COLOR = RED
        ATOMIC_COLOR = BLUE

        # タイトル
        title = Text("誤差のスケール比較", font_size=36, color=WHITE).to_edge(UP)
        self.play(Write(title))

        subtitle = Text("10時間飛行後", font_size=24, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.2)
        self.play(Write(subtitle))

        # ===== MEMSの誤差: 6.5km =====
        # 大きな円で6.5kmを表現
        mems_circle = Circle(
            radius=2.5,
            fill_color=MEMS_COLOR, fill_opacity=0.3,
            stroke_color=MEMS_COLOR, stroke_width=3,
        )
        mems_circle.shift(LEFT * 0.5)

        mems_label = Text("MEMS", font_size=24, color=MEMS_COLOR)
        mems_label.next_to(mems_circle, UP, buff=0.2)

        mems_value = Text("6.5 km", font_size=28, color=MEMS_COLOR)
        mems_value.move_to(mems_circle.get_center() + UP * 0.5)

        # ===== 原子干渉計の誤差: 65cm =====
        # 小さな点で65cmを表現 (1/10000スケール)
        # 2.5 / 10000 = 0.00025 だと見えないので最小表示
        atomic_dot = Dot(
            radius=0.05,
            color=ATOMIC_COLOR,
        )
        atomic_dot.move_to(mems_circle.get_center())

        atomic_label = Text("原子干渉計", font_size=20, color=ATOMIC_COLOR)
        atomic_label.next_to(atomic_dot, DOWN, buff=0.5)

        atomic_value = Text("65 cm", font_size=20, color=ATOMIC_COLOR)
        atomic_value.next_to(atomic_label, DOWN, buff=0.1)

        # 矢印で点を指す
        arrow = Arrow(
            atomic_label.get_top() + UP * 0.1,
            atomic_dot.get_center() + DOWN * 0.15,
            color=ATOMIC_COLOR,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.3,
        )

        # アニメーション
        self.play(GrowFromCenter(mems_circle), Write(mems_label))
        self.play(Write(mems_value))
        self.wait(0.5)

        self.play(FadeIn(atomic_dot, scale=3))
        self.play(Write(atomic_label), Write(atomic_value), GrowArrow(arrow))
        self.wait(1)

        # 説明テキスト
        explanation = VGroup(
            Text("同じスケールで描くと", font_size=22, color=WHITE),
            Text("原子干渉計の誤差は点にしか見えない", font_size=22, color=YELLOW),
        ).arrange(DOWN, buff=0.2)
        explanation.to_edge(DOWN, buff=0.5)

        self.play(Write(explanation))
        self.wait(2)

        # フェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class PrecisionErrorGrowth(Scene):
    """時間経過による誤差蓄積の比較"""

    def construct(self):
        MEMS_COLOR = RED
        ATOMIC_COLOR = BLUE

        # タイトル
        title = Text("誤差の時間発展", font_size=36, color=WHITE).to_edge(UP)
        self.play(Write(title))

        # 数式: δx ~ (1/2)δa·t²
        formula = MathTex(
            r"\delta x \approx \frac{1}{2} \delta a \cdot t^2",
            font_size=36,
            color=YELLOW,
        )
        formula.next_to(title, DOWN, buff=0.3)
        self.play(Write(formula))

        # 軸の設定
        axes = Axes(
            x_range=[0, 10.5, 2],
            y_range=[0, 7, 1],
            x_length=8,
            y_length=4,
            axis_config={"include_tip": True, "tip_length": 0.2},
            x_axis_config={"numbers_to_include": [0, 2, 4, 6, 8, 10]},
            y_axis_config={"numbers_to_include": [0, 2, 4, 6]},
        ).shift(DOWN * 0.5)

        x_label = Text("時間 (時間)", font_size=20).next_to(axes.x_axis, DOWN, buff=0.3)
        y_label = Text("誤差 (km)", font_size=20).next_to(axes.y_axis, LEFT, buff=0.3).rotate(90 * DEGREES)

        self.play(Create(axes), Write(x_label), Write(y_label))

        # MEMSの誤差曲線 (t²に比例、10時間で6.5km)
        # δx = k * t² where k = 6.5 / 100 = 0.065
        mems_curve = axes.plot(
            lambda t: 0.065 * t ** 2,
            x_range=[0, 10],
            color=MEMS_COLOR,
            stroke_width=3,
        )

        mems_label = Text("MEMS", font_size=20, color=MEMS_COLOR)
        mems_label.next_to(mems_curve.get_end(), RIGHT, buff=0.2)

        # 原子干渉計の誤差曲線 (10時間で0.00065km = 65cm)
        # ほぼ0に見えるので、誇張して表示
        atomic_curve = axes.plot(
            lambda t: 0.0000065 * t ** 2,  # 実際の値
            x_range=[0, 10],
            color=ATOMIC_COLOR,
            stroke_width=3,
        )

        atomic_label = Text("原子干渉計", font_size=20, color=ATOMIC_COLOR)
        atomic_label.next_to(axes.c2p(10, 0.5), RIGHT, buff=0.2)

        # アニメーション
        self.play(Create(mems_curve), Write(mems_label), run_time=2)
        self.wait(0.5)

        self.play(Create(atomic_curve), Write(atomic_label), run_time=2)
        self.wait(0.5)

        # 10時間地点にマーカー
        mems_point = Dot(axes.c2p(10, 6.5), color=MEMS_COLOR)
        mems_value = Text("6.5 km", font_size=18, color=MEMS_COLOR)
        mems_value.next_to(mems_point, UP, buff=0.1)

        atomic_point = Dot(axes.c2p(10, 0), color=ATOMIC_COLOR)
        atomic_value = Text("65 cm", font_size=18, color=ATOMIC_COLOR)
        atomic_value.next_to(atomic_point, DOWN, buff=0.1)

        self.play(
            FadeIn(mems_point), Write(mems_value),
            FadeIn(atomic_point), Write(atomic_value),
        )
        self.wait(1)

        # 精度の説明
        mems_prec_label = Text("MEMS: ", font_size=20, color=MEMS_COLOR)
        mems_prec_value = MathTex(r"\delta a \approx 10^{-5}", font_size=24, color=MEMS_COLOR)
        mems_prec_unit = Text(" m/s²", font_size=20, color=MEMS_COLOR)
        mems_prec_line = VGroup(mems_prec_label, mems_prec_value, mems_prec_unit).arrange(RIGHT, buff=0.1)

        atomic_prec_label = Text("原子干渉計: ", font_size=20, color=ATOMIC_COLOR)
        atomic_prec_value = MathTex(r"\delta a \approx 10^{-9}", font_size=24, color=ATOMIC_COLOR)
        atomic_prec_unit = Text(" m/s²", font_size=20, color=ATOMIC_COLOR)
        atomic_prec_line = VGroup(atomic_prec_label, atomic_prec_value, atomic_prec_unit).arrange(RIGHT, buff=0.1)

        precision_text = VGroup(mems_prec_line, atomic_prec_line).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        precision_text.to_edge(RIGHT, buff=0.5).shift(DOWN * 2)

        self.play(Write(precision_text))
        self.wait(2)

        # フェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class PrecisionComparisonCombined(Scene):
    """統合版: 精度比較の全体像"""

    def construct(self):
        MEMS_COLOR = RED
        ATOMIC_COLOR = BLUE

        # ===== パート1: イントロ =====
        title = Text("慣性航法の精度比較", font_size=40, color=WHITE)
        self.play(Write(title))
        self.wait(1)

        self.play(title.animate.scale(0.7).to_edge(UP))

        # ===== パート2: 精度の数値 =====
        precision_title = Text("加速度計の精度", font_size=28, color=YELLOW)
        precision_title.next_to(title, DOWN, buff=0.4)

        mems_precision_formula = VGroup(
            MathTex(r"\delta a \approx 10^{-5}", font_size=28, color=MEMS_COLOR),
            Text(" m/s²", font_size=22, color=MEMS_COLOR),
        ).arrange(RIGHT, buff=0.1)
        mems_precision = VGroup(
            Text("MEMS加速度計", font_size=24, color=MEMS_COLOR),
            mems_precision_formula,
        ).arrange(DOWN, buff=0.1)

        atomic_precision_formula = VGroup(
            MathTex(r"\delta a \approx 10^{-9}", font_size=28, color=ATOMIC_COLOR),
            Text(" m/s²", font_size=22, color=ATOMIC_COLOR),
        ).arrange(RIGHT, buff=0.1)
        atomic_precision = VGroup(
            Text("原子干渉計", font_size=24, color=ATOMIC_COLOR),
            atomic_precision_formula,
        ).arrange(DOWN, buff=0.1)

        precision_group = VGroup(mems_precision, atomic_precision).arrange(RIGHT, buff=2)
        precision_group.next_to(precision_title, DOWN, buff=0.5)

        self.play(Write(precision_title))
        self.play(Write(mems_precision), Write(atomic_precision))
        self.wait(1)

        # 精度差
        ratio = VGroup(
            MathTex(r"10000 \times", font_size=32, color=GREEN),
            Text(" 高精度", font_size=26, color=GREEN),
        ).arrange(RIGHT, buff=0.1)
        ratio.next_to(precision_group, DOWN, buff=0.4)
        self.play(Write(ratio))
        self.wait(1)

        # ===== パート3: 10時間後の誤差 =====
        self.play(
            FadeOut(precision_title), FadeOut(mems_precision),
            FadeOut(atomic_precision), FadeOut(ratio),
        )

        error_title = Text("10時間飛行後の位置誤差", font_size=28, color=YELLOW)
        error_title.next_to(title, DOWN, buff=0.4)
        self.play(Write(error_title))

        # バーチャート形式
        # MEMSバー
        mems_bar_group = VGroup()
        mems_bar = Rectangle(
            width=5, height=0.6,
            fill_color=MEMS_COLOR, fill_opacity=0.7,
            stroke_color=MEMS_COLOR, stroke_width=2,
        )
        mems_bar_label = Text("MEMS", font_size=20, color=MEMS_COLOR)
        mems_bar_label.next_to(mems_bar, LEFT, buff=0.3)
        mems_bar_value = Text("6.5 km", font_size=20, color=WHITE)
        mems_bar_value.move_to(mems_bar.get_center())
        mems_bar_group.add(mems_bar_label, mems_bar, mems_bar_value)
        mems_bar_group.shift(UP * 0.3)

        # 原子干渉計バー
        atomic_bar_group = VGroup()
        atomic_bar = Rectangle(
            width=0.05, height=0.6,
            fill_color=ATOMIC_COLOR, fill_opacity=0.7,
            stroke_color=ATOMIC_COLOR, stroke_width=2,
        )
        atomic_bar_label = Text("原子干渉計", font_size=20, color=ATOMIC_COLOR)
        atomic_bar_label.next_to(atomic_bar, LEFT, buff=0.3)
        atomic_bar.align_to(mems_bar, LEFT)
        atomic_bar_label.align_to(mems_bar_label, RIGHT)
        atomic_bar_value = Text("65 cm", font_size=16, color=ATOMIC_COLOR)
        atomic_bar_value.next_to(atomic_bar, RIGHT, buff=0.2)
        atomic_bar_group.add(atomic_bar_label, atomic_bar, atomic_bar_value)
        atomic_bar_group.shift(DOWN * 0.8)

        self.play(
            GrowFromEdge(mems_bar, LEFT),
            Write(mems_bar_label), Write(mems_bar_value),
        )
        self.wait(0.3)

        self.play(
            GrowFromEdge(atomic_bar, LEFT),
            Write(atomic_bar_label), Write(atomic_bar_value),
        )
        self.wait(1)

        # ===== パート4: 結論 =====
        conclusion_box = VGroup(
            Text("原子干渉計により", font_size=26, color=WHITE),
            Text("GPS不要の高精度航法が可能に", font_size=26, color=GREEN),
        ).arrange(DOWN, buff=0.2)
        conclusion_box.to_edge(DOWN, buff=0.6)

        box = SurroundingRectangle(conclusion_box, color=GREEN, buff=0.2)

        self.play(Write(conclusion_box), Create(box))
        self.wait(2)

        # フェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class FundamentalConstantsAdvantage(Scene):
    """原子干渉計が自然定数を基準にしている利点を図解"""

    def construct(self):
        MEMS_COLOR = RED
        ATOMIC_COLOR = BLUE
        CONSTANT_COLOR = GOLD

        # タイトル
        title = Text("なぜ原子干渉計は高精度なのか？", font_size=36, color=WHITE).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # ===== 左側: MEMS（機械式）=====
        mems_title = Text("MEMS加速度計", font_size=24, color=MEMS_COLOR)
        mems_title.shift(LEFT * 3.5 + UP * 1.8)

        # バネと重りのイラスト
        spring_base = Line(LEFT * 4.5 + UP * 0.8, LEFT * 2.5 + UP * 0.8, color=GRAY, stroke_width=3)
        spring = self._create_spring(LEFT * 3.5 + UP * 0.8, LEFT * 3.5, color=MEMS_COLOR)
        mass = Square(side_length=0.5, color=MEMS_COLOR, fill_opacity=0.7)
        mass.move_to(LEFT * 3.5 + DOWN * 0.25)

        mems_label = Text("機械的な部品", font_size=18, color=MEMS_COLOR)
        mems_label.next_to(mass, DOWN, buff=0.3)

        self.play(Write(mems_title))
        self.play(Create(spring_base), Create(spring), FadeIn(mass), Write(mems_label))
        self.wait(0.5)

        # 問題点: 劣化・変化
        problems = VGroup(
            Text("❌ 温度で特性が変化", font_size=18, color=MEMS_COLOR),
            Text("❌ 経年劣化する", font_size=18, color=MEMS_COLOR),
            Text("❌ 個体差がある", font_size=18, color=MEMS_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        problems.shift(LEFT * 3.5 + DOWN * 2.2)

        self.play(Write(problems), run_time=1.5)
        self.wait(0.5)

        # ===== 右側: 原子干渉計 =====
        atomic_title = Text("原子干渉計", font_size=24, color=ATOMIC_COLOR)
        atomic_title.shift(RIGHT * 3.5 + UP * 1.8)

        # 原子のイラスト
        atom = Circle(radius=0.4, color=ATOMIC_COLOR, fill_opacity=0.7)
        atom.shift(RIGHT * 3.5 + UP * 0.3)

        # 電子軌道
        orbit1 = Ellipse(width=1.2, height=0.4, color=ATOMIC_COLOR, stroke_width=1.5)
        orbit1.move_to(atom.get_center())
        orbit2 = Ellipse(width=1.2, height=0.4, color=ATOMIC_COLOR, stroke_width=1.5)
        orbit2.move_to(atom.get_center()).rotate(60 * DEGREES)
        orbit3 = Ellipse(width=1.2, height=0.4, color=ATOMIC_COLOR, stroke_width=1.5)
        orbit3.move_to(atom.get_center()).rotate(-60 * DEGREES)

        atom_group = VGroup(orbit1, orbit2, orbit3, atom)

        atomic_label = Text("原子の遷移周波数", font_size=18, color=ATOMIC_COLOR)
        atomic_label.next_to(atom_group, DOWN, buff=0.3)

        self.play(Write(atomic_title))
        self.play(FadeIn(atom_group), Write(atomic_label))
        self.wait(0.5)

        # 利点: 自然定数
        advantages = VGroup(
            Text("✓ 普遍的な自然定数", font_size=18, color=GREEN),
            Text("✓ 劣化しない", font_size=18, color=GREEN),
            Text("✓ 宇宙のどこでも同じ", font_size=18, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        advantages.shift(RIGHT * 3.5 + DOWN * 1.5)

        self.play(Write(advantages), run_time=1.5)
        self.wait(1)

        # ===== 下部: 自然定数の強調 =====
        const_title = Text("基準となる自然定数:", font_size=22, color=CONSTANT_COLOR)

        h_sym = MathTex(r"h", font_size=28, color=CONSTANT_COLOR)
        h_text = Text(" プランク定数", font_size=20)
        h_line = VGroup(h_sym, h_text).arrange(RIGHT, buff=0.1)

        c_sym = MathTex(r"c", font_size=28, color=CONSTANT_COLOR)
        c_text = Text(" 光速", font_size=20)
        c_line = VGroup(c_sym, c_text).arrange(RIGHT, buff=0.1)

        nu_sym = MathTex(r"\nu_0", font_size=28, color=CONSTANT_COLOR)
        nu_text = Text(" 原子遷移周波数", font_size=20)
        nu_line = VGroup(nu_sym, nu_text).arrange(RIGHT, buff=0.1)

        constants_box = VGroup(const_title, h_line, c_line, nu_line).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        constants_box.to_edge(DOWN, buff=0.4)

        box = SurroundingRectangle(constants_box, color=CONSTANT_COLOR, buff=0.2)

        self.play(Write(constants_box), Create(box), run_time=1.5)
        self.wait(2)

        # フェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def _create_spring(self, start, end, color, coils=5):
        """バネを作成"""
        points = []
        start_point = np.array([start[0], start[1], 0])
        end_point = np.array([end[0], end[1], 0])

        total_length = np.linalg.norm(end_point - start_point)
        direction = (end_point - start_point) / total_length

        # 垂直方向
        perp = np.array([-direction[1], direction[0], 0])

        for i in range(coils * 4 + 1):
            t = i / (coils * 4)
            pos = start_point + direction * total_length * t
            offset = 0.15 * np.sin(i * np.pi / 2) * perp
            points.append(pos + offset)

        return VMobject(color=color, stroke_width=2).set_points_as_corners(points)


class FundamentalConstantsSimple(Scene):
    """シンプル版: 自然定数の利点"""

    def construct(self):
        MEMS_COLOR = RED
        ATOMIC_COLOR = BLUE

        # タイトル
        title = Text("測定基準の違い", font_size=36, color=WHITE).to_edge(UP)
        self.play(Write(title))

        # 比較表形式
        # ヘッダー
        header_mems = Text("MEMS", font_size=28, color=MEMS_COLOR)
        header_atomic = Text("原子干渉計", font_size=28, color=ATOMIC_COLOR)
        headers = VGroup(header_mems, header_atomic).arrange(RIGHT, buff=3)
        headers.shift(UP * 2)

        self.play(Write(headers))

        # 基準
        basis_label = Text("測定基準:", font_size=22, color=GRAY).shift(LEFT * 5 + UP * 1)
        mems_basis = Text("機械部品の特性", font_size=20, color=MEMS_COLOR)
        atomic_basis = Text("自然の基本定数", font_size=20, color=ATOMIC_COLOR)
        basis_row = VGroup(mems_basis, atomic_basis).arrange(RIGHT, buff=2)
        basis_row.shift(UP * 1)

        self.play(Write(basis_label), Write(basis_row))
        self.wait(0.5)

        # 経時変化
        change_label = Text("経時変化:", font_size=22, color=GRAY).shift(LEFT * 5 + UP * 0.2)
        mems_change = Text("劣化・ドリフト", font_size=20, color=MEMS_COLOR)
        atomic_change = Text("なし（普遍的）", font_size=20, color=GREEN)
        change_row = VGroup(mems_change, atomic_change).arrange(RIGHT, buff=2.5)
        change_row.shift(UP * 0.2)

        self.play(Write(change_label), Write(change_row))
        self.wait(0.5)

        # 環境依存
        env_label = Text("環境依存:", font_size=22, color=GRAY).shift(LEFT * 5 + DOWN * 0.6)
        mems_env = Text("温度で変化", font_size=20, color=MEMS_COLOR)
        atomic_env = Text("宇宙でも同じ", font_size=20, color=GREEN)
        env_row = VGroup(mems_env, atomic_env).arrange(RIGHT, buff=2.8)
        env_row.shift(DOWN * 0.6)

        self.play(Write(env_label), Write(env_row))
        self.wait(1)

        # 強調: 自然定数
        highlight = VGroup(
            MathTex(r"h", font_size=36, color=GOLD),
            Text("プランク定数", font_size=20),
            MathTex(r"c", font_size=36, color=GOLD),
            Text("光速", font_size=20),
        ).arrange(RIGHT, buff=0.5)
        highlight.shift(DOWN * 1.8)

        explanation = Text(
            "これらは宇宙のどこでも、いつでも同じ値",
            font_size=22,
            color=YELLOW,
        ).next_to(highlight, DOWN, buff=0.3)

        self.play(Write(highlight), Write(explanation))
        self.wait(2)

        # フェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects])
