"""
レーザー冷却の原理アニメーション

原子干渉計で使用されるレーザー冷却の仕組みを視覚的に説明する

使用方法:
    manim -pql laser_cooling_animation.py LaserCoolingPrinciple
    manim -pqh laser_cooling_animation.py LaserCoolingPrinciple  # 高画質
    manim -pql laser_cooling_animation.py DopplerCooling
    manim -pql laser_cooling_animation.py LaserCoolingComplete
"""

from manim import *
import numpy as np


class LaserCoolingPrinciple(Scene):
    """レーザー冷却の基本原理：光子の運動量移行"""

    def construct(self):
        # タイトル
        title = Text("レーザー冷却の原理", font_size=36).to_edge(UP)
        self.play(Write(title))

        # 原子を表す円
        atom = Circle(radius=0.4, color=BLUE, fill_opacity=0.8)
        atom.shift(RIGHT * 2)
        atom_label = Text("原子", font_size=20).next_to(atom, UP, buff=0.2)

        # 原子の速度ベクトル
        velocity_arrow = Arrow(
            atom.get_center(),
            atom.get_center() + RIGHT * 1.5,
            color=GREEN,
            buff=0,
            stroke_width=5,
        )
        velocity_label = MathTex("v", font_size=28, color=GREEN).next_to(
            velocity_arrow, UP, buff=0.1
        )

        # 原子とベクトルをグループ化（説明テキストと被らないよう上に配置）
        atom_group = VGroup(atom, atom_label, velocity_arrow, velocity_label)
        atom_group.move_to(UP * 0.8)

        self.play(FadeIn(atom), Write(atom_label))
        self.play(GrowArrow(velocity_arrow), Write(velocity_label))
        self.wait(1)

        # ステップ1：光子が向かってくる
        step1_text = Text("① 逆向きから光子を照射", font_size=24, color=YELLOW)
        step1_text.to_edge(DOWN, buff=1.5)
        self.play(Write(step1_text))

        # 光子（波として表現）- 原子の進行方向（右）の前方から逆向きに照射
        photon_start = RIGHT * 5
        photon = self.create_photon_wave(photon_start, atom.get_center() + RIGHT * 0.5)
        photon_arrow = Arrow(
            photon_start + LEFT * 0.5,
            atom.get_center() + RIGHT * 0.5,
            color=RED,
            buff=0,
            stroke_width=3,
        )
        photon_label = Text("光子", font_size=18, color=RED).next_to(
            photon_start + LEFT * 1.5, UP
        )

        self.play(Create(photon), GrowArrow(photon_arrow), Write(photon_label))
        self.wait(0.5)

        # 光子が原子に吸収される
        self.play(
            photon.animate.move_to(atom.get_center()),
            photon_arrow.animate.put_start_and_end_on(
                atom.get_center() + RIGHT * 0.5, atom.get_center()
            ),
            FadeOut(photon_label),
            run_time=1,
        )

        # 吸収のフラッシュ効果
        flash = Circle(radius=0.1, color=YELLOW, fill_opacity=1)
        flash.move_to(atom.get_center())
        self.play(
            flash.animate.scale(3).set_opacity(0),
            atom.animate.set_color(PURPLE),
            FadeOut(photon),
            FadeOut(photon_arrow),
            run_time=0.5,
        )
        self.remove(flash)

        # ステップ2：運動量移行
        step1_text_new = Text("② 光子の運動量を受け取る → 減速", font_size=24, color=YELLOW)
        step1_text_new.to_edge(DOWN, buff=1.5)
        self.play(ReplacementTransform(step1_text, step1_text_new))

        # 速度ベクトルが短くなる
        new_velocity_arrow = Arrow(
            atom.get_center(),
            atom.get_center() + RIGHT * 0.8,
            color=GREEN,
            buff=0,
            stroke_width=5,
        )

        self.play(
            ReplacementTransform(velocity_arrow, new_velocity_arrow),
            velocity_label.animate.next_to(
                atom.get_center() + RIGHT * 0.4, UP, buff=0.1
            ),
        )
        self.wait(1)

        # ステップ3：自然放出
        step2_text = Text("③ 光子を自然放出（ランダム方向）", font_size=24, color=YELLOW)
        step2_text.to_edge(DOWN, buff=1.5)
        self.play(ReplacementTransform(step1_text_new, step2_text))

        # 放出される光子（ランダム方向に複数）
        emission_arrows = VGroup()
        for angle in [30, 120, 210, 300]:
            direction = np.array(
                [np.cos(np.radians(angle)), np.sin(np.radians(angle)), 0]
            )
            arrow = Arrow(
                atom.get_center(),
                atom.get_center() + direction * 1.0,
                color=ORANGE,
                buff=0.4,
                stroke_width=2,
            )
            emission_arrows.add(arrow)

        self.play(
            atom.animate.set_color(BLUE),
            *[GrowArrow(arr) for arr in emission_arrows],
        )
        self.wait(1)

        # 説明テキスト
        explanation = VGroup(
            Text("• 吸収は常に逆向き → 一方向に減速", font_size=22),
            Text("• 放出はランダム → 平均するとゼロ", font_size=22),
            Text("• 繰り返すと原子が減速する", font_size=22, color=BLUE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        explanation.next_to(step2_text, UP, buff=0.5)

        self.play(FadeOut(emission_arrows))
        self.play(Write(explanation))
        self.wait(3)

    def create_photon_wave(self, start, end):
        """光子を波として表現"""
        path = Line(start, end)
        wave = VGroup()
        num_waves = 8

        for i in range(num_waves):
            t_start = i / num_waves
            t_end = (i + 1) / num_waves
            if i % 2 == 0:
                arc = ArcBetweenPoints(
                    path.point_from_proportion(t_start),
                    path.point_from_proportion(t_end),
                    angle=TAU / 4,
                    color=RED,
                )
            else:
                arc = ArcBetweenPoints(
                    path.point_from_proportion(t_start),
                    path.point_from_proportion(t_end),
                    angle=-TAU / 4,
                    color=RED,
                )
            wave.add(arc)

        return wave


class DopplerCooling(Scene):
    """ドップラー効果を利用した冷却原理"""

    def construct(self):
        # タイトル
        title = Text("ドップラー冷却の原理", font_size=36).to_edge(UP)
        self.play(Write(title))

        # 中央に周波数の説明
        freq_explanation = VGroup(
            MathTex(r"\nu_{\text{laser}} < \nu_0", font_size=32, color=RED),
            Text("（赤方偏移したレーザーを使用）", font_size=22),
        ).arrange(DOWN, buff=0.2)
        freq_explanation.shift(UP * 2)
        self.play(Write(freq_explanation))
        self.wait(1)

        # 軸（原子の速度を表す）
        axis = NumberLine(
            x_range=[-3, 3, 1],
            length=10,
            include_numbers=False,
            include_tip=True,
        ).shift(DOWN * 0.5)

        axis_label = Text("原子の速度", font_size=20).next_to(axis, DOWN)
        left_label = Text("← レーザー側へ", font_size=18, color=BLUE).next_to(
            axis.get_left(), DOWN
        )
        right_label = Text("レーザーから離れる →", font_size=18, color=GRAY).next_to(
            axis.get_right(), DOWN
        )

        self.play(Create(axis), Write(axis_label), Write(left_label), Write(right_label))

        # レーザー光源
        laser = VGroup(
            Rectangle(width=0.8, height=0.4, color=RED, fill_opacity=0.8),
            Text("レーザー", font_size=14, color=WHITE),
        ).arrange(DOWN, buff=0.1)
        laser.move_to(LEFT * 6)

        laser_beam = DashedLine(
            LEFT * 5.5, RIGHT * 5, color=RED, stroke_width=2, dash_length=0.2
        )
        self.play(FadeIn(laser), Create(laser_beam))

        # ケース1: 近づく原子（青方偏移 → 共鳴）
        case1_title = Text("近づく原子", font_size=22, color=BLUE).shift(
            DOWN * 2 + LEFT * 3
        )
        case1_atom = Circle(radius=0.25, color=BLUE, fill_opacity=0.8)
        case1_atom.shift(DOWN * 0.5 + LEFT * 2)
        case1_arrow = Arrow(
            case1_atom.get_center() + LEFT * 0.5,
            case1_atom.get_center(),
            color=BLUE,
            buff=0,
            stroke_width=4,
        )

        case1_explanation = VGroup(
            Text("青方偏移 → 共鳴", font_size=18, color=BLUE),
            Text("光子を吸収 → 減速", font_size=18, color=GREEN),
        ).arrange(DOWN, buff=0.1)
        case1_explanation.next_to(case1_title, DOWN, buff=0.3)

        # ケース2: 遠ざかる原子（赤方偏移 → 非共鳴）
        case2_title = Text("遠ざかる原子", font_size=22, color=GRAY).shift(
            DOWN * 2 + RIGHT * 3
        )
        case2_atom = Circle(radius=0.25, color=GRAY, fill_opacity=0.5)
        case2_atom.shift(DOWN * 0.5 + RIGHT * 2)
        case2_arrow = Arrow(
            case2_atom.get_center(),
            case2_atom.get_center() + RIGHT * 0.5,
            color=GRAY,
            buff=0,
            stroke_width=4,
        )

        case2_explanation = VGroup(
            Text("さらに赤方偏移 → 非共鳴", font_size=18, color=GRAY),
            Text("光子を吸収しない", font_size=18, color=GRAY),
        ).arrange(DOWN, buff=0.1)
        case2_explanation.next_to(case2_title, DOWN, buff=0.3)

        # アニメーション
        self.play(Write(case1_title), FadeIn(case1_atom), GrowArrow(case1_arrow))
        self.play(Write(case1_explanation))
        self.wait(1)

        self.play(Write(case2_title), FadeIn(case2_atom), GrowArrow(case2_arrow))
        self.play(Write(case2_explanation))
        self.wait(1)

        # 結論
        conclusion = VGroup(
            Text("結果:", font_size=24, color=YELLOW),
            Text("「速い原子だけ」が減速される", font_size=24, color=YELLOW),
            Text("→ 速度分布が狭くなる = 冷却", font_size=24, color=BLUE),
        ).arrange(DOWN, buff=0.2)
        conclusion.to_edge(DOWN, buff=0.5)

        self.play(Write(conclusion))
        self.wait(3)


class LaserCoolingComplete(Scene):
    """レーザー冷却の完全なアニメーション：複数回の吸収・放出サイクル"""

    def construct(self):
        # タイトル
        title = Text("レーザー冷却サイクル", font_size=32).to_edge(UP)
        self.play(Write(title))

        # 原子
        atom = Circle(radius=0.35, color=BLUE, fill_opacity=0.8)
        atom.shift(RIGHT * 2)

        # 初期速度（速い）
        velocity = 2.0
        velocity_tracker = ValueTracker(velocity)

        # 速度ベクトル（動的に更新）
        velocity_arrow = always_redraw(
            lambda: Arrow(
                atom.get_center(),
                atom.get_center() + RIGHT * velocity_tracker.get_value() * 0.8,
                color=self.velocity_color(velocity_tracker.get_value()),
                buff=0,
                stroke_width=5,
            )
        )

        # 速度表示
        velocity_label = always_redraw(
            lambda: Text(
                f"v = {velocity_tracker.get_value():.1f}",
                font_size=24,
                color=self.velocity_color(velocity_tracker.get_value()),
            ).to_corner(UR)
        )

        # レーザー光源（右側 = 原子の進行方向の前方から逆向きに照射）
        laser_right = VGroup(
            Polygon(
                RIGHT * 0.3 + UP * 0.2,
                LEFT * 0.3,
                RIGHT * 0.3 + DOWN * 0.2,
                color=RED,
                fill_opacity=0.8,
            ),
        )
        laser_right.move_to(RIGHT * 5)
        laser_label = Text("赤方偏移\nレーザー", font_size=14, color=RED).next_to(
            laser_right, DOWN
        )

        # レーザービーム（右から左へ）
        laser_beam = DashedLine(
            RIGHT * 4.5, LEFT * 4, color=RED, stroke_width=2, dash_length=0.15
        ).shift(DOWN * 0.1)

        self.play(FadeIn(atom), Create(velocity_arrow), Write(velocity_label))
        self.play(FadeIn(laser_right), Write(laser_label), Create(laser_beam))
        self.wait(1)

        # サイクルカウンター
        cycle_counter = Text("サイクル: 0", font_size=24).to_corner(UL)
        self.play(Write(cycle_counter))

        # 5サイクルの冷却アニメーション
        for cycle in range(5):
            # 光子が右側から飛んでくる（原子の進行方向と逆向き）
            photon = Dot(color=RED, radius=0.1)
            photon.move_to(RIGHT * 4)

            self.play(
                photon.animate.move_to(atom.get_center()),
                run_time=0.4,
            )

            # 吸収（原子が光る）
            self.play(
                Flash(atom, color=YELLOW, line_length=0.3, num_lines=8, run_time=0.3),
                atom.animate.set_color(PURPLE),
                FadeOut(photon),
            )

            # 減速（速度ベクトルが短くなる）
            new_velocity = velocity_tracker.get_value() * 0.75
            self.play(
                velocity_tracker.animate.set_value(new_velocity),
                run_time=0.3,
            )

            # 自然放出（ランダム方向）
            emission_angle = np.random.uniform(0, 2 * np.pi)
            emission_dir = np.array(
                [np.cos(emission_angle), np.sin(emission_angle), 0]
            )
            emitted_photon = Dot(color=ORANGE, radius=0.08)
            emitted_photon.move_to(atom.get_center())

            self.play(
                atom.animate.set_color(BLUE),
                emitted_photon.animate.move_to(atom.get_center() + emission_dir * 2),
                run_time=0.3,
            )
            self.remove(emitted_photon)

            # カウンター更新
            new_counter = Text(f"サイクル: {cycle + 1}", font_size=24).to_corner(UL)
            self.play(
                ReplacementTransform(cycle_counter, new_counter),
                run_time=0.2,
            )
            cycle_counter = new_counter

        self.wait(1)

        # 結果の説明
        result = VGroup(
            Text("結果:", font_size=28, color=YELLOW),
            Text(f"初期速度: 2.0 → 最終速度: {velocity_tracker.get_value():.2f}", font_size=24),
            Text("5サイクルで約75%減速", font_size=24, color=BLUE),
        ).arrange(DOWN, buff=0.2)
        result.to_edge(DOWN, buff=0.8)

        self.play(Write(result))
        self.wait(3)

    def velocity_color(self, v):
        """速度に応じた色（速い=赤、遅い=青）"""
        ratio = min(1, v / 2.0)
        return interpolate_color(BLUE, RED, ratio)


class MOTAnimation(Scene):
    """磁気光学トラップ（MOT）の概念図"""

    def construct(self):
        # タイトル
        title = Text("磁気光学トラップ（MOT）", font_size=32).to_edge(UP)
        subtitle = Text("6方向からレーザーを照射", font_size=24, color=YELLOW).next_to(
            title, DOWN
        )
        self.play(Write(title), Write(subtitle))

        # 中央の原子雲
        atom_cloud = VGroup()
        np.random.seed(42)
        for _ in range(30):
            atom = Dot(
                point=np.random.randn(3) * 0.5,
                color=BLUE,
                radius=0.05,
            )
            atom_cloud.add(atom)

        self.play(FadeIn(atom_cloud))

        # 6方向のレーザービーム
        directions = [
            (LEFT, "x-"),
            (RIGHT, "x+"),
            (UP, "y+"),
            (DOWN, "y-"),
            (OUT * 0.7 + UP * 0.3, "z+"),  # 3D効果を出すため斜めに
            (IN * 0.7 + DOWN * 0.3, "z-"),
        ]

        laser_beams = VGroup()
        laser_arrows = VGroup()

        for direction, label in directions:
            # レーザービーム（矢印）
            start = direction * 3
            end = ORIGIN

            arrow = Arrow(
                start,
                end,
                color=RED,
                buff=0.3,
                stroke_width=4,
            )
            laser_arrows.add(arrow)

            # ビーム（破線）
            beam = DashedLine(start, end * 0.3, color=RED, stroke_width=2)
            laser_beams.add(beam)

        self.play(
            *[GrowArrow(arr) for arr in laser_arrows],
            *[Create(beam) for beam in laser_beams],
        )
        self.wait(1)

        # 原子が中央に集まる効果
        for _ in range(3):
            self.play(
                *[atom.animate.move_to(atom.get_center() * 0.7) for atom in atom_cloud],
                run_time=0.5,
            )

        # 冷却される原子雲（縮小）
        self.play(
            atom_cloud.animate.scale(0.5),
            run_time=1,
        )

        # 説明
        explanation = VGroup(
            Text("• 各方向から赤方偏移レーザーを照射", font_size=22),
            Text("• どの方向に動いても減速される", font_size=22),
            Text("• 磁場勾配で中央に閉じ込め", font_size=22),
            Text("• 到達温度: 数μK〜数十μK", font_size=22, color=BLUE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        explanation.to_edge(DOWN, buff=0.5)

        self.play(Write(explanation))
        self.wait(3)


class LaserCoolingEnergyDiagram(Scene):
    """レーザー冷却のエネルギー準位図"""

    def construct(self):
        # タイトル
        title = Text("レーザー冷却とエネルギー準位", font_size=32).to_edge(UP)
        self.play(Write(title))

        # エネルギー準位
        ground_state = Line(LEFT * 2, RIGHT * 2, color=WHITE, stroke_width=3)
        ground_state.shift(DOWN * 1.5)
        ground_label = Text("基底状態", font_size=20).next_to(ground_state, LEFT)

        excited_state = Line(LEFT * 2, RIGHT * 2, color=WHITE, stroke_width=3)
        excited_state.shift(UP * 1.5)
        excited_label = Text("励起状態", font_size=20).next_to(excited_state, LEFT)

        self.play(
            Create(ground_state),
            Create(excited_state),
            Write(ground_label),
            Write(excited_label),
        )

        # 原子（基底状態）
        atom = Dot(color=BLUE, radius=0.15)
        atom.move_to(ground_state.get_center())

        self.play(FadeIn(atom))
        self.wait(1)

        # ステップ1: 光子吸収
        step1 = Text("① 光子吸収", font_size=24, color=YELLOW).to_corner(UL)
        self.play(Write(step1))

        # 光子が飛んでくる
        photon_path = Arrow(
            LEFT * 4 + DOWN * 1.5,
            atom.get_center() + LEFT * 0.3,
            color=RED,
            stroke_width=3,
        )
        photon_wave = Text("ℏω", font_size=20, color=RED).next_to(photon_path, UP)

        self.play(GrowArrow(photon_path), Write(photon_wave))

        # 原子が励起状態に遷移
        transition_arrow = Arrow(
            ground_state.get_center(),
            excited_state.get_center(),
            color=RED,
            buff=0.3,
        )

        self.play(
            atom.animate.move_to(excited_state.get_center()),
            atom.animate.set_color(PURPLE),
            FadeIn(transition_arrow),
            FadeOut(photon_path),
            FadeOut(photon_wave),
            run_time=1,
        )
        self.wait(1)

        # ステップ2: 自然放出
        step2 = Text("② 自然放出", font_size=24, color=YELLOW).next_to(step1, DOWN)
        self.play(Write(step2))

        # ランダム方向に光子を放出
        emission_arrow = Arrow(
            excited_state.get_center(),
            ground_state.get_center(),
            color=ORANGE,
            buff=0.3,
        )
        emitted_photon = Arrow(
            atom.get_center() + RIGHT * 0.3,
            RIGHT * 4 + UP * 1,
            color=ORANGE,
            stroke_width=2,
        )

        self.play(
            atom.animate.move_to(ground_state.get_center()),
            atom.animate.set_color(BLUE),
            ReplacementTransform(transition_arrow, emission_arrow),
            GrowArrow(emitted_photon),
            run_time=1,
        )
        self.wait(1)

        # 運動量の説明
        momentum_box = VGroup(
            Text("運動量変化:", font_size=22),
            MathTex(r"\Delta p_{\text{吸収}} = -\hbar k", font_size=24, color=RED),
            Text("（一方向に減速）", font_size=18, color=RED),
            MathTex(
                r"\langle \Delta p_{\text{放出}} \rangle = 0", font_size=24, color=ORANGE
            ),
            Text("（ランダムで平均ゼロ）", font_size=18, color=ORANGE),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        momentum_box.to_edge(RIGHT).shift(DOWN * 0.5)

        self.play(Write(momentum_box))
        self.wait(1)

        # 結論
        conclusion = Text(
            "繰り返すと正味で減速 → 冷却",
            font_size=26,
            color=BLUE,
        ).to_edge(DOWN, buff=0.5)

        self.play(Write(conclusion))
        self.wait(3)


class DopplerSelectiveCooling(Scene):
    """ドップラー効果による選択的冷却の詳細図解"""

    def construct(self):
        # タイトル
        title = Text("ドップラー効果による選択的減速", font_size=32, color=WHITE).to_edge(UP)
        self.play(Write(title))

        # ===== パート1: 周波数の説明 =====
        freq_title = Text("レーザー周波数の設定", font_size=24, color=YELLOW).shift(UP * 2.2)
        self.play(Write(freq_title))

        # 周波数軸
        freq_axis = NumberLine(
            x_range=[0, 10, 2],
            length=8,
            include_numbers=False,
            include_tip=True,
        ).shift(UP * 1)

        freq_label = MathTex(r"\nu", font_size=28).next_to(freq_axis.get_right(), RIGHT)
        self.play(Create(freq_axis), Write(freq_label))

        # 共鳴周波数
        resonance_pos = freq_axis.n2p(6)
        resonance_line = DashedLine(
            resonance_pos + UP * 0.5,
            resonance_pos + DOWN * 0.5,
            color=WHITE,
            stroke_width=2,
        )
        resonance_label = MathTex(r"\nu_0", font_size=24, color=WHITE).next_to(resonance_line, UP)
        resonance_text = Text("共鳴周波数", font_size=16, color=WHITE).next_to(resonance_label, UP, buff=0.1)

        # レーザー周波数（共鳴より低い = 赤方偏移）
        laser_pos = freq_axis.n2p(4)
        laser_line = Line(
            laser_pos + UP * 0.4,
            laser_pos + DOWN * 0.4,
            color=RED,
            stroke_width=4,
        )
        laser_label = MathTex(r"\nu_L", font_size=24, color=RED).next_to(laser_line, DOWN)
        laser_text = Text("レーザー", font_size=16, color=RED).next_to(laser_label, DOWN, buff=0.1)

        self.play(
            Create(resonance_line), Write(resonance_label), Write(resonance_text),
            Create(laser_line), Write(laser_label), Write(laser_text),
        )

        # 赤方偏移の説明
        offset_brace = BraceBetweenPoints(laser_pos, resonance_pos, direction=DOWN)
        offset_label = Text("赤方偏移", font_size=16, color=YELLOW).next_to(offset_brace, DOWN, buff=0.1)

        self.play(Create(offset_brace), Write(offset_label))
        self.wait(1)

        # 上部をまとめて縮小・移動
        freq_group = VGroup(
            freq_title, freq_axis, freq_label,
            resonance_line, resonance_label, resonance_text,
            laser_line, laser_label, laser_text,
            offset_brace, offset_label
        )
        self.play(freq_group.animate.scale(0.7).to_edge(UP, buff=0.5))

        # ===== パート2: 近づく原子 =====
        # ボックスタイトル
        approaching_title = Text("① 近づく原子", font_size=22, color=BLUE).shift(LEFT * 3.5 + UP * 0.5)

        # 原子とレーザーの図
        laser_left = Arrow(LEFT * 5.5, LEFT * 2.5, color=RED, stroke_width=4)
        laser_left.shift(DOWN * 0.5)
        laser_left_label = Text("レーザー", font_size=14, color=RED).next_to(laser_left, UP, buff=0.1)

        atom_approaching = Circle(radius=0.25, color=BLUE, fill_opacity=0.8)
        atom_approaching.shift(LEFT * 2 + DOWN * 0.5)

        atom_vel = Arrow(
            atom_approaching.get_center(),
            atom_approaching.get_center() + LEFT * 0.8,
            color=GREEN, buff=0, stroke_width=4
        )
        vel_label = MathTex("v", font_size=20, color=GREEN).next_to(atom_vel, UP, buff=0.05)

        self.play(
            Write(approaching_title),
            GrowArrow(laser_left), Write(laser_left_label),
            FadeIn(atom_approaching), GrowArrow(atom_vel), Write(vel_label),
        )

        # ドップラー効果の説明
        doppler_up = VGroup(
            Text("原子から見ると:", font_size=16, color=WHITE),
            MathTex(r"\nu' = \nu_L + \Delta\nu", font_size=22, color=BLUE),
            Text("青方偏移 → 共鳴!", font_size=18, color=BLUE),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        doppler_up.next_to(atom_approaching, DOWN, buff=0.4)

        self.play(Write(doppler_up))
        self.wait(0.5)

        # 吸収のアニメーション
        photon = Dot(color=RED, radius=0.1).move_to(LEFT * 5)
        self.play(photon.animate.move_to(atom_approaching.get_center()), run_time=0.5)
        self.play(
            Flash(atom_approaching, color=YELLOW, line_length=0.2, num_lines=8, run_time=0.3),
            atom_approaching.animate.set_color(PURPLE),
            FadeOut(photon),
        )

        result_left = Text("→ 光を吸収して減速!", font_size=18, color=GREEN)
        result_left.next_to(doppler_up, DOWN, buff=0.3)
        self.play(Write(result_left))
        self.wait(1)

        # ===== パート3: 遠ざかる原子 =====
        # ボックスタイトル
        receding_title = Text("② 遠ざかる原子", font_size=22, color=GRAY).shift(RIGHT * 3.5 + UP * 0.5)

        # 原子とレーザーの図
        laser_right = Arrow(RIGHT * 1.5, RIGHT * 4.5, color=RED, stroke_width=4)
        laser_right.shift(DOWN * 0.5)
        laser_right_label = Text("レーザー", font_size=14, color=RED).next_to(laser_right, UP, buff=0.1)

        atom_receding = Circle(radius=0.25, color=GRAY, fill_opacity=0.5)
        atom_receding.shift(RIGHT * 5 + DOWN * 0.5)

        atom_vel_r = Arrow(
            atom_receding.get_center(),
            atom_receding.get_center() + RIGHT * 0.8,
            color=GRAY, buff=0, stroke_width=4
        )
        vel_label_r = MathTex("v", font_size=20, color=GRAY).next_to(atom_vel_r, UP, buff=0.05)

        self.play(
            Write(receding_title),
            GrowArrow(laser_right), Write(laser_right_label),
            FadeIn(atom_receding), GrowArrow(atom_vel_r), Write(vel_label_r),
        )

        # ドップラー効果の説明
        doppler_down = VGroup(
            Text("原子から見ると:", font_size=16, color=WHITE),
            MathTex(r"\nu' = \nu_L - \Delta\nu", font_size=22, color=GRAY),
            Text("さらに赤方偏移 → 非共鳴", font_size=18, color=GRAY),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        doppler_down.next_to(atom_receding, DOWN, buff=0.4)

        self.play(Write(doppler_down))
        self.wait(0.5)

        # 吸収されない
        photon2 = Dot(color=RED, radius=0.1).move_to(RIGHT * 2)
        self.play(photon2.animate.move_to(RIGHT * 5.5), run_time=0.5)
        self.remove(photon2)

        result_right = Text("→ 光を吸収しない", font_size=18, color=GRAY)
        result_right.next_to(doppler_down, DOWN, buff=0.3)
        self.play(Write(result_right))
        self.wait(1)

        # ===== 結論 =====
        conclusion_box = VGroup(
            Text("結論:", font_size=24, color=YELLOW),
            Text("「速い原子だけ」が選択的に減速される", font_size=22, color=YELLOW),
        ).arrange(DOWN, buff=0.15)
        conclusion_box.to_edge(DOWN, buff=0.3)

        box = SurroundingRectangle(conclusion_box, color=YELLOW, buff=0.2)

        self.play(Write(conclusion_box), Create(box))
        self.wait(2)

        # フェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class DopplerFrequencyShift(Scene):
    """ドップラー効果による周波数シフトの視覚化"""

    def construct(self):
        # タイトル
        title = Text("ドップラー効果と共鳴条件", font_size=32, color=WHITE).to_edge(UP)
        self.play(Write(title))

        # 周波数スペクトル軸
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 1.2, 0.5],
            x_length=10,
            y_length=3,
            axis_config={"include_tip": True},
        ).shift(DOWN * 0.5)

        x_label = MathTex(r"\nu", font_size=28).next_to(axes.get_x_axis(), RIGHT)
        y_label = Text("吸収率", font_size=20).next_to(axes.get_y_axis(), UP)

        self.play(Create(axes), Write(x_label), Write(y_label))

        # 共鳴線（ローレンツ型）
        def lorentzian(x, x0, gamma=0.3):
            return gamma**2 / ((x - x0)**2 + gamma**2)

        resonance_curve = axes.plot(
            lambda x: lorentzian(x, 6),
            x_range=[3, 9],
            color=WHITE,
            stroke_width=3,
        )

        resonance_label = MathTex(r"\nu_0", font_size=24, color=WHITE)
        resonance_label.next_to(axes.c2p(6, 1), UP)

        self.play(Create(resonance_curve), Write(resonance_label))
        self.wait(0.5)

        # レーザー周波数（赤方偏移）
        laser_line = DashedLine(
            axes.c2p(4, 0),
            axes.c2p(4, 1.1),
            color=RED,
            stroke_width=2,
        )
        laser_label = MathTex(r"\nu_L", font_size=24, color=RED)
        laser_label.next_to(axes.c2p(4, 1.1), UP)

        self.play(Create(laser_line), Write(laser_label))

        # 説明テキスト
        explanation = Text(
            "レーザーは共鳴より低い周波数に設定",
            font_size=20, color=YELLOW
        ).to_edge(DOWN, buff=1.5)
        self.play(Write(explanation))
        self.wait(1)

        # 近づく原子：青方偏移で共鳴位置へ
        approaching_dot = Dot(axes.c2p(4, 0.1), color=BLUE, radius=0.15)
        approaching_label = Text("近づく原子", font_size=16, color=BLUE)
        approaching_label.next_to(approaching_dot, DOWN)

        self.play(FadeIn(approaching_dot), Write(approaching_label))

        # 青方偏移のアニメーション
        shift_arrow = Arrow(
            axes.c2p(4, 0.5),
            axes.c2p(6, 0.5),
            color=BLUE,
            stroke_width=3,
        )
        shift_label = Text("青方偏移", font_size=16, color=BLUE).next_to(shift_arrow, UP)

        self.play(
            approaching_dot.animate.move_to(axes.c2p(6, 1)),
            GrowArrow(shift_arrow),
            Write(shift_label),
            run_time=1.5,
        )

        # 共鳴！
        resonance_flash = Text("共鳴!", font_size=24, color=GREEN)
        resonance_flash.next_to(approaching_dot, RIGHT)
        self.play(
            Flash(approaching_dot, color=GREEN, line_length=0.3),
            Write(resonance_flash),
        )
        self.wait(1)

        # 遠ざかる原子：さらに赤方偏移
        receding_dot = Dot(axes.c2p(4, 0.1), color=GRAY, radius=0.15)
        receding_label = Text("遠ざかる原子", font_size=16, color=GRAY)
        receding_label.next_to(receding_dot, DOWN)

        # 前のものを少し透明に
        self.play(
            approaching_dot.animate.set_opacity(0.3),
            approaching_label.animate.set_opacity(0.3),
            shift_arrow.animate.set_opacity(0.3),
            shift_label.animate.set_opacity(0.3),
            resonance_flash.animate.set_opacity(0.3),
        )

        self.play(FadeIn(receding_dot), Write(receding_label))

        # 赤方偏移
        shift_arrow2 = Arrow(
            axes.c2p(4, 0.3),
            axes.c2p(2, 0.3),
            color=GRAY,
            stroke_width=3,
        )
        shift_label2 = Text("赤方偏移", font_size=16, color=GRAY).next_to(shift_arrow2, UP)

        self.play(
            receding_dot.animate.move_to(axes.c2p(2, 0.05)),
            GrowArrow(shift_arrow2),
            Write(shift_label2),
            run_time=1.5,
        )

        # 非共鳴
        no_resonance = Text("非共鳴", font_size=24, color=GRAY)
        no_resonance.next_to(receding_dot, LEFT)
        self.play(Write(no_resonance))
        self.wait(2)

        # フェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects])