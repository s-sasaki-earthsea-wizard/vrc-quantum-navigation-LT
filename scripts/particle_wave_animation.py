"""
粒子と波動の重ね合わせアニメーション

正方形の箱の中でバラバラな速度で運動する粒子と、
その波動の重ね合わせを視覚的に示す

使用方法:
    manim -pql particle_wave_animation.py ParticleWaveInterference
    manim -pqh particle_wave_animation.py ParticleWaveInterference  # 高画質
"""

from manim import *
import numpy as np


class ParticleWaveInterference(Scene):
    """熱い原子のバラバラな運動と波動の重ね合わせ"""

    def construct(self):
        # 色の設定
        BOX_COLOR = WHITE
        PARTICLE_COLORS = [RED, ORANGE, YELLOW, GREEN, TEAL, BLUE, PURPLE, PINK]

        # タイトル
        title = Text("熱い原子の運動と波動", font_size=32, color=WHITE).to_edge(UP)
        self.play(Write(title))

        # ===== 左側: 粒子の運動 =====
        box_left = Square(side_length=3, color=BOX_COLOR, stroke_width=2)
        box_left.shift(LEFT * 3.5)

        box_label = Text("原子の運動", font_size=20, color=WHITE)
        box_label.next_to(box_left, UP, buff=0.2)

        self.play(Create(box_left), Write(box_label))

        # 粒子を生成（バラバラな速度）
        num_particles = 8
        particles = []
        velocities = []

        np.random.seed(42)
        for i in range(num_particles):
            # ランダムな位置
            pos = box_left.get_center() + np.array([
                np.random.uniform(-1.2, 1.2),
                np.random.uniform(-1.2, 1.2),
                0
            ])
            # ランダムな速度（方向と大きさ）
            speed = np.random.uniform(0.3, 1.5)
            angle = np.random.uniform(0, 2 * np.pi)
            vel = np.array([speed * np.cos(angle), speed * np.sin(angle), 0])

            particle = Dot(pos, radius=0.08, color=PARTICLE_COLORS[i % len(PARTICLE_COLORS)])
            particles.append(particle)
            velocities.append(vel)

        particles_group = VGroup(*particles)
        self.play(FadeIn(particles_group))

        # 速度ベクトルを表示
        arrows = []
        for i, (p, v) in enumerate(zip(particles, velocities)):
            arrow = Arrow(
                p.get_center(),
                p.get_center() + v * 0.5,
                buff=0,
                stroke_width=2,
                color=PARTICLE_COLORS[i % len(PARTICLE_COLORS)],
                max_tip_length_to_length_ratio=0.3,
            )
            arrows.append(arrow)

        arrows_group = VGroup(*arrows)
        self.play(Create(arrows_group))

        # 説明テキスト
        speed_text = Text("速度がバラバラ", font_size=18, color=YELLOW)
        speed_text.next_to(box_left, DOWN, buff=0.3)
        self.play(Write(speed_text))
        self.wait(0.5)

        # ===== 右側: 波動の重ね合わせ =====
        wave_box = Rectangle(width=4, height=2.5, color=BOX_COLOR, stroke_width=2)
        wave_box.shift(RIGHT * 3)

        wave_label = Text("波動の重ね合わせ", font_size=20, color=WHITE)
        wave_label.next_to(wave_box, UP, buff=0.2)

        self.play(Create(wave_box), Write(wave_label))

        # 各粒子に対応する波（異なる波長）
        waves = VGroup()
        wave_x_range = [-1.8, 1.8]

        for i in range(num_particles):
            # 速度に応じた波長（速いほど短い）
            speed = np.linalg.norm(velocities[i])
            wavelength = 0.8 / speed  # λ ∝ 1/v

            wave = FunctionGraph(
                lambda x, wl=wavelength, phase=i * 0.5: 0.15 * np.sin(2 * np.pi * x / wl + phase),
                x_range=wave_x_range,
                color=PARTICLE_COLORS[i % len(PARTICLE_COLORS)],
                stroke_width=1.5,
                stroke_opacity=0.6,
            )
            wave.shift(RIGHT * 3)
            waves.add(wave)

        self.play(Create(waves), run_time=1.5)
        self.wait(0.5)

        # 波長がバラバラの説明
        wavelength_text = Text("波長がバラバラ", font_size=18, color=YELLOW)
        wavelength_text.next_to(wave_box, DOWN, buff=0.3)
        self.play(Write(wavelength_text))
        self.wait(1)

        # ===== 結論: 干渉縞がぼやける =====
        # 波を重ね合わせた結果（ぼやけた波形）
        self.play(FadeOut(waves))

        # 重ね合わせ結果（複雑で不規則な波形）
        def superposed_wave(x):
            result = 0
            for i in range(num_particles):
                speed = np.linalg.norm(velocities[i])
                wavelength = 0.8 / speed
                result += 0.1 * np.sin(2 * np.pi * x / wavelength + i * 0.5)
            return result

        superposed = FunctionGraph(
            superposed_wave,
            x_range=wave_x_range,
            color=GRAY,
            stroke_width=3,
        )
        superposed.shift(RIGHT * 3)

        result_label = Text("→ 干渉縞がぼやける", font_size=20, color=RED)
        result_label.next_to(wave_box, DOWN, buff=0.3)

        self.play(
            Create(superposed),
            Transform(wavelength_text, result_label),
        )
        self.wait(2)

        # フェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class ParticleMotionAnimation(Scene):
    """粒子が箱の中で動くアニメーション"""

    def construct(self):
        BOX_COLOR = WHITE
        PARTICLE_COLORS = [RED, ORANGE, YELLOW, GREEN, TEAL, BLUE, PURPLE, PINK]

        # タイトル
        title = Text("熱い原子の運動", font_size=36, color=WHITE).to_edge(UP)
        self.play(Write(title))

        # 箱
        box = Square(side_length=5, color=BOX_COLOR, stroke_width=2)

        self.play(Create(box))

        # 粒子を生成
        num_particles = 8
        particles = []
        velocities = []
        positions = []

        np.random.seed(42)
        for i in range(num_particles):
            pos = np.array([
                np.random.uniform(-2, 2),
                np.random.uniform(-2, 2),
                0
            ])
            speed = np.random.uniform(1, 4)
            angle = np.random.uniform(0, 2 * np.pi)
            vel = np.array([speed * np.cos(angle), speed * np.sin(angle), 0])

            particle = Dot(pos, radius=0.12, color=PARTICLE_COLORS[i % len(PARTICLE_COLORS)])
            particles.append(particle)
            velocities.append(vel)
            positions.append(pos)

        particles_group = VGroup(*particles)
        self.play(FadeIn(particles_group))

        # 説明
        explanation = Text(
            "バラバラな速度・方向で運動",
            font_size=24,
            color=YELLOW,
        ).to_edge(DOWN)
        self.play(Write(explanation))

        # 粒子を動かす（壁で反射）
        dt = 1 / 15  # フレームレート
        duration = 4  # 秒

        def update_particles(mob, dt_frame):
            nonlocal positions, velocities
            for i, particle in enumerate(particles):
                # 位置更新
                positions[i] = positions[i] + velocities[i] * dt

                # 壁との衝突判定
                if abs(positions[i][0]) > 2.3:
                    velocities[i][0] *= -1
                    positions[i][0] = np.clip(positions[i][0], -2.3, 2.3)
                if abs(positions[i][1]) > 2.3:
                    velocities[i][1] *= -1
                    positions[i][1] = np.clip(positions[i][1], -2.3, 2.3)

                particle.move_to(positions[i])

        particles_group.add_updater(update_particles)
        self.wait(duration)
        particles_group.remove_updater(update_particles)

        self.wait(1)

        # フェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class HotVsColdParticles(Scene):
    """高温と低温の粒子の比較"""

    def construct(self):
        BOX_COLOR = WHITE
        HOT_COLOR = RED
        COLD_COLOR = BLUE

        # タイトル
        title = Text("温度と原子の運動", font_size=32, color=WHITE).to_edge(UP)
        self.play(Write(title))

        # ===== 左側: 高温 =====
        hot_box = Square(side_length=3, color=HOT_COLOR, stroke_width=2)
        hot_box.shift(LEFT * 3.5 + DOWN * 0.3)

        hot_label = Text("高温", font_size=24, color=HOT_COLOR)
        hot_label.next_to(hot_box, UP, buff=0.2)

        # ===== 右側: 低温 =====
        cold_box = Square(side_length=3, color=COLD_COLOR, stroke_width=2)
        cold_box.shift(RIGHT * 3.5 + DOWN * 0.3)

        cold_label = Text("低温", font_size=24, color=COLD_COLOR)
        cold_label.next_to(cold_box, UP, buff=0.2)

        self.play(
            Create(hot_box), Write(hot_label),
            Create(cold_box), Write(cold_label),
        )

        # 高温の粒子（速い、バラバラ）
        np.random.seed(42)
        hot_particles = []
        hot_velocities = []
        hot_positions = []

        for i in range(6):
            pos = hot_box.get_center() + np.array([
                np.random.uniform(-1.2, 1.2),
                np.random.uniform(-1.2, 1.2),
                0
            ])
            speed = np.random.uniform(2, 5)
            angle = np.random.uniform(0, 2 * np.pi)
            vel = np.array([speed * np.cos(angle), speed * np.sin(angle), 0])

            particle = Dot(pos, radius=0.1, color=HOT_COLOR)
            hot_particles.append(particle)
            hot_velocities.append(vel)
            hot_positions.append(pos.copy())

        hot_group = VGroup(*hot_particles)

        # 低温の粒子（遅い、揃っている）
        cold_particles = []
        cold_velocities = []
        cold_positions = []

        for i in range(6):
            pos = cold_box.get_center() + np.array([
                np.random.uniform(-1.2, 1.2),
                np.random.uniform(-1.2, 1.2),
                0
            ])
            speed = np.random.uniform(0.3, 0.8)
            angle = np.random.uniform(0, 2 * np.pi)
            vel = np.array([speed * np.cos(angle), speed * np.sin(angle), 0])

            particle = Dot(pos, radius=0.1, color=COLD_COLOR)
            cold_particles.append(particle)
            cold_velocities.append(vel)
            cold_positions.append(pos.copy())

        cold_group = VGroup(*cold_particles)

        self.play(FadeIn(hot_group), FadeIn(cold_group))

        # 説明テキスト
        hot_desc = Text("速度バラバラ", font_size=18, color=HOT_COLOR)
        hot_desc.next_to(hot_box, DOWN, buff=0.2)

        cold_desc = Text("速度が揃う", font_size=18, color=COLD_COLOR)
        cold_desc.next_to(cold_box, DOWN, buff=0.2)

        self.play(Write(hot_desc), Write(cold_desc))

        # 粒子を動かす
        dt = 1 / 15
        box_half = 1.3

        def update_hot(mob, dt_frame):
            for i, particle in enumerate(hot_particles):
                hot_positions[i] = hot_positions[i] + hot_velocities[i] * dt
                center = hot_box.get_center()

                if abs(hot_positions[i][0] - center[0]) > box_half:
                    hot_velocities[i][0] *= -1
                if abs(hot_positions[i][1] - center[1]) > box_half:
                    hot_velocities[i][1] *= -1

                hot_positions[i][0] = np.clip(hot_positions[i][0], center[0] - box_half, center[0] + box_half)
                hot_positions[i][1] = np.clip(hot_positions[i][1], center[1] - box_half, center[1] + box_half)
                particle.move_to(hot_positions[i])

        def update_cold(mob, dt_frame):
            for i, particle in enumerate(cold_particles):
                cold_positions[i] = cold_positions[i] + cold_velocities[i] * dt
                center = cold_box.get_center()

                if abs(cold_positions[i][0] - center[0]) > box_half:
                    cold_velocities[i][0] *= -1
                if abs(cold_positions[i][1] - center[1]) > box_half:
                    cold_velocities[i][1] *= -1

                cold_positions[i][0] = np.clip(cold_positions[i][0], center[0] - box_half, center[0] + box_half)
                cold_positions[i][1] = np.clip(cold_positions[i][1], center[1] - box_half, center[1] + box_half)
                particle.move_to(cold_positions[i])

        hot_group.add_updater(update_hot)
        cold_group.add_updater(update_cold)

        self.wait(3)

        hot_group.remove_updater(update_hot)
        cold_group.remove_updater(update_cold)

        # 波長の比較を下に表示
        hot_wave_label = Text("→ 波長バラバラ", font_size=16, color=HOT_COLOR)
        hot_wave_label.next_to(hot_desc, DOWN, buff=0.15)

        cold_wave_label = Text("→ 波長が揃う", font_size=16, color=COLD_COLOR)
        cold_wave_label.next_to(cold_desc, DOWN, buff=0.15)

        self.play(Write(hot_wave_label), Write(cold_wave_label))

        # 結論
        hot_result = Text("干渉縞ぼやける", font_size=16, color=RED)
        hot_result.next_to(hot_wave_label, DOWN, buff=0.1)

        cold_result = Text("干渉縞くっきり", font_size=16, color=GREEN)
        cold_result.next_to(cold_wave_label, DOWN, buff=0.1)

        self.play(Write(hot_result), Write(cold_result))
        self.wait(2)

        # フェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class WaveSuperposition(Scene):
    """波動の重ね合わせの視覚化"""

    def construct(self):
        # タイトル
        title = Text("波動の重ね合わせ", font_size=36, color=WHITE).to_edge(UP)
        self.play(Write(title))

        # ===== 左: 波長が揃った波 =====
        left_label = Text("波長が揃っている", font_size=20, color=GREEN).shift(LEFT * 3.5 + UP * 2)
        self.play(Write(left_label))

        # 同じ波長の波を3つ
        coherent_waves = VGroup()
        wavelength = 1.0
        for i in range(3):
            wave = FunctionGraph(
                lambda x, ph=i * 0.3: 0.3 * np.sin(2 * np.pi * x / wavelength + ph),
                x_range=[-2.5, 2.5],
                color=GREEN,
                stroke_width=2,
                stroke_opacity=0.7,
            )
            wave.shift(LEFT * 3.5 + UP * (0.5 - i * 0.3))
            coherent_waves.add(wave)

        self.play(Create(coherent_waves))

        # 重ね合わせ結果（強め合う）
        coherent_sum = FunctionGraph(
            lambda x: 0.6 * np.sin(2 * np.pi * x / wavelength),
            x_range=[-2.5, 2.5],
            color=YELLOW,
            stroke_width=4,
        )
        coherent_sum.shift(LEFT * 3.5 + DOWN * 1.5)

        coherent_result = Text("→ くっきり干渉", font_size=18, color=YELLOW)
        coherent_result.next_to(coherent_sum, DOWN, buff=0.2)

        self.play(Create(coherent_sum), Write(coherent_result))

        # ===== 右: 波長がバラバラの波 =====
        right_label = Text("波長がバラバラ", font_size=20, color=RED).shift(RIGHT * 3.5 + UP * 2)
        self.play(Write(right_label))

        # 異なる波長の波
        incoherent_waves = VGroup()
        wavelengths = [0.6, 1.0, 1.5]
        for i, wl in enumerate(wavelengths):
            wave = FunctionGraph(
                lambda x, w=wl, ph=i * 0.5: 0.3 * np.sin(2 * np.pi * x / w + ph),
                x_range=[-2.5, 2.5],
                color=RED,
                stroke_width=2,
                stroke_opacity=0.7,
            )
            wave.shift(RIGHT * 3.5 + UP * (0.5 - i * 0.3))
            incoherent_waves.add(wave)

        self.play(Create(incoherent_waves))

        # 重ね合わせ結果（打ち消し合って不規則）
        def messy_wave(x):
            return sum(0.2 * np.sin(2 * np.pi * x / wl + i * 0.5)
                       for i, wl in enumerate(wavelengths))

        incoherent_sum = FunctionGraph(
            messy_wave,
            x_range=[-2.5, 2.5],
            color=GRAY,
            stroke_width=4,
        )
        incoherent_sum.shift(RIGHT * 3.5 + DOWN * 1.5)

        incoherent_result = Text("→ ぼやける", font_size=18, color=GRAY)
        incoherent_result.next_to(incoherent_sum, DOWN, buff=0.2)

        self.play(Create(incoherent_sum), Write(incoherent_result))
        self.wait(2)

        # フェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects])
