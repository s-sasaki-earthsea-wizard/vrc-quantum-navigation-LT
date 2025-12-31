"""
VTグラフと移動距離のアニメーション

速度-時間グラフの面積が移動距離になることを視覚的に示す

使用方法:
    manim -pql vt_graph_animation.py VTGraphAnimation
    manim -pqh vt_graph_animation.py VTGraphAnimation  # 高画質
"""

from manim import *


class VTGraphAnimation(Scene):
    """VTグラフと積分の概念を示すアニメーション"""

    def construct(self):
        # 色の設定
        VELOCITY_COLOR = BLUE
        AREA_COLOR = BLUE_A
        AXIS_COLOR = WHITE

        # 軸の作成
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 4, 1],
            x_length=8,
            y_length=5,
            axis_config={
                "color": AXIS_COLOR,
                "include_tip": True,
                "tip_length": 0.2,
            },
            x_axis_config={"numbers_to_include": [1, 2, 3, 4]},
            y_axis_config={"numbers_to_include": [1, 2, 3]},
        )

        # 軸ラベル
        x_label = axes.get_x_axis_label(
            MathTex("t", color=AXIS_COLOR), edge=RIGHT, direction=RIGHT
        )
        y_label = axes.get_y_axis_label(
            MathTex("v(t)", color=AXIS_COLOR), edge=UP, direction=UP
        )

        # 速度関数（変化する速度の例）
        def velocity_func(t):
            return 0.5 * t + 1 + 0.5 * np.sin(t)

        # 速度曲線
        velocity_curve = axes.plot(
            velocity_func,
            x_range=[0, 4.5],
            color=VELOCITY_COLOR,
            stroke_width=3,
        )

        # グラフとラベルを表示
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(0.5)

        # 速度曲線を描画
        velocity_label = MathTex("v(t)", color=VELOCITY_COLOR).next_to(
            velocity_curve.get_end(), UP
        )
        self.play(Create(velocity_curve), Write(velocity_label))
        self.wait(1)

        # リーマン和（粗い分割）
        riemann_rects_coarse = axes.get_riemann_rectangles(
            velocity_curve,
            x_range=[0, 4],
            dx=1.0,
            color=[AREA_COLOR, TEAL],
            fill_opacity=0.5,
            stroke_width=1,
            stroke_color=WHITE,
        )

        # 面積のテキスト
        area_text = Text("面積 = 移動距離", font_size=36, color=YELLOW).to_edge(UP)

        self.play(Create(riemann_rects_coarse), Write(area_text))
        self.wait(1)

        # より細かい分割へ遷移
        riemann_rects_medium = axes.get_riemann_rectangles(
            velocity_curve,
            x_range=[0, 4],
            dx=0.5,
            color=[AREA_COLOR, TEAL],
            fill_opacity=0.5,
            stroke_width=1,
            stroke_color=WHITE,
        )

        self.play(Transform(riemann_rects_coarse, riemann_rects_medium))
        self.wait(0.5)

        # さらに細かく
        riemann_rects_fine = axes.get_riemann_rectangles(
            velocity_curve,
            x_range=[0, 4],
            dx=0.2,
            color=[AREA_COLOR, TEAL],
            fill_opacity=0.5,
            stroke_width=0.5,
            stroke_color=WHITE,
        )

        self.play(Transform(riemann_rects_coarse, riemann_rects_fine))
        self.wait(0.5)

        # 極限（滑らかな面積）
        area = axes.get_area(
            velocity_curve,
            x_range=[0, 4],
            color=AREA_COLOR,
            opacity=0.6,
        )

        self.play(Transform(riemann_rects_coarse, area))
        self.wait(1)

        # 積分の数式を表示（面積テキストと入れ替え）
        integral_formula = MathTex(
            r"x(t) = \int_0^t v(\tau) \, d\tau",
            font_size=42,
            color=YELLOW,
        ).to_edge(UP)

        self.play(Transform(area_text, integral_formula))
        self.wait(2)

        # フェードアウト
        self.play(
            FadeOut(riemann_rects_coarse),
            FadeOut(area_text),
            FadeOut(velocity_curve),
            FadeOut(velocity_label),
            FadeOut(axes),
            FadeOut(x_label),
            FadeOut(y_label),
        )


class ConstantVelocity(Scene):
    """等速運動の場合（比較用）"""

    def construct(self):
        VELOCITY_COLOR = BLUE
        AREA_COLOR = BLUE_A

        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 4, 1],
            x_length=8,
            y_length=5,
            axis_config={"include_tip": True},
        )

        x_label = axes.get_x_axis_label(MathTex("t"), edge=RIGHT)
        y_label = axes.get_y_axis_label(MathTex("v"), edge=UP)

        # 等速（一定の速度）
        constant_v = axes.plot(lambda t: 2, x_range=[0, 4], color=VELOCITY_COLOR)

        # 長方形の面積
        area = axes.get_area(constant_v, x_range=[0, 4], color=AREA_COLOR, opacity=0.6)

        # 数式
        formula = MathTex(r"x = v \cdot t", font_size=48, color=YELLOW).to_edge(UP)

        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(Create(constant_v))
        self.play(FadeIn(area), Write(formula))
        self.wait(2)


class AcceleratedMotion(Scene):
    """加速度運動と二重積分"""

    def construct(self):
        ACCEL_COLOR = RED
        VELOCITY_COLOR = BLUE
        POSITION_COLOR = GREEN

        # タイトル
        title = Text("加速度 → 速度 → 位置", font_size=36).to_edge(UP)
        self.play(Write(title))

        # 3つのグラフを並べる
        axes_a = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 3, 1],
            x_length=3.5,
            y_length=2.5,
            axis_config={"include_tip": True, "tip_length": 0.15},
        ).shift(LEFT * 4 + DOWN * 0.5)

        axes_v = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 4, 1],
            x_length=3.5,
            y_length=2.5,
            axis_config={"include_tip": True, "tip_length": 0.15},
        ).shift(DOWN * 0.5)

        axes_x = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 8, 2],
            x_length=3.5,
            y_length=2.5,
            axis_config={"include_tip": True, "tip_length": 0.15},
        ).shift(RIGHT * 4 + DOWN * 0.5)

        # ラベル
        label_a = MathTex("a(t)", color=ACCEL_COLOR, font_size=30).next_to(
            axes_a, UP, buff=0.2
        )
        label_v = MathTex("v(t)", color=VELOCITY_COLOR, font_size=30).next_to(
            axes_v, UP, buff=0.2
        )
        label_x = MathTex("x(t)", color=POSITION_COLOR, font_size=30).next_to(
            axes_x, UP, buff=0.2
        )

        # 一定加速度
        accel_curve = axes_a.plot(lambda t: 1, x_range=[0, 4], color=ACCEL_COLOR)

        # 速度（積分結果）
        velocity_curve = axes_v.plot(lambda t: t, x_range=[0, 4], color=VELOCITY_COLOR)

        # 位置（二重積分結果）
        position_curve = axes_x.plot(
            lambda t: 0.5 * t**2, x_range=[0, 4], color=POSITION_COLOR
        )

        # 矢印
        arrow1 = Arrow(
            axes_a.get_right() + RIGHT * 0.2,
            axes_v.get_left() + LEFT * 0.2,
            buff=0.1,
            color=WHITE,
        )
        arrow2 = Arrow(
            axes_v.get_right() + RIGHT * 0.2,
            axes_x.get_left() + LEFT * 0.2,
            buff=0.1,
            color=WHITE,
        )

        int_label1 = MathTex(r"\int", font_size=24).next_to(arrow1, UP, buff=0.1)
        int_label2 = MathTex(r"\int", font_size=24).next_to(arrow2, UP, buff=0.1)

        # アニメーション
        self.play(Create(axes_a), Create(axes_v), Create(axes_x))
        self.play(Write(label_a), Write(label_v), Write(label_x))

        self.play(Create(accel_curve))
        self.play(GrowArrow(arrow1), Write(int_label1))
        self.play(Create(velocity_curve))
        self.play(GrowArrow(arrow2), Write(int_label2))
        self.play(Create(position_curve))

        self.wait(2)

        # 数式
        formulas = VGroup(
            MathTex(r"v(t) = \int a(t) \, dt", font_size=28),
            MathTex(r"x(t) = \int v(t) \, dt", font_size=28),
        ).arrange(RIGHT, buff=1.5)
        formulas.to_edge(DOWN)

        self.play(Write(formulas))
        self.wait(2)
