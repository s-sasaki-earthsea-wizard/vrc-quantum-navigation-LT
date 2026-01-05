"""
加速度の二重積分アニメーション

加速度から速度、速度から位置への積分の流れを視覚的に示す

使用方法:
    manim -pql double_integral_animation.py DoubleIntegral
    manim -pqh double_integral_animation.py DoubleIntegral  # 高画質
"""

from manim import *


class DoubleIntegral(Scene):
    """加速度の二重積分で位置を求める過程を示すアニメーション"""

    def construct(self):
        # 色の設定
        ACCEL_COLOR = RED
        VELOCITY_COLOR = BLUE
        POSITION_COLOR = GREEN
        ARROW_COLOR = YELLOW

        # タイトル
        title = Text("加速度から位置を求める", font_size=36, color=WHITE).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # ===== パート1: 矢印チェーン =====
        # a → v → x の流れ
        a_tex = MathTex("a", font_size=64, color=ACCEL_COLOR)
        v_tex = MathTex("v", font_size=64, color=VELOCITY_COLOR)
        x_tex = MathTex("x", font_size=64, color=POSITION_COLOR)

        # 積分記号付き矢印
        arrow1 = MathTex(r"\xrightarrow{\int dt}", font_size=48, color=ARROW_COLOR)
        arrow2 = MathTex(r"\xrightarrow{\int dt}", font_size=48, color=ARROW_COLOR)

        # 矢印チェーンを配置
        chain = VGroup(a_tex, arrow1, v_tex, arrow2, x_tex).arrange(RIGHT, buff=0.3)
        chain.shift(UP * 0.5)

        # 日本語ラベル
        a_label = Text("加速度", font_size=24, color=ACCEL_COLOR).next_to(a_tex, DOWN, buff=0.3)
        v_label = Text("速度", font_size=24, color=VELOCITY_COLOR).next_to(v_tex, DOWN, buff=0.3)
        x_label = Text("位置", font_size=24, color=POSITION_COLOR).next_to(x_tex, DOWN, buff=0.3)

        # アニメーション: 矢印チェーン
        self.play(Write(a_tex), Write(a_label))
        self.wait(0.3)
        self.play(Write(arrow1))
        self.play(Write(v_tex), Write(v_label))
        self.wait(0.3)
        self.play(Write(arrow2))
        self.play(Write(x_tex), Write(x_label))
        self.wait(1)

        # ===== パート2: 積分式 =====
        # 矢印チェーンを上に移動
        chain_group = VGroup(chain, a_label, v_label, x_label)
        self.play(chain_group.animate.shift(UP * 1.2).scale(0.8))

        # 積分式を表示
        integral1 = MathTex(
            r"v(t) = \int_0^t a(\tau) \, d\tau",
            font_size=42,
        )
        integral1.set_color_by_tex("v", VELOCITY_COLOR)
        integral1.set_color_by_tex("a", ACCEL_COLOR)

        integral2 = MathTex(
            r"x(t) = \int_0^t v(\tau) \, d\tau",
            font_size=42,
        )
        integral2.set_color_by_tex("x", POSITION_COLOR)
        integral2.set_color_by_tex("v", VELOCITY_COLOR)

        integrals = VGroup(integral1, integral2).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        integrals.shift(DOWN * 1)

        self.play(Write(integral1), run_time=1.5)
        self.wait(0.5)
        self.play(Write(integral2), run_time=1.5)
        self.wait(1)

        # ===== パート3: 二重積分の結論 =====
        conclusion = MathTex(
            r"x(t) = \iint a \, dt \, dt",
            font_size=48,
            color=YELLOW,
        )
        conclusion.next_to(integrals, DOWN, buff=0.8)

        box = SurroundingRectangle(conclusion, color=YELLOW, buff=0.2)

        self.play(Write(conclusion))
        self.play(Create(box))
        self.wait(2)

        # フェードアウト
        self.play(
            FadeOut(title),
            FadeOut(chain_group),
            FadeOut(integrals),
            FadeOut(conclusion),
            FadeOut(box),
        )


class DoubleIntegralWithGraph(Scene):
    """グラフ付きの二重積分アニメーション"""

    def construct(self):
        ACCEL_COLOR = RED
        VELOCITY_COLOR = BLUE
        POSITION_COLOR = GREEN

        # タイトル
        title = Text("二重積分の視覚化", font_size=32).to_edge(UP)
        self.play(Write(title))

        # 3つのグラフを並べる
        axes_config = {
            "x_range": [0, 4, 1],
            "x_length": 3,
            "y_length": 2,
            "axis_config": {"include_tip": True, "tip_length": 0.15},
        }

        axes_a = Axes(y_range=[0, 2, 1], **axes_config).shift(LEFT * 4 + DOWN * 0.3)
        axes_v = Axes(y_range=[0, 4, 1], **axes_config).shift(DOWN * 0.3)
        axes_x = Axes(y_range=[0, 8, 2], **axes_config).shift(RIGHT * 4 + DOWN * 0.3)

        # 軸ラベル
        label_a = MathTex("a(t)", color=ACCEL_COLOR, font_size=28).next_to(axes_a, UP, buff=0.15)
        label_v = MathTex("v(t)", color=VELOCITY_COLOR, font_size=28).next_to(axes_v, UP, buff=0.15)
        label_x = MathTex("x(t)", color=POSITION_COLOR, font_size=28).next_to(axes_x, UP, buff=0.15)

        # 一定加速度 a = 1
        accel_curve = axes_a.plot(lambda t: 1, x_range=[0, 4], color=ACCEL_COLOR, stroke_width=3)

        # 速度 v = t（積分結果）
        velocity_curve = axes_v.plot(lambda t: t, x_range=[0, 4], color=VELOCITY_COLOR, stroke_width=3)

        # 位置 x = t²/2（二重積分結果）
        position_curve = axes_x.plot(
            lambda t: 0.5 * t**2, x_range=[0, 4], color=POSITION_COLOR, stroke_width=3
        )

        # 積分記号付き矢印
        arrow1 = Arrow(
            axes_a.get_right() + RIGHT * 0.1,
            axes_v.get_left() + LEFT * 0.1,
            buff=0.05,
            color=YELLOW,
            stroke_width=3,
        )
        arrow2 = Arrow(
            axes_v.get_right() + RIGHT * 0.1,
            axes_x.get_left() + LEFT * 0.1,
            buff=0.05,
            color=YELLOW,
            stroke_width=3,
        )

        int_label1 = MathTex(r"\int dt", font_size=22, color=YELLOW).next_to(arrow1, UP, buff=0.05)
        int_label2 = MathTex(r"\int dt", font_size=22, color=YELLOW).next_to(arrow2, UP, buff=0.05)

        # アニメーション
        self.play(Create(axes_a), Create(axes_v), Create(axes_x))
        self.play(Write(label_a), Write(label_v), Write(label_x))

        # 加速度グラフ
        self.play(Create(accel_curve))
        accel_area = axes_a.get_area(accel_curve, x_range=[0, 4], color=ACCEL_COLOR, opacity=0.3)
        self.play(FadeIn(accel_area))

        # 矢印と速度グラフ
        self.play(GrowArrow(arrow1), Write(int_label1))
        self.play(Create(velocity_curve))
        velocity_area = axes_v.get_area(velocity_curve, x_range=[0, 4], color=VELOCITY_COLOR, opacity=0.3)
        self.play(FadeIn(velocity_area))

        # 矢印と位置グラフ
        self.play(GrowArrow(arrow2), Write(int_label2))
        self.play(Create(position_curve))

        self.wait(1)

        # 数式を下に表示
        formulas = VGroup(
            MathTex(r"v(t) = \int_0^t a \, d\tau = t", font_size=28),
            MathTex(r"x(t) = \int_0^t v \, d\tau = \frac{t^2}{2}", font_size=28),
        ).arrange(RIGHT, buff=1)
        formulas.to_edge(DOWN, buff=0.5)

        self.play(Write(formulas))
        self.wait(2)

        # フェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class ErrorAccumulation(Scene):
    """誤差蓄積問題を示すアニメーション - δx ~ (1/2) δa · t²"""

    def construct(self):
        # 色の設定
        ERROR_COLOR = RED
        RESULT_COLOR = ORANGE
        HIGHLIGHT_COLOR = YELLOW

        # タイトル
        title = Text("誤差蓄積問題", font_size=36, color=WHITE).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # ===== パート1: 問題提起 =====
        problem_text = Text(
            "加速度のわずかな誤差が...",
            font_size=32,
            color=WHITE,
        ).shift(UP * 1.5)

        self.play(Write(problem_text))
        self.wait(0.5)

        # 誤差の矢印チェーン
        delta_a = MathTex(r"\delta a", font_size=56, color=ERROR_COLOR)
        arrow1 = MathTex(r"\xrightarrow{\int dt}", font_size=42, color=WHITE)
        delta_v = MathTex(r"\delta v", font_size=56, color=ORANGE)
        arrow2 = MathTex(r"\xrightarrow{\int dt}", font_size=42, color=WHITE)
        delta_x = MathTex(r"\delta x", font_size=56, color=RESULT_COLOR)

        error_chain = VGroup(delta_a, arrow1, delta_v, arrow2, delta_x).arrange(RIGHT, buff=0.3)
        error_chain.shift(UP * 0.3)

        # ラベル
        a_label = Text("加速度誤差", font_size=20, color=ERROR_COLOR).next_to(delta_a, DOWN, buff=0.25)
        v_label = Text("速度誤差", font_size=20, color=ORANGE).next_to(delta_v, DOWN, buff=0.25)
        x_label = Text("位置誤差", font_size=20, color=RESULT_COLOR).next_to(delta_x, DOWN, buff=0.25)

        self.play(Write(delta_a), Write(a_label))
        self.play(Write(arrow1))
        self.play(Write(delta_v), Write(v_label))
        self.play(Write(arrow2))
        self.play(Write(delta_x), Write(x_label))
        self.wait(0.5)

        # 問題テキストを更新
        problem_text2 = Text(
            "位置誤差に拡大する！",
            font_size=32,
            color=RESULT_COLOR,
        ).shift(UP * 1.5)

        self.play(Transform(problem_text, problem_text2))
        self.wait(1)

        # ===== パート2: 数式導出 =====
        # 上部をまとめて縮小・移動
        upper_group = VGroup(problem_text, error_chain, a_label, v_label, x_label)
        self.play(upper_group.animate.scale(0.7).to_edge(UP, buff=0.8))

        # 二重積分なので t² に比例
        explanation = Text(
            "二重積分なので誤差は時間の二乗に比例",
            font_size=28,
            color=WHITE,
        ).shift(UP * 0.3)

        self.play(Write(explanation))
        self.wait(0.5)

        # メインの数式
        main_formula = MathTex(
            r"\delta x \sim \frac{1}{2} \delta a \cdot t^2",
            font_size=64,
            color=HIGHLIGHT_COLOR,
        ).shift(DOWN * 0.8)

        box = SurroundingRectangle(main_formula, color=HIGHLIGHT_COLOR, buff=0.25, stroke_width=3)

        self.play(Write(main_formula), run_time=1.5)
        self.play(Create(box))
        self.wait(1)

        # t² を強調
        t_squared_note = Text(
            "← 時間が2倍 → 誤差は4倍！",
            font_size=24,
            color=RED,
        ).next_to(box, DOWN, buff=0.4)

        self.play(Write(t_squared_note))
        self.wait(2)

        # フェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class ErrorAccumulationGraph(Scene):
    """誤差蓄積をグラフで視覚化するアニメーション"""

    def construct(self):
        ERROR_COLOR = RED
        TRUE_COLOR = GREEN
        MEASURED_COLOR = BLUE

        # タイトル
        title = Text("誤差の時間発展", font_size=32, color=WHITE).to_edge(UP)
        self.play(Write(title))

        # 軸の作成
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 15, 5],
            x_length=7,
            y_length=4,
            axis_config={
                "color": WHITE,
                "include_tip": True,
                "tip_length": 0.2,
            },
            x_axis_config={"numbers_to_include": [1, 2, 3, 4]},
            y_axis_config={"numbers_to_include": [5, 10]},
        ).shift(DOWN * 0.5)

        x_label = axes.get_x_axis_label(MathTex("t", font_size=32), edge=RIGHT, direction=RIGHT)
        y_label = axes.get_y_axis_label(
            MathTex(r"\delta x", font_size=32, color=ERROR_COLOR),
            edge=UP,
            direction=UP,
        )

        self.play(Create(axes), Write(x_label), Write(y_label))

        # 誤差曲線: δx = (1/2) δa t² （δa = 1 と仮定）
        error_curve = axes.plot(
            lambda t: 0.5 * t**2,
            x_range=[0, 5],
            color=ERROR_COLOR,
            stroke_width=4,
        )

        curve_label = MathTex(
            r"\delta x = \frac{1}{2} \delta a \cdot t^2",
            font_size=28,
            color=ERROR_COLOR,
        ).next_to(error_curve.get_end(), UP + LEFT, buff=0.2)

        self.play(Create(error_curve), run_time=2)
        self.play(Write(curve_label))
        self.wait(0.5)

        # 時間経過で誤差が急増することを示す
        # t=2 と t=4 の点を比較
        dot_t2 = Dot(axes.c2p(2, 0.5 * 4), color=YELLOW, radius=0.1)
        dot_t4 = Dot(axes.c2p(4, 0.5 * 16), color=YELLOW, radius=0.1)

        line_t2 = DashedLine(
            axes.c2p(2, 0), axes.c2p(2, 0.5 * 4), color=YELLOW, stroke_width=2
        )
        line_t4 = DashedLine(
            axes.c2p(4, 0), axes.c2p(4, 0.5 * 16), color=YELLOW, stroke_width=2
        )

        label_t2 = MathTex("t=2", font_size=24, color=YELLOW).next_to(dot_t2, RIGHT, buff=0.15)
        label_t4 = MathTex("t=4", font_size=24, color=YELLOW).next_to(dot_t4, LEFT, buff=0.15)

        self.play(Create(line_t2), Create(dot_t2), Write(label_t2))
        self.wait(0.3)
        self.play(Create(line_t4), Create(dot_t4), Write(label_t4))
        self.wait(0.5)

        # 比較テキスト
        comparison = VGroup(
            MathTex(r"t=2: \delta x = 2", font_size=28),
            MathTex(r"t=4: \delta x = 8", font_size=28),
            MathTex(r"\text{時間2倍} \rightarrow \text{誤差4倍}", font_size=28, color=RED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        comparison.to_edge(RIGHT, buff=0.5).shift(DOWN * 0.5)

        self.play(Write(comparison), run_time=1.5)
        self.wait(2)

        # フェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class ErrorAccumulationCombined(Scene):
    """誤差蓄積の完全版アニメーション（数式 + グラフ）"""

    def construct(self):
        ERROR_COLOR = RED
        HIGHLIGHT_COLOR = YELLOW

        # ===== パート1: 問題と数式 =====
        title = Text("慣性航法の誤差蓄積", font_size=36, color=WHITE).to_edge(UP)
        self.play(Write(title))

        # 誤差の矢印チェーン
        delta_a = MathTex(r"\delta a", font_size=48, color=ERROR_COLOR)
        arrow1 = MathTex(r"\xrightarrow{\int}", font_size=36, color=WHITE)
        delta_v = MathTex(r"\delta v", font_size=48, color=ORANGE)
        arrow2 = MathTex(r"\xrightarrow{\int}", font_size=36, color=WHITE)
        delta_x = MathTex(r"\delta x", font_size=48, color=YELLOW)

        error_chain = VGroup(delta_a, arrow1, delta_v, arrow2, delta_x).arrange(RIGHT, buff=0.2)
        error_chain.shift(UP * 2)

        self.play(Write(error_chain), run_time=1.5)
        self.wait(0.5)

        # メインの数式
        main_formula = MathTex(
            r"\delta x \sim \frac{1}{2} \delta a \cdot t^2",
            font_size=48,
            color=HIGHLIGHT_COLOR,
        ).shift(UP * 0.8)

        box = SurroundingRectangle(main_formula, color=HIGHLIGHT_COLOR, buff=0.2)

        self.play(Write(main_formula))
        self.play(Create(box))
        self.wait(0.5)

        # ===== パート2: グラフ =====
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 12, 4],
            x_length=5,
            y_length=2.5,
            axis_config={"include_tip": True, "tip_length": 0.15},
            x_axis_config={"numbers_to_include": [2, 4]},
        ).shift(DOWN * 1.8)

        x_label = axes.get_x_axis_label(MathTex("t", font_size=28), edge=RIGHT)
        y_label = axes.get_y_axis_label(MathTex(r"\delta x", font_size=28, color=ERROR_COLOR), edge=UP)

        self.play(Create(axes), Write(x_label), Write(y_label))

        # 誤差曲線
        error_curve = axes.plot(
            lambda t: 0.5 * t**2,
            x_range=[0, 5],
            color=ERROR_COLOR,
            stroke_width=3,
        )

        # 塗りつぶし（誤差の蓄積を視覚化）
        area = axes.get_area(error_curve, x_range=[0, 5], color=ERROR_COLOR, opacity=0.3)

        self.play(Create(error_curve), FadeIn(area), run_time=1.5)
        self.wait(0.5)

        # 警告テキスト
        warning = Text(
            "時間とともに誤差が急速に増大",
            font_size=24,
            color=RED,
        ).next_to(axes, DOWN, buff=0.3)

        self.play(Write(warning))
        self.wait(2)

        # フェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects])
