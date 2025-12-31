"""
マッハ-ツェンダー型干渉計のアニメーション

光学干渉計と原子干渉計の対応を視覚的に示す

使用方法:
    manim -pql mach_zehnder_animation.py MachZehnderOptical
    manim -pql mach_zehnder_animation.py MachZehnderAtomic
    manim -pql mach_zehnder_animation.py MachZehnderComparison
"""

from manim import *
import numpy as np


class MachZehnderOptical(Scene):
    """光学的マッハ-ツェンダー干渉計（正方形配置）"""

    def construct(self):
        title = Text("光学的マッハ-ツェンダー干渉計", font_size=36).to_edge(UP)
        self.play(Write(title))

        # 干渉計のレイアウト（正方形配置）
        # 正方形の辺の長さ
        side = 3.0
        center = ORIGIN + DOWN * 0.3

        # 位置の定義（正方形の頂点）
        bs1_pos = center + LEFT * side / 2 + UP * side / 2    # 左上: BS₁
        m1_pos = center + RIGHT * side / 2 + UP * side / 2    # 右上: M₁
        m2_pos = center + LEFT * side / 2 + DOWN * side / 2   # 左下: M₂
        bs2_pos = center + RIGHT * side / 2 + DOWN * side / 2  # 右下: BS₂

        # ビームスプリッター1（左上、45度傾斜板）
        bs1 = Rectangle(width=0.8, height=0.12, color=BLUE, fill_opacity=0.5)
        bs1.rotate(-PI / 4).move_to(bs1_pos)
        bs1_label = Text("BS₁", font_size=20, color=BLUE).next_to(bs1, UL, buff=0.15)

        # ビームスプリッター2（右下、45度傾斜板）
        bs2 = Rectangle(width=0.8, height=0.12, color=BLUE, fill_opacity=0.5)
        bs2.rotate(-PI / 4).move_to(bs2_pos)
        bs2_label = Text("BS₂", font_size=20, color=BLUE).next_to(bs2, DR, buff=0.15)

        # ミラー1（右上、-45度傾斜 = \の向き）
        # 左から来た光を下に反射
        m1 = Rectangle(width=0.8, height=0.12, color=GRAY, fill_opacity=0.9)
        m1.rotate(-PI / 4).move_to(m1_pos)
        m1_label = Text("M₁", font_size=20, color=GRAY).next_to(m1, UR, buff=0.15)

        # ミラー2（左下、-45度傾斜 = \の向き）
        # 上から来た光を右に反射
        m2 = Rectangle(width=0.8, height=0.12, color=GRAY, fill_opacity=0.9)
        m2.rotate(-PI / 4).move_to(m2_pos)
        m2_label = Text("M₂", font_size=20, color=GRAY).next_to(m2, DL, buff=0.15)

        # サンプル（上辺の経路上、BS₁→M₁の間）
        sample_pos = (bs1_pos + m1_pos) / 2
        sample = Rectangle(
            width=0.5, height=0.7,
            color=TEAL, fill_opacity=0.4,
            stroke_color=TEAL, stroke_width=2
        )
        sample.move_to(sample_pos)
        sample_label = Text("サンプル", font_size=16, color=TEAL).next_to(sample, UP, buff=0.1)
        sample_note = MathTex(r"n > 1", font_size=18, color=TEAL).next_to(sample, DOWN, buff=0.05)

        # 光源（左から入射）
        source = Circle(radius=0.25, color=YELLOW, fill_opacity=0.8)
        source.move_to(bs1_pos + LEFT * 2)
        source_label = Text("光源", font_size=18).next_to(source, UP)

        # 検出器1（BS₂から右へ出射）
        detector1 = Rectangle(width=0.5, height=0.6, color=GREEN, fill_opacity=0.6)
        detector1.move_to(bs2_pos + RIGHT * 2)
        det1_label = Text("検出器1", font_size=16).next_to(detector1, UP)

        # 検出器2（BS₂から下へ出射）
        detector2 = Rectangle(width=0.6, height=0.5, color=GREEN, fill_opacity=0.6)
        detector2.move_to(bs2_pos + DOWN * 1.5)
        det2_label = Text("検出器2", font_size=16).next_to(detector2, RIGHT)

        # 光学素子を順番に表示
        self.play(FadeIn(source), Write(source_label))
        self.wait(0.3)

        self.play(
            FadeIn(bs1), Write(bs1_label),
            FadeIn(bs2), Write(bs2_label),
        )
        self.play(
            FadeIn(m1), Write(m1_label),
            FadeIn(m2), Write(m2_label),
        )
        self.play(FadeIn(sample), Write(sample_label), Write(sample_note))
        self.play(
            FadeIn(detector1), Write(det1_label),
            FadeIn(detector2), Write(det2_label),
        )
        self.wait(0.5)

        # 入射光（左から水平にBS₁へ）
        input_ray = Arrow(
            source.get_right() + RIGHT * 0.1,
            bs1_pos + LEFT * 0.3,
            color=YELLOW,
            buff=0,
            stroke_width=4,
        )

        self.play(GrowArrow(input_ray))
        self.wait(0.3)

        # ステップ1: 分割
        step1_text = Text("① 分割（ハーフミラー）", font_size=26, color=YELLOW)
        step1_text.to_corner(UL).shift(DOWN * 0.8 + RIGHT * 0.2)
        self.play(Write(step1_text))

        # 経路A（上辺を通る: BS₁→M₁）- 赤
        # 3つのセグメント: BS₁→サンプル入口、サンプル内、サンプル出口→M₁
        path_a1 = Line(
            bs1_pos + RIGHT * 0.3,
            sample.get_left(),
            color=RED,
            stroke_width=3,
        )
        path_a_sample = Line(
            sample.get_left(),
            sample.get_right(),
            color=RED,
            stroke_width=3,
        )
        path_a2_to_m1 = Arrow(
            sample.get_right(),
            m1_pos + LEFT * 0.3,
            color=RED,
            buff=0,
            stroke_width=3,
        )
        path_a_label = Text("経路A", font_size=16, color=RED)
        path_a_label.next_to(sample, UP, buff=0.6)

        # 経路B（左辺を通る: BS₁→M₂）- 青
        path_b1 = Arrow(
            bs1_pos + DOWN * 0.3,
            m2_pos + UP * 0.3,
            color=BLUE,
            buff=0,
            stroke_width=3,
        )
        path_b_label = Text("経路B", font_size=16, color=BLUE)
        path_b_label.next_to(path_b1, LEFT, buff=0.1)

        # 経路Aは順番にアニメーション（サンプル内は遅く）
        # 経路Bは経路A全体と同時に進行
        self.play(
            Create(path_a1, run_time=0.4),
            GrowArrow(path_b1, run_time=1.2),
            Write(path_a_label),
            Write(path_b_label),
        )
        # サンプル内は遅く（屈折率が高いので光が遅くなる）
        self.play(Create(path_a_sample, run_time=0.6, rate_func=linear))
        # サンプル後は通常速度
        self.play(GrowArrow(path_a2_to_m1, run_time=0.3))
        self.wait(0.5)

        # ステップ2: 反射
        step2_text = Text("② 反射（全反射鏡）", font_size=26, color=YELLOW)
        step2_text.next_to(step1_text, DOWN, aligned_edge=LEFT)
        self.play(Write(step2_text))

        # 経路A続き（右辺: M₁→BS₂）
        path_a2 = Arrow(
            m1_pos + DOWN * 0.3,
            bs2_pos + UP * 0.3,
            color=RED,
            buff=0,
            stroke_width=3,
        )

        # 経路B続き（下辺: M₂→BS₂）
        path_b2 = Arrow(
            m2_pos + RIGHT * 0.3,
            bs2_pos + LEFT * 0.3,
            color=BLUE,
            buff=0,
            stroke_width=3,
        )

        self.play(GrowArrow(path_a2), GrowArrow(path_b2))
        self.wait(0.5)

        # ステップ3: 再結合
        step3_text = Text("③ 再結合（干渉）", font_size=26, color=YELLOW)
        step3_text.next_to(step2_text, DOWN, aligned_edge=LEFT)
        self.play(Write(step3_text))

        # 出力光1（BS₂から右へ → 検出器1）
        output_ray1 = Arrow(
            bs2_pos + RIGHT * 0.3,
            detector1.get_left() + LEFT * 0.1,
            color=PURPLE,
            buff=0,
            stroke_width=4,
        )

        # 出力光2（BS₂から下へ → 検出器2）
        output_ray2 = Arrow(
            bs2_pos + DOWN * 0.3,
            detector2.get_top() + UP * 0.1,
            color=PURPLE,
            buff=0,
            stroke_width=4,
        )

        self.play(GrowArrow(output_ray1), GrowArrow(output_ray2))
        self.wait(0.5)

        # ステップ表示をフェードアウト
        self.play(FadeOut(step1_text), FadeOut(step2_text), FadeOut(step3_text))
        self.wait(0.5)

        # 干渉計全体をフェードアウト
        interferometer_elements = VGroup(
            source, source_label,
            bs1, bs1_label, bs2, bs2_label,
            m1, m1_label, m2, m2_label,
            sample, sample_label, sample_note,
            detector1, det1_label, detector2, det2_label,
            input_ray,
            path_a1, path_a_sample, path_a2_to_m1, path_a_label,
            path_b1, path_b_label,
            path_a2, path_b2,
            output_ray1, output_ray2,
        )
        self.play(FadeOut(interferometer_elements))
        self.wait(0.3)

        # 干渉の説明（中央に大きく表示）
        explanation = VGroup(
            Text("サンプルを通る経路Aは光路長が変化", font_size=28),
            MathTex(r"\Delta L = (n - 1) \cdot d", font_size=40, color=TEAL),
            MathTex(r"\Downarrow", font_size=36),
            MathTex(r"\Delta\phi = \frac{2\pi}{\lambda} \cdot \Delta L", font_size=44),
            Text("2つの検出器の強度は相補的（明/暗ポート）", font_size=24, color=GREEN),
        ).arrange(DOWN, buff=0.4)
        explanation.move_to(ORIGIN)

        self.play(Write(explanation), run_time=2)
        self.wait(2)


class OpticalMachZehnder(Scene):
    """光学的マッハ-ツェンダー干渉計"""

    def construct(self):
        title = Text("光学的マッハ-ツェンダー干渉計", font_size=36).to_edge(UP)
        self.play(Write(title))

        # 干渉計の構成要素
        # ビームスプリッター1（入力側）
        bs1 = Square(side_length=0.5, color=BLUE, fill_opacity=0.3)
        bs1.rotate(PI / 4)
        bs1.move_to(LEFT * 3)
        bs1_label = Text("BS", font_size=20).next_to(bs1, DOWN)

        # ミラー1（上側）
        m1 = Rectangle(width=0.6, height=0.15, color=GRAY, fill_opacity=0.8)
        m1.rotate(PI / 4)
        m1.move_to(LEFT * 3 + UP * 2)
        m1_label = Text("M", font_size=20).next_to(m1, LEFT)

        # ミラー2（右側）
        m2 = Rectangle(width=0.6, height=0.15, color=GRAY, fill_opacity=0.8)
        m2.rotate(-PI / 4)
        m2.move_to(RIGHT * 1 + DOWN * 0)
        m2_label = Text("M", font_size=20).next_to(m2, RIGHT)

        # ビームスプリッター2（出力側）
        bs2 = Square(side_length=0.5, color=BLUE, fill_opacity=0.3)
        bs2.rotate(PI / 4)
        bs2.move_to(RIGHT * 1 + UP * 2)
        bs2_label = Text("BS", font_size=20).next_to(bs2, DOWN)

        # 検出器
        detector = Rectangle(width=0.4, height=0.6, color=GREEN, fill_opacity=0.5)
        detector.move_to(RIGHT * 3 + UP * 2)
        det_label = Text("検出器", font_size=18).next_to(detector, RIGHT)

        # 光学系を配置
        optics = VGroup(bs1, bs1_label, m1, m1_label, m2, m2_label, bs2, bs2_label, detector, det_label)
        optics.move_to(ORIGIN)

        self.play(
            FadeIn(bs1), Write(bs1_label),
            FadeIn(m1), Write(m1_label),
            FadeIn(m2), Write(m2_label),
            FadeIn(bs2), Write(bs2_label),
            FadeIn(detector), Write(det_label),
        )
        self.wait(0.5)

        # 光線の経路
        # 入射光
        input_ray = Arrow(LEFT * 5, bs1.get_center() + LEFT * 0.3, color=YELLOW, buff=0)

        # 経路A（上を通る）
        path_a1 = Arrow(bs1.get_center(), m1.get_center(), color=RED, buff=0.2)
        path_a2 = Arrow(m1.get_center(), bs2.get_center(), color=RED, buff=0.2)

        # 経路B（右を通る）
        path_b1 = Arrow(bs1.get_center(), m2.get_center(), color=BLUE, buff=0.2)
        path_b2 = Arrow(m2.get_center(), bs2.get_center(), color=BLUE, buff=0.2)

        # 出力
        output_ray = Arrow(bs2.get_center(), detector.get_center(), color=PURPLE, buff=0.2)

        # アニメーション
        self.play(GrowArrow(input_ray))
        self.wait(0.3)

        # 分割
        split_text = Text("分割", font_size=24, color=YELLOW).next_to(bs1, UP, buff=0.5)
        self.play(Write(split_text))
        self.play(
            GrowArrow(path_a1),
            GrowArrow(path_b1),
        )
        self.wait(0.3)

        # 反射
        reflect_text = Text("反射", font_size=24, color=YELLOW).move_to(UP * 3)
        self.play(Write(reflect_text))
        self.play(
            GrowArrow(path_a2),
            GrowArrow(path_b2),
        )
        self.wait(0.3)

        # 再結合
        recombine_text = Text("再結合", font_size=24, color=YELLOW).next_to(bs2, UP, buff=0.5)
        self.play(Write(recombine_text))
        self.play(GrowArrow(output_ray))
        self.wait(0.5)

        # 干渉の説明
        self.play(FadeOut(split_text), FadeOut(reflect_text), FadeOut(recombine_text))

        interference_text = VGroup(
            Text("2つの経路の位相差が干渉縞を作る", font_size=24),
            MathTex(r"\Delta\phi = \frac{2\pi}{\lambda} \Delta L", font_size=32),
        ).arrange(DOWN, buff=0.3)
        interference_text.to_edge(DOWN)

        self.play(Write(interference_text))
        self.wait(2)


class AtomInterferometer(Scene):
    """原子干渉計（ラマンパルス方式）"""

    def construct(self):
        title = Text("原子干渉計（ラマンパルス方式）", font_size=36).to_edge(UP)
        self.play(Write(title))

        # 時間軸
        time_axis = Arrow(LEFT * 5, RIGHT * 5, color=WHITE, buff=0)
        time_label = Text("時間", font_size=20).next_to(time_axis, RIGHT)
        self.play(GrowArrow(time_axis), Write(time_label))

        # パルス位置
        pulse_positions = [LEFT * 3, ORIGIN, RIGHT * 3]
        pulse_labels = ["π/2", "π", "π/2"]
        pulse_colors = [BLUE, RED, BLUE]

        pulses = []
        labels = []

        for pos, label, color in zip(pulse_positions, pulse_labels, pulse_colors):
            # パルスを表す縦線
            pulse = Line(pos + DOWN * 0.3, pos + UP * 2.5, color=color, stroke_width=4)
            pulse_text = MathTex(label, font_size=32, color=color).next_to(pulse, UP)
            pulses.append(pulse)
            labels.append(pulse_text)

        # 時刻ラベル
        t0 = Text("t=0", font_size=18).next_to(pulse_positions[0] + DOWN * 0.5, DOWN)
        tT = Text("t=T", font_size=18).next_to(pulse_positions[1] + DOWN * 0.5, DOWN)
        t2T = Text("t=2T", font_size=18).next_to(pulse_positions[2] + DOWN * 0.5, DOWN)

        # 原子の軌跡
        # 初期状態（|g⟩）
        start_point = LEFT * 4.5 + UP * 0.5

        # 経路A（|e⟩状態、運動量+ħk）
        path_a = VMobject(color=RED, stroke_width=3)
        path_a.set_points_smoothly([
            start_point,
            pulse_positions[0] + UP * 0.5,
            pulse_positions[1] + UP * 2,
            pulse_positions[2] + UP * 0.5,
            RIGHT * 4.5 + UP * 0.5,
        ])

        # 経路B（|g⟩状態、運動量0）
        path_b = VMobject(color=BLUE, stroke_width=3)
        path_b.set_points_smoothly([
            start_point,
            pulse_positions[0] + UP * 0.5,
            pulse_positions[1] + DOWN * 0.5,
            pulse_positions[2] + UP * 0.5,
            RIGHT * 4.5 + UP * 0.5,
        ])

        # アニメーション
        # パルスを順番に表示
        self.play(Create(pulses[0]), Write(labels[0]), Write(t0))
        self.wait(0.3)

        # 分割の説明
        split_text = Text("分割", font_size=24, color=YELLOW).next_to(pulses[0], LEFT, buff=0.5)
        self.play(Write(split_text))

        # 経路の分岐を表示
        path_a_seg1 = VMobject(color=RED, stroke_width=3)
        path_a_seg1.set_points_smoothly([
            start_point,
            pulse_positions[0] + UP * 0.5,
            pulse_positions[1] + UP * 2,
        ])

        path_b_seg1 = VMobject(color=BLUE, stroke_width=3)
        path_b_seg1.set_points_smoothly([
            start_point,
            pulse_positions[0] + UP * 0.5,
            pulse_positions[1] + DOWN * 0.5,
        ])

        self.play(Create(path_a_seg1), Create(path_b_seg1), run_time=1.5)

        # πパルス
        self.play(Create(pulses[1]), Write(labels[1]), Write(tT))
        reflect_text = Text("反転", font_size=24, color=YELLOW).next_to(pulses[1], LEFT, buff=0.5)
        self.play(ReplacementTransform(split_text, reflect_text))

        # 経路の続き
        path_a_seg2 = VMobject(color=RED, stroke_width=3)
        path_a_seg2.set_points_smoothly([
            pulse_positions[1] + UP * 2,
            pulse_positions[2] + UP * 0.5,
        ])

        path_b_seg2 = VMobject(color=BLUE, stroke_width=3)
        path_b_seg2.set_points_smoothly([
            pulse_positions[1] + DOWN * 0.5,
            pulse_positions[2] + UP * 0.5,
        ])

        self.play(Create(path_a_seg2), Create(path_b_seg2), run_time=1.5)

        # π/2パルス（再結合）
        self.play(Create(pulses[2]), Write(labels[2]), Write(t2T))
        recombine_text = Text("再結合", font_size=24, color=YELLOW).next_to(pulses[2], RIGHT, buff=0.5)
        self.play(ReplacementTransform(reflect_text, recombine_text))

        self.wait(0.5)
        self.play(FadeOut(recombine_text))

        # 凡例
        legend = VGroup(
            VGroup(
                Line(ORIGIN, RIGHT * 0.5, color=RED, stroke_width=3),
                MathTex(r"|e\rangle", font_size=24, color=RED),
                Text("（運動量 +ħk）", font_size=18, color=RED),
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                Line(ORIGIN, RIGHT * 0.5, color=BLUE, stroke_width=3),
                MathTex(r"|g\rangle", font_size=24, color=BLUE),
                Text("（運動量 0）", font_size=18, color=BLUE),
            ).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        legend.to_corner(DL)

        self.play(Write(legend))
        self.wait(1)

        # 位相差の式
        phase_formula = VGroup(
            Text("加速度による位相差:", font_size=24),
            MathTex(r"\Delta\phi = k_{\text{eff}} \cdot a \cdot T^2", font_size=36, color=YELLOW),
        ).arrange(DOWN, buff=0.2)
        phase_formula.to_edge(DOWN)

        self.play(Write(phase_formula))
        self.wait(2)


class MachZehnderComparison(Scene):
    """光学干渉計と原子干渉計の比較"""

    def construct(self):
        title = Text("光学干渉計 vs 原子干渉計", font_size=36).to_edge(UP)
        self.play(Write(title))

        # 左側：光学系
        optical_title = Text("光学系", font_size=28, color=YELLOW).move_to(LEFT * 3.5 + UP * 2)

        # 光学干渉計の簡略図
        optical_diagram = VGroup()

        # ビームスプリッター（ハーフミラー）
        bs = Square(side_length=0.4, color=BLUE, fill_opacity=0.3).rotate(PI / 4)
        bs.move_to(LEFT * 4.5 + UP * 0.5)
        bs_label = Text("ハーフミラー", font_size=14).next_to(bs, DOWN, buff=0.3)

        # ミラー
        mirror = Rectangle(width=0.5, height=0.1, color=GRAY, fill_opacity=0.8)
        mirror.move_to(LEFT * 3 + UP * 0.5)
        mirror_label = Text("全反射鏡", font_size=14).next_to(mirror, DOWN, buff=0.3)

        optical_diagram.add(bs, bs_label, mirror, mirror_label)
        optical_diagram.move_to(LEFT * 3.5 + DOWN * 0.5)

        # 右側：原子系
        atom_title = Text("原子系", font_size=28, color=YELLOW).move_to(RIGHT * 3.5 + UP * 2)

        # 原子干渉計の簡略図
        atom_diagram = VGroup()

        # π/2パルス
        pi2_pulse = Line(UP * 0.5, DOWN * 0.5, color=BLUE, stroke_width=6)
        pi2_pulse.move_to(RIGHT * 2 + UP * 0.5)
        pi2_label = MathTex(r"\pi/2", font_size=24, color=BLUE).next_to(pi2_pulse, DOWN, buff=0.3)
        pi2_desc = Text("パルス", font_size=14).next_to(pi2_label, DOWN, buff=0.1)

        # πパルス
        pi_pulse = Line(UP * 0.5, DOWN * 0.5, color=RED, stroke_width=6)
        pi_pulse.move_to(RIGHT * 4 + UP * 0.5)
        pi_label = MathTex(r"\pi", font_size=24, color=RED).next_to(pi_pulse, DOWN, buff=0.3)
        pi_desc = Text("パルス", font_size=14).next_to(pi_label, DOWN, buff=0.1)

        atom_diagram.add(pi2_pulse, pi2_label, pi2_desc, pi_pulse, pi_label, pi_desc)
        atom_diagram.move_to(RIGHT * 3.5 + DOWN * 0.5)

        # 対応表
        table = VGroup()

        headers = VGroup(
            Text("要素", font_size=22),
            Text("光学系", font_size=22),
            Text("原子系", font_size=22),
        ).arrange(RIGHT, buff=1.5)

        row1 = VGroup(
            Text("波", font_size=20),
            Text("光子", font_size=20, color=YELLOW),
            Text("ド・ブロイ波", font_size=20, color=YELLOW),
        ).arrange(RIGHT, buff=1.2)

        row2 = VGroup(
            Text("分割器", font_size=20),
            Text("ハーフミラー", font_size=20, color=BLUE),
            MathTex(r"\pi/2", font_size=24, color=BLUE),
        ).arrange(RIGHT, buff=0.9)

        row3 = VGroup(
            Text("反射器", font_size=20),
            Text("全反射鏡", font_size=20, color=RED),
            MathTex(r"\pi", font_size=24, color=RED),
        ).arrange(RIGHT, buff=1.1)

        table = VGroup(headers, row1, row2, row3).arrange(DOWN, buff=0.4)
        table.move_to(DOWN * 1.5)

        # 区切り線
        divider = Line(UP * 2.5, DOWN * 2.5, color=GRAY, stroke_width=2)

        # アニメーション
        self.play(Write(optical_title), Write(atom_title))
        self.play(Create(divider))
        self.wait(0.3)

        self.play(FadeIn(optical_diagram))
        self.play(FadeIn(atom_diagram))
        self.wait(0.5)

        # 表を順番に表示
        self.play(Write(headers))
        self.wait(0.3)

        for row in [row1, row2, row3]:
            self.play(Write(row))
            self.wait(0.3)

        self.wait(1)

        # 結論
        conclusion = Text(
            "本質は同じ: 波の分割・反射・再結合による干渉",
            font_size=24,
            color=GREEN,
        ).to_edge(DOWN)

        self.play(Write(conclusion))
        self.wait(2)


class PulseSequence(Scene):
    """パルスシーケンスの詳細"""

    def construct(self):
        title = Text("パルスシーケンス: π/2 - π - π/2", font_size=36).to_edge(UP)
        self.play(Write(title))

        # 時間軸
        time_line = Line(LEFT * 5, RIGHT * 5, color=WHITE)
        time_line.move_to(DOWN * 1)
        self.play(Create(time_line))

        # パルス
        pulse_data = [
            (LEFT * 3, "π/2", BLUE, "分割"),
            (ORIGIN, "π", RED, "反転"),
            (RIGHT * 3, "π/2", BLUE, "再結合"),
        ]

        pulses = []
        for pos, label, color, desc in pulse_data:
            # パルス波形
            pulse = VGroup()
            wave = FunctionGraph(
                lambda x: 0.8 * np.sin(10 * x) * np.exp(-2 * x**2),
                x_range=[-1, 1],
                color=color,
            )
            wave.scale(0.5).move_to(pos + UP * 0.5)
            pulse.add(wave)

            # ラベル
            pulse_label = MathTex(label, font_size=32, color=color)
            pulse_label.next_to(wave, UP, buff=0.2)
            pulse.add(pulse_label)

            # 説明
            desc_text = Text(desc, font_size=20)
            desc_text.next_to(pos + DOWN * 1, DOWN, buff=0.3)
            pulse.add(desc_text)

            pulses.append(pulse)

        # 時刻ラベル
        times = [
            (LEFT * 3, "0"),
            (ORIGIN, "T"),
            (RIGHT * 3, "2T"),
        ]

        time_labels = []
        for pos, t in times:
            label = MathTex(f"t = {t}", font_size=24)
            label.next_to(pos + DOWN * 1, UP, buff=0.1)
            time_labels.append(label)

        # 矢印
        arrows = [
            Arrow(LEFT * 3 + DOWN * 1.3, ORIGIN + DOWN * 1.3, color=GRAY, buff=0.1),
            Arrow(ORIGIN + DOWN * 1.3, RIGHT * 3 + DOWN * 1.3, color=GRAY, buff=0.1),
        ]

        arrow_labels = [
            MathTex("T", font_size=24).next_to(arrows[0], DOWN, buff=0.1),
            MathTex("T", font_size=24).next_to(arrows[1], DOWN, buff=0.1),
        ]

        # アニメーション
        for i, (pulse, time_label) in enumerate(zip(pulses, time_labels)):
            self.play(Create(pulse), Write(time_label))
            if i < len(arrows):
                self.play(GrowArrow(arrows[i]), Write(arrow_labels[i]))
            self.wait(0.5)

        # 状態遷移の説明
        state_box = VGroup(
            MathTex(r"|g\rangle \xrightarrow{\pi/2} \frac{|g\rangle + |e\rangle}{\sqrt{2}}", font_size=28),
            MathTex(r"\xrightarrow{\pi} |g\rangle \leftrightarrow |e\rangle", font_size=28),
            MathTex(r"\xrightarrow{\pi/2} \text{干渉}", font_size=28),
        ).arrange(RIGHT, buff=0.5)
        state_box.to_edge(DOWN)

        self.play(Write(state_box))
        self.wait(2)
