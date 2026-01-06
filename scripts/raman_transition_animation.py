"""
ラマン遷移のアニメーション

2本のレーザーによる原子の内部状態と運動量の同時変化を視覚的に示す

使用方法:
    manim -pql raman_transition_animation.py RamanTransition
    manim -pqh raman_transition_animation.py RamanTransition  # 高画質
"""

from manim import *
import numpy as np


class RamanTransition(Scene):
    """ラマン遷移の基本原理を示すアニメーション"""

    def construct(self):
        # 色の設定
        GROUND_COLOR = BLUE
        EXCITED_COLOR = RED
        VIRTUAL_COLOR = GRAY
        LASER1_COLOR = "#FF6B6B"  # 赤めのレーザー
        LASER2_COLOR = "#4ECDC4"  # 緑がかったレーザー

        # タイトル
        title = Text("ラマン遷移", font_size=36, color=WHITE).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # ===== パート1: 2本のレーザー =====
        intro = Text(
            "周波数がわずかに違う2本のレーザーを照射",
            font_size=24,
            color=YELLOW,
        ).shift(UP * 2.2)
        self.play(Write(intro))

        # 原子
        atom = Circle(radius=0.4, color=GROUND_COLOR, fill_opacity=0.8)
        atom.shift(DOWN * 0.5)
        atom_label = MathTex("|g\\rangle", font_size=28, color=GROUND_COLOR)
        atom_label.next_to(atom, DOWN, buff=0.2)

        self.play(FadeIn(atom), Write(atom_label))

        # 2本のレーザー
        laser1 = Arrow(
            LEFT * 4 + UP * 1.5,
            atom.get_center() + UP * 0.2 + LEFT * 0.3,
            color=LASER1_COLOR,
            stroke_width=4,
        )
        laser1_label = MathTex(r"\omega_1", font_size=24, color=LASER1_COLOR)
        laser1_label.next_to(laser1.get_start(), UP, buff=0.1)

        laser2 = Arrow(
            LEFT * 4 + DOWN * 0.5,
            atom.get_center() + DOWN * 0.2 + LEFT * 0.3,
            color=LASER2_COLOR,
            stroke_width=4,
        )
        laser2_label = MathTex(r"\omega_2", font_size=24, color=LASER2_COLOR)
        laser2_label.next_to(laser2.get_start(), DOWN, buff=0.1)

        self.play(
            GrowArrow(laser1), Write(laser1_label),
            GrowArrow(laser2), Write(laser2_label),
        )
        self.wait(1)

        # 周波数差の説明
        freq_diff = MathTex(
            r"\omega_1 - \omega_2 \approx \omega_{hf}",
            font_size=28,
            color=YELLOW,
        ).shift(RIGHT * 3 + UP * 1)
        freq_diff_text = Text("（超微細構造の周波数差）", font_size=16, color=YELLOW)
        freq_diff_text.next_to(freq_diff, DOWN, buff=0.1)

        self.play(Write(freq_diff), Write(freq_diff_text))
        self.wait(1)

        # ===== パート2: 状態遷移 =====
        # レーザーの矢印はフェードアウト、テキストのみ縮小・移動
        upper_group = VGroup(intro, freq_diff, freq_diff_text)
        self.play(
            FadeOut(laser1), FadeOut(laser1_label),
            FadeOut(laser2), FadeOut(laser2_label),
            upper_group.animate.scale(0.6).to_edge(UP, buff=0.6),
            atom.animate.move_to(LEFT * 3 + DOWN * 0.5),
            atom_label.animate.next_to(LEFT * 3 + DOWN * 0.5, DOWN, buff=0.3),
        )

        # 遷移の矢印
        transition_arrow = Arrow(
            LEFT * 2, RIGHT * 2,
            color=YELLOW,
            stroke_width=4,
        ).shift(DOWN * 0.5)
        transition_label = Text("ラマン遷移", font_size=20, color=YELLOW)
        transition_label.next_to(transition_arrow, UP, buff=0.1)

        self.play(GrowArrow(transition_arrow), Write(transition_label))

        # 遷移後の原子
        atom_excited = Circle(radius=0.4, color=EXCITED_COLOR, fill_opacity=0.8)
        atom_excited.shift(RIGHT * 3 + DOWN * 0.5)
        atom_excited_label = MathTex("|e\\rangle", font_size=28, color=EXCITED_COLOR)
        atom_excited_label.next_to(atom_excited, DOWN, buff=0.2)

        # 運動量変化の矢印
        momentum_arrow = Arrow(
            atom_excited.get_center(),
            atom_excited.get_center() + RIGHT * 1.2,
            color=GREEN,
            stroke_width=5,
            buff=0.4,
        )
        momentum_label = MathTex(r"\hbar k_{eff}", font_size=24, color=GREEN)
        momentum_label.next_to(momentum_arrow, UP, buff=0.1)

        self.play(
            FadeIn(atom_excited),
            Write(atom_excited_label),
            GrowArrow(momentum_arrow),
            Write(momentum_label),
        )
        self.wait(1)

        # ===== パート3: 説明テキスト =====
        explanation = VGroup(
            Text("• 内部状態が変化: ", font_size=20, color=WHITE),
            MathTex(r"|g\rangle \rightarrow |e\rangle", font_size=24),
            Text("• 運動量が変化: ", font_size=20, color=WHITE),
            MathTex(r"p \rightarrow p + \hbar k_{eff}", font_size=24, color=GREEN),
        )
        explanation[0].next_to(explanation[1], LEFT, buff=0.1)
        explanation[2].next_to(explanation[3], LEFT, buff=0.1)

        row1 = VGroup(explanation[0], explanation[1]).arrange(RIGHT, buff=0.1)
        row2 = VGroup(explanation[2], explanation[3]).arrange(RIGHT, buff=0.1)
        explanation_group = VGroup(row1, row2).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        explanation_group.to_edge(DOWN, buff=0.8)

        self.play(Write(explanation_group))
        self.wait(2)

        # フェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class RamanEnergyDiagram(Scene):
    """ラマン遷移のエネルギー準位図"""

    def construct(self):
        GROUND_COLOR = BLUE
        EXCITED_COLOR = RED
        VIRTUAL_COLOR = GRAY
        LASER1_COLOR = "#FF6B6B"
        LASER2_COLOR = "#4ECDC4"

        # タイトル
        title = Text("ラマン遷移のエネルギー準位図", font_size=32, color=WHITE).to_edge(UP)
        self.play(Write(title))

        # エネルギー準位
        # 基底状態 |g⟩
        ground_level = Line(LEFT * 2, RIGHT * 0.5, color=GROUND_COLOR, stroke_width=4)
        ground_level.shift(DOWN * 2)
        ground_label = MathTex("|g\\rangle", font_size=28, color=GROUND_COLOR)
        ground_label.next_to(ground_level, LEFT, buff=0.3)

        # 励起状態 |e⟩（運動量変化後）
        excited_level = Line(LEFT * 0.5, RIGHT * 2, color=EXCITED_COLOR, stroke_width=4)
        excited_level.shift(DOWN * 1.2)
        excited_label = MathTex("|e\\rangle", font_size=28, color=EXCITED_COLOR)
        excited_label.next_to(excited_level, RIGHT, buff=0.3)

        # 仮想準位
        virtual_level = DashedLine(LEFT * 2.5, RIGHT * 2.5, color=VIRTUAL_COLOR, stroke_width=2)
        virtual_level.shift(UP * 1.5)
        virtual_label = Text("仮想準位", font_size=18, color=VIRTUAL_COLOR)
        virtual_label.next_to(virtual_level, RIGHT, buff=0.3)

        self.play(
            Create(ground_level), Write(ground_label),
            Create(excited_level), Write(excited_label),
            Create(virtual_level), Write(virtual_label),
        )
        self.wait(0.5)

        # エネルギー差のブラケット
        energy_brace = BraceBetweenPoints(
            ground_level.get_right() + RIGHT * 0.2 + DOWN * 0.1,
            excited_level.get_left() + LEFT * 0.2 + UP * 0.1,
            direction=RIGHT,
        )
        energy_label = MathTex(r"\hbar \omega_{hf}", font_size=22)
        energy_label.next_to(energy_brace, RIGHT, buff=0.1)

        self.play(Create(energy_brace), Write(energy_label))
        self.wait(0.5)

        # 原子（基底状態）
        atom = Dot(ground_level.get_center(), color=GROUND_COLOR, radius=0.15)
        self.play(FadeIn(atom))
        self.wait(0.5)

        # レーザー1（上向き、吸収）
        laser1_arrow = Arrow(
            ground_level.get_center() + DOWN * 0.3,
            virtual_level.get_center() + LEFT * 1 + DOWN * 0.3,
            color=LASER1_COLOR,
            stroke_width=3,
        )
        laser1_label = MathTex(r"\omega_1", font_size=22, color=LASER1_COLOR)
        laser1_label.next_to(laser1_arrow, LEFT, buff=0.1)

        laser1_text = Text("吸収", font_size=16, color=LASER1_COLOR)
        laser1_text.next_to(laser1_label, DOWN, buff=0.1)

        self.play(GrowArrow(laser1_arrow), Write(laser1_label), Write(laser1_text))

        # 原子が仮想準位へ
        self.play(atom.animate.move_to(virtual_level.get_center() + LEFT * 1))
        self.wait(0.3)

        # レーザー2（下向き、誘導放出）
        laser2_arrow = Arrow(
            virtual_level.get_center() + RIGHT * 1 + UP * 0.3,
            excited_level.get_center() + UP * 0.3,
            color=LASER2_COLOR,
            stroke_width=3,
        )
        laser2_label = MathTex(r"\omega_2", font_size=22, color=LASER2_COLOR)
        laser2_label.next_to(laser2_arrow, RIGHT, buff=0.1)

        laser2_text = Text("誘導放出", font_size=16, color=LASER2_COLOR)
        laser2_text.next_to(laser2_label, DOWN, buff=0.1)

        self.play(GrowArrow(laser2_arrow), Write(laser2_label), Write(laser2_text))

        # 原子が励起状態へ
        self.play(
            atom.animate.move_to(excited_level.get_center()).set_color(EXCITED_COLOR),
        )
        self.wait(0.5)

        # 運動量変化の説明
        momentum_box = VGroup(
            Text("運動量変化:", font_size=20, color=WHITE),
            MathTex(r"\Delta p = \hbar(k_1 - k_2) = \hbar k_{eff}", font_size=24, color=GREEN),
        ).arrange(DOWN, buff=0.15)
        momentum_box.to_edge(DOWN, buff=0.5)

        box = SurroundingRectangle(momentum_box, color=GREEN, buff=0.2)

        self.play(Write(momentum_box), Create(box))
        self.wait(2)

        # フェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class RamanStates(Scene):
    """基底状態|g⟩と励起状態|e⟩の説明"""

    def construct(self):
        GROUND_COLOR = BLUE
        EXCITED_COLOR = RED

        # タイトル
        title = Text("ラマン遷移による状態変化", font_size=32, color=WHITE).to_edge(UP)
        self.play(Write(title))

        # ===== 左側: 基底状態 =====
        ground_box = VGroup()

        ground_title = Text("基底状態", font_size=24, color=GROUND_COLOR)
        ground_ket = MathTex("|g\\rangle", font_size=48, color=GROUND_COLOR)

        ground_atom = Circle(radius=0.5, color=GROUND_COLOR, fill_opacity=0.7)
        ground_momentum = Arrow(
            ground_atom.get_center(),
            ground_atom.get_center() + RIGHT * 0.8,
            color=WHITE,
            stroke_width=3,
            buff=0.5,
        )
        ground_p_label = MathTex("p", font_size=24, color=WHITE)
        ground_p_label.next_to(ground_momentum, UP, buff=0.05)

        ground_desc = Text("運動量そのまま", font_size=18, color=WHITE)

        ground_box.add(ground_title, ground_ket, ground_atom, ground_momentum, ground_p_label, ground_desc)
        ground_title.shift(UP * 1.5)
        ground_ket.shift(UP * 0.7)
        ground_atom.shift(DOWN * 0.3)
        ground_momentum.next_to(ground_atom, RIGHT, buff=0.1)
        ground_p_label.next_to(ground_momentum, UP, buff=0.05)
        ground_desc.shift(DOWN * 1.5)

        ground_box.shift(LEFT * 3.5)

        # ===== 右側: 励起状態 =====
        excited_box = VGroup()

        excited_title = Text("励起状態", font_size=24, color=EXCITED_COLOR)
        excited_ket = MathTex("|e\\rangle", font_size=48, color=EXCITED_COLOR)

        excited_atom = Circle(radius=0.5, color=EXCITED_COLOR, fill_opacity=0.7)
        excited_momentum = Arrow(
            excited_atom.get_center(),
            excited_atom.get_center() + RIGHT * 1.5,
            color=GREEN,
            stroke_width=4,
            buff=0.5,
        )
        excited_p_label = MathTex(r"p + \hbar k_{eff}", font_size=22, color=GREEN)
        excited_p_label.next_to(excited_momentum, UP, buff=0.05)

        excited_desc = Text("運動量が変化", font_size=18, color=GREEN)

        excited_box.add(excited_title, excited_ket, excited_atom, excited_momentum, excited_p_label, excited_desc)
        excited_title.shift(UP * 1.5)
        excited_ket.shift(UP * 0.7)
        excited_atom.shift(DOWN * 0.3)
        excited_momentum.next_to(excited_atom, RIGHT, buff=0.1)
        excited_p_label.next_to(excited_momentum, UP, buff=0.05)
        excited_desc.shift(DOWN * 1.5)

        excited_box.shift(RIGHT * 3.5)

        # アニメーション
        self.play(
            Write(ground_title), Write(ground_ket),
            Write(excited_title), Write(excited_ket),
        )
        self.play(
            FadeIn(ground_atom), FadeIn(excited_atom),
        )
        self.play(
            GrowArrow(ground_momentum), Write(ground_p_label),
            GrowArrow(excited_momentum), Write(excited_p_label),
        )
        self.play(
            Write(ground_desc), Write(excited_desc),
        )
        self.wait(1)

        # 遷移矢印
        transition = Arrow(LEFT * 1.5, RIGHT * 1.5, color=YELLOW, stroke_width=4)
        transition_label = Text("ラマン遷移", font_size=20, color=YELLOW)
        transition_label.next_to(transition, UP, buff=0.1)

        self.play(GrowArrow(transition), Write(transition_label))
        self.wait(1)

        # 補足説明
        note = VGroup(
            Text("内部状態と運動量が", font_size=22, color=WHITE),
            Text("同時に変化する", font_size=22, color=YELLOW),
        ).arrange(DOWN, buff=0.1)
        note.to_edge(DOWN, buff=0.5)

        box = SurroundingRectangle(note, color=YELLOW, buff=0.2)

        self.play(Write(note), Create(box))
        self.wait(2)

        # フェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class RamanTransitionCombined(Scene):
    """ラマン遷移の完全版アニメーション"""

    def construct(self):
        GROUND_COLOR = BLUE
        EXCITED_COLOR = RED
        LASER1_COLOR = "#FF6B6B"
        LASER2_COLOR = "#4ECDC4"

        # タイトル
        title = Text("ラマン遷移", font_size=36, color=WHITE).to_edge(UP)
        self.play(Write(title))

        # 説明テキスト
        intro = Text(
            "2本のレーザーで原子の状態と運動量を同時に変化",
            font_size=22,
            color=YELLOW,
        ).shift(UP * 2.3)
        self.play(Write(intro))

        # ===== 左側: 遷移前 =====
        before_label = Text("遷移前", font_size=20, color=WHITE).shift(LEFT * 4 + UP * 1)

        atom_before = Circle(radius=0.4, color=GROUND_COLOR, fill_opacity=0.8)
        atom_before.shift(LEFT * 4)
        state_before = MathTex("|g\\rangle", font_size=32, color=GROUND_COLOR)
        state_before.next_to(atom_before, DOWN, buff=0.2)

        p_before = Arrow(
            atom_before.get_center(),
            atom_before.get_center() + RIGHT * 0.8,
            color=WHITE,
            stroke_width=3,
            buff=0.4,
        )
        p_before_label = MathTex("p", font_size=22, color=WHITE)
        p_before_label.next_to(p_before, UP, buff=0.05)

        self.play(
            Write(before_label),
            FadeIn(atom_before), Write(state_before),
            GrowArrow(p_before), Write(p_before_label),
        )

        # ===== 中央: レーザー照射 =====
        laser_box = Rectangle(width=2.5, height=3, color=YELLOW, stroke_width=2)
        laser_box_label = Text("レーザー照射", font_size=18, color=YELLOW)
        laser_box_label.next_to(laser_box, UP, buff=0.1)

        laser1_line = Arrow(LEFT * 1, RIGHT * 0.3, color=LASER1_COLOR, stroke_width=3)
        laser1_line.shift(UP * 0.5)
        laser1_freq = MathTex(r"\omega_1", font_size=20, color=LASER1_COLOR)
        laser1_freq.next_to(laser1_line, UP, buff=0.05)

        laser2_line = Arrow(LEFT * 1, RIGHT * 0.3, color=LASER2_COLOR, stroke_width=3)
        laser2_line.shift(DOWN * 0.5)
        laser2_freq = MathTex(r"\omega_2", font_size=20, color=LASER2_COLOR)
        laser2_freq.next_to(laser2_line, DOWN, buff=0.05)

        self.play(
            Create(laser_box), Write(laser_box_label),
            GrowArrow(laser1_line), Write(laser1_freq),
            GrowArrow(laser2_line), Write(laser2_freq),
        )

        # ===== 右側: 遷移後 =====
        after_label = Text("遷移後", font_size=20, color=WHITE).shift(RIGHT * 4 + UP * 1)

        atom_after = Circle(radius=0.4, color=EXCITED_COLOR, fill_opacity=0.8)
        atom_after.shift(RIGHT * 4)
        state_after = MathTex("|e\\rangle", font_size=32, color=EXCITED_COLOR)
        state_after.next_to(atom_after, DOWN, buff=0.2)

        p_after = Arrow(
            atom_after.get_center(),
            atom_after.get_center() + RIGHT * 1.5,
            color=GREEN,
            stroke_width=4,
            buff=0.4,
        )
        p_after_label = MathTex(r"p + \hbar k_{eff}", font_size=20, color=GREEN)
        p_after_label.next_to(p_after, UP, buff=0.05)

        self.play(
            Write(after_label),
            FadeIn(atom_after), Write(state_after),
            GrowArrow(p_after), Write(p_after_label),
        )

        # 遷移矢印
        arrow1 = Arrow(LEFT * 2.8, LEFT * 1.3, color=WHITE, stroke_width=2)
        arrow2 = Arrow(RIGHT * 1.3, RIGHT * 2.8, color=WHITE, stroke_width=2)

        self.play(GrowArrow(arrow1), GrowArrow(arrow2))
        self.wait(1)

        # 結論ボックス
        conclusion = VGroup(
            MathTex(r"|g\rangle \xrightarrow{\text{Raman}} |e\rangle", font_size=28),
            MathTex(r"p \rightarrow p + \hbar k_{eff}", font_size=28, color=GREEN),
        ).arrange(DOWN, buff=0.2)
        conclusion.to_edge(DOWN, buff=0.5)

        box = SurroundingRectangle(conclusion, color=YELLOW, buff=0.2)

        self.play(Write(conclusion), Create(box))
        self.wait(2)

        # フェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects])
