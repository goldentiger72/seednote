import pygame
import random
import math
import sys
from enum import Enum

# ===========================
# 기본 초기화 및 설정
# ===========================
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Crystal Cavern Chronicles")

clock = pygame.time.Clock()
FPS = 60  # 프레임 제한

# ===========================
# 게임 상태
# ===========================
class GameState(Enum):
    TITLE = 0
    PLAYING = 1
    GAME_OVER = 2
    LEVEL_COMPLETE = 3
    GAME_WIN = 4

# ===========================
# 색상 정의
# ===========================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)
BROWN = (165, 42, 42)
GRAY = (128, 128, 128)
LIGHT_BLUE = (173, 216, 230)
DARK_GREEN = (0, 100, 0)
GOLD = (255, 215, 0)

# ===========================
# 레벨 테마
# ===========================
class LevelTheme(Enum):
    FOREST = 0
    CAVE = 1
    LAVA = 2
    ICE = 3
    SPACE = 4

# ===========================
# 레벨 데이터
#  - 플랫폼, 적, 스폰 위치, 포털, 보스(마지막 레벨)
#  - 레벨별 파워업도 랜덤 생성
# ===========================
level_designs = [
    # -----------------------------------------
    # Level 1: Forest Theme
    # -----------------------------------------
    {
        "theme": LevelTheme.FOREST,
        "platforms": [
            {"x": 0, "y": 550, "width": 800, "height": 50},  # Ground
            {"x": 100, "y": 450, "width": 200, "height": 20},
            {"x": 400, "y": 400, "width": 150, "height": 20},
            {"x": 600, "y": 350, "width": 100, "height": 20},
            {"x": 200, "y": 300, "width": 150, "height": 20},
            {"x": 350, "y": 250, "width": 100, "height": 20},
            {"x": 500, "y": 200, "width": 150, "height": 20},
        ],
        "spawn_point": {"x": 50, "y": 450},
        "exit_portal": {"x": 700, "y": 150},
        "enemies": [
            {"type": "walker", "x": 300, "y": 430, "width": 30, "height": 30, "speed": 2},
            {"type": "walker", "x": 500, "y": 380, "width": 30, "height": 30, "speed": 2},
            {"type": "jumper", "x": 250, "y": 280, "width": 30, "height": 30, "jump_force": 10},
        ],
        "collectibles": [
            {"x": 150, "y": 430, "collected": False},
            {"x": 450, "y": 380, "collected": False},
            {"x": 650, "y": 330, "collected": False},
            {"x": 250, "y": 280, "collected": False},
            {"x": 400, "y": 230, "collected": False},
            {"x": 550, "y": 180, "collected": False},
        ]
    },
    # -----------------------------------------
    # Level 2: Cave Theme
    # -----------------------------------------
    {
        "theme": LevelTheme.CAVE,
        "platforms": [
            {"x": 0, "y": 550, "width": 300, "height": 50},   # Ground left
            {"x": 500, "y": 550, "width": 300, "height": 50}, # Ground right
            {"x": 150, "y": 450, "width": 100, "height": 20},
            {"x": 350, "y": 400, "width": 100, "height": 20},
            {"x": 550, "y": 350, "width": 100, "height": 20},
            {"x": 250, "y": 300, "width": 100, "height": 20},
            {"x": 450, "y": 250, "width": 100, "height": 20},
            {"x": 650, "y": 200, "width": 100, "height": 20},
        ],
        "spawn_point": {"x": 150, "y": 450},
        "exit_portal": {"x": 650, "y": 150},
        "enemies": [
            {"type": "walker", "x": 200, "y": 430, "width": 30, "height": 30, "speed": 2},
            {"type": "flyer", "x": 400, "y": 300, "width": 30, "height": 30, "speed": 3},
            {"type": "jumper", "x": 500, "y": 330, "width": 30, "height": 30, "jump_force": 10},
            {"type": "walker", "x": 600, "y": 180, "width": 30, "height": 30, "speed": 3},
        ],
        "collectibles": [
            {"x": 200, "y": 430, "collected": False},
            {"x": 400, "y": 380, "collected": False},
            {"x": 600, "y": 330, "collected": False},
            {"x": 300, "y": 280, "collected": False},
            {"x": 500, "y": 230, "collected": False},
            {"x": 700, "y": 180, "collected": False},
        ]
    },
    # -----------------------------------------
    # Level 3: Lava Theme
    # -----------------------------------------
    {
        "theme": LevelTheme.LAVA,
        "platforms": [
            {"x": 0, "y": 550, "width": 800, "height": 50},  # Lava floor
            {"x": 50, "y": 450, "width": 150, "height": 20},
            {"x": 300, "y": 400, "width": 150, "height": 20},
            {"x": 550, "y": 350, "width": 150, "height": 20},
            {"x": 100, "y": 300, "width": 150, "height": 20},
            {"x": 350, "y": 250, "width": 150, "height": 20},
            {"x": 600, "y": 200, "width": 150, "height": 20},
            # Moving platforms
            {"x": 200, "y": 350, "width": 80, "height": 20,
             "moving": True, "direction": 1, "speed": 2, "range": 100},
            {"x": 450, "y": 300, "width": 80, "height": 20,
             "moving": True, "direction": 1, "speed": 2, "range": 100},
        ],
        "spawn_point": {"x": 80, "y": 400},
        "exit_portal": {"x": 650, "y": 150},
        "enemies": [
            {"type": "flyer", "x": 250, "y": 350, "width": 30, "height": 30, "speed": 3},
            {"type": "flyer", "x": 500, "y": 300, "width": 30, "height": 30, "speed": 3},
            {"type": "walker", "x": 400, "y": 380, "width": 30, "height": 30, "speed": 3},
            {"type": "walker", "x": 650, "y": 330, "width": 30, "height": 30, "speed": 3},
            {"type": "jumper", "x": 200, "y": 280, "width": 30, "height": 30, "jump_force": 12},
        ],
        "collectibles": [
            {"x": 100, "y": 430, "collected": False},
            {"x": 350, "y": 380, "collected": False},
            {"x": 600, "y": 330, "collected": False},
            {"x": 150, "y": 280, "collected": False},
            {"x": 400, "y": 230, "collected": False},
            {"x": 650, "y": 180, "collected": False},
        ]
    },
    # -----------------------------------------
    # Level 4: Ice Theme
    # -----------------------------------------
    {
        "theme": LevelTheme.ICE,
        "platforms": [
            {"x": 0, "y": 550, "width": 800, "height": 50},  # Ice floor
            {"x": 100, "y": 450, "width": 100, "height": 20},
            {"x": 300, "y": 450, "width": 100, "height": 20},
            {"x": 500, "y": 450, "width": 100, "height": 20},
            {"x": 700, "y": 450, "width": 100, "height": 20},
            {"x": 200, "y": 350, "width": 100, "height": 20},
            {"x": 400, "y": 350, "width": 100, "height": 20},
            {"x": 600, "y": 350, "width": 100, "height": 20},
            {"x": 100, "y": 250, "width": 100, "height": 20},
            {"x": 300, "y": 250, "width": 100, "height": 20},
            {"x": 500, "y": 250, "width": 100, "height": 20},
            {"x": 700, "y": 250, "width": 100, "height": 20},
        ],
        "spawn_point": {"x": 50, "y": 500},
        "exit_portal": {"x": 700, "y": 200},
        "enemies": [
            {"type": "walker", "x": 150, "y": 430, "width": 30, "height": 30, "speed": 4},
            {"type": "walker", "x": 350, "y": 430, "width": 30, "height": 30, "speed": 4},
            {"type": "walker", "x": 550, "y": 430, "width": 30, "height": 30, "speed": 4},
            {"type": "flyer", "x": 250, "y": 330, "width": 30, "height": 30, "speed": 3},
            {"type": "flyer", "x": 450, "y": 330, "width": 30, "height": 30, "speed": 3},
            {"type": "jumper", "x": 650, "y": 330, "width": 30, "height": 30, "jump_force": 12},
        ],
        "collectibles": [
            {"x": 150, "y": 430, "collected": False},
            {"x": 350, "y": 430, "collected": False},
            {"x": 550, "y": 430, "collected": False},
            {"x": 250, "y": 330, "collected": False},
            {"x": 450, "y": 330, "collected": False},
            {"x": 650, "y": 330, "collected": False},
            {"x": 150, "y": 230, "collected": False},
            {"x": 350, "y": 230, "collected": False},
            {"x": 550, "y": 230, "collected": False},
        ]
    },
    # -----------------------------------------
    # Level 5: Space Theme (Boss Level)
    # -----------------------------------------
    {
        "theme": LevelTheme.SPACE,
        "platforms": [
            {"x": 0, "y": 550, "width": 800, "height": 50},  # Ground
            {"x": 100, "y": 450, "width": 200, "height": 20},
            {"x": 500, "y": 450, "width": 200, "height": 20},
            {"x": 300, "y": 350, "width": 200, "height": 20},
            {"x": 100, "y": 250, "width": 200, "height": 20},
            {"x": 500, "y": 250, "width": 200, "height": 20},
        ],
        "spawn_point": {"x": 150, "y": 400},
        "exit_portal": None,  # 보스 레벨이므로 포털 없음
        "boss": {
            "x": 400, "y": 150, "width": 80, "height": 80,
            "health": 100, "speed": 3, "attack_cooldown": 60,
            "attack_pattern": "spiral", "bullet_speed": 5
        },
        "enemies": [
            {"type": "flyer", "x": 200, "y": 350, "width": 30, "height": 30, "speed": 3},
            {"type": "flyer", "x": 600, "y": 350, "width": 30, "height": 30, "speed": 3},
        ],
        "collectibles": [
            {"x": 150, "y": 430, "collected": False},
            {"x": 250, "y": 430, "collected": False},
            {"x": 550, "y": 430, "collected": False},
            {"x": 650, "y": 430, "collected": False},
            {"x": 350, "y": 330, "collected": False},
            {"x": 450, "y": 330, "collected": False},
            {"x": 150, "y": 230, "collected": False},
            {"x": 250, "y": 230, "collected": False},
            {"x": 550, "y": 230, "collected": False},
            {"x": 650, "y": 230, "collected": False},
        ]
    },
]

# ===========================
# 전역 변수들
# ===========================
current_level = 0
game_state = GameState.TITLE
score = 0
lives = 3
collected_gems = 0
total_gems = sum(len(level["collectibles"]) for level in level_designs)

# 플레이어 정보
player = {
    "x": level_designs[current_level]["spawn_point"]["x"],
    "y": level_designs[current_level]["spawn_point"]["y"],
    "width": 30,
    "height": 50,
    "velocity_x": 0,
    "velocity_y": 0,
    "gravity": 0.5,
    "speed": 5,
    "jump_force": 12,
    "on_ground": False,
    "double_jump": False,
    "double_jump_used": False,
    "on_ice": False,
    "direction": 1,  # 1: 오른쪽, -1: 왼쪽
    "animation_frame": 0,
    "animation_cooldown": 5,
    "animation_timer": 0,
    "invincible": False,
    "invincible_timer": 0,
    "dash_ability": True,
    "dash_cooldown": 0,
    "health": 100,
    "max_health": 100,
    "shooting_cooldown": 0,
    "bullets": []
}

# 보스(마지막 레벨)
boss = None
boss_bullets = []

if current_level == 4:  # 레벨 5(인덱스4)일 때 보스 복사
    boss = level_designs[current_level]["boss"].copy()
    boss["active"] = True

# ===========================
# 동적 배경 파티클
# ===========================
timer = 0

# 별 (Space/Title 화면 등에 사용)
stars = []
for _ in range(100):
    stars.append({
        "x": random.randint(0, SCREEN_WIDTH),
        "y": random.randint(0, SCREEN_HEIGHT),
        "size": random.randint(1, 3),
        "speed": random.uniform(0.1, 0.5)
    })

# 구름 (Forest 레벨 등에 사용)
clouds = []
for _ in range(10):
    clouds.append({
        "x": random.randint(-200, SCREEN_WIDTH),
        "y": random.randint(50, 150),
        "speed": random.uniform(0.3, 0.7),
        "size": random.uniform(0.5, 1.5)
    })

# 물방울 (Cave 테마 연출용)
bubbles = []
for _ in range(20):
    bubbles.append({
        "x": random.randint(0, SCREEN_WIDTH),
        "y": random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT + 200),
        "size": random.randint(2, 10),
        "speed": random.uniform(1, 3)
    })

# 용암 파티클
lava_particles = []
for _ in range(30):
    lava_particles.append({
        "x": random.randint(0, SCREEN_WIDTH),
        "y": random.randint(550, 600),
        "height": random.randint(5, 15),
        "speed": random.uniform(2, 5),
        "lifetime": random.randint(30, 60)
    })

# 눈 파티클 (Ice 레벨)
snowflakes = []
for _ in range(100):
    snowflakes.append({
        "x": random.randint(0, SCREEN_WIDTH),
        "y": random.randint(-50, SCREEN_HEIGHT),
        "size": random.randint(1, 4),
        "speed": random.uniform(1, 3),
        "wobble": random.uniform(-0.5, 0.5)
    })

# 우주 잔해 (Space 레벨)
space_debris = []
for _ in range(20):
    space_debris.append({
        "x": random.randint(0, SCREEN_WIDTH),
        "y": random.randint(0, SCREEN_HEIGHT),
        "size": random.randint(2, 8),
        "speed_x": random.uniform(-1, 1),
        "speed_y": random.uniform(-1, 1),
        "rotation": random.uniform(0, 360),
        "rotation_speed": random.uniform(-2, 2)
    })

# ===========================
# 폰트
# ===========================
title_font = pygame.font.SysFont("Arial", 64)
subtitle_font = pygame.font.SysFont("Arial", 32)
hud_font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 18)

# ===========================
# 특수 효과 & 파워업
# ===========================
effects = []
power_ups = []
for level in level_designs:
    if "power_ups" not in level:
        level["power_ups"] = []
        # 각 레벨마다 2개씩 랜덤 파워업 배치
        for _ in range(2):
            level["power_ups"].append({
                "x": random.randint(100, 700),
                "y": random.randint(100, 400),
                "type": random.choice(["health", "speed", "jump", "shield"]),
                "collected": False,
                "animation_frame": 0,
                "animation_timer": 0
            })

# ===========================
# 함수들
# ===========================

def reset_level():
    """
    현재 레벨을 다시 시작할 때(플레이어 사망 등) 상태 초기화
    """
    global player, boss, boss_bullets

    # 플레이어 재배치
    player["x"] = level_designs[current_level]["spawn_point"]["x"]
    player["y"] = level_designs[current_level]["spawn_point"]["y"]
    player["velocity_x"] = 0
    player["velocity_y"] = 0
    player["on_ground"] = False
    player["double_jump_used"] = False
    player["invincible"] = True
    player["invincible_timer"] = 60
    player["bullets"] = []

    # 보스 레벨이면 보스 재설정
    if current_level == 4:
        boss = level_designs[current_level]["boss"].copy()
        boss["active"] = True
        boss_bullets = []

    # 이 레벨의 보석/수집품, 파워업 다시 초기화
    for collectible in level_designs[current_level]["collectibles"]:
        collectible["collected"] = False
    for power_up in level_designs[current_level]["power_ups"]:
        power_up["collected"] = False


def draw_title_screen():
    screen.fill(BLACK)

    # 별 그리기 (배경)
    for star in stars:
        pygame.draw.circle(screen, WHITE, (int(star["x"]), int(star["y"])), star["size"])

    # 타이틀 텍스트
    title_text = title_font.render("Crystal Cavern Chronicles", True, CYAN)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
    screen.blit(title_text, title_rect)

    # 깜박이는 서브타이틀
    pulse = (math.sin(timer / 10) + 1) / 2  # 0 ~ 1
    subtitle_color = (
        int(255 * pulse),
        int(255 * pulse),
        int(255 * (1 - pulse))
    )
    subtitle_text = subtitle_font.render("Press SPACE to Start", True, subtitle_color)
    subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 350))
    screen.blit(subtitle_text, subtitle_rect)

    # 컨트롤 안내
    controls_text1 = small_font.render("Controls: Arrow Keys to Move, UP to Jump, SPACE to Shoot", True, WHITE)
    controls_text2 = small_font.render("Press SHIFT to Dash, Collect Crystals and Defeat Enemies", True, WHITE)
    controls_rect1 = controls_text1.get_rect(center=(SCREEN_WIDTH // 2, 450))
    controls_rect2 = controls_text2.get_rect(center=(SCREEN_WIDTH // 2, 480))
    screen.blit(controls_text1, controls_rect1)
    screen.blit(controls_text2, controls_rect2)

    # 간단한 플레이어 그림
    player_x = SCREEN_WIDTH // 2
    player_y = 250
    pygame.draw.rect(screen, BLUE, (player_x - 15, player_y - 25, 30, 50))  # 몸통
    pygame.draw.circle(screen, LIGHT_BLUE, (player_x, player_y - 35), 15)   # 머리
    pygame.draw.circle(screen, WHITE, (player_x - 5, player_y - 38), 4)     # 왼눈
    pygame.draw.circle(screen, WHITE, (player_x + 5, player_y - 38), 4)     # 오른눈
    pygame.draw.circle(screen, BLACK, (player_x - 5, player_y - 38), 2)
    pygame.draw.circle(screen, BLACK, (player_x + 5, player_y - 38), 2)

    # 옆에 결정 로고
    crystal_points = [
        (player_x + 50, player_y - 10),
        (player_x + 65, player_y - 30),
        (player_x + 80, player_y - 10),
        (player_x + 65, player_y + 20)
    ]
    pygame.draw.polygon(screen, CYAN, crystal_points)
    pygame.draw.polygon(screen, WHITE, crystal_points, 2)

    # 하단부 장식 결정
    for i in range(10):
        x = i * 90 + 45
        y = 550
        height = random.randint(20, 50)
        crystal_points = [
            (x - 10, y),
            (x, y - height),
            (x + 10, y)
        ]
        color = (
            int(100 + 155 * abs(math.sin(timer / 20 + i))),
            int(100 + 155 * abs(math.sin(timer / 15 + i))),
            int(200 + 55 * abs(math.sin(timer / 10 + i)))
        )
        pygame.draw.polygon(screen, color, crystal_points)
        pygame.draw.polygon(screen, WHITE, crystal_points, 1)


def draw_game_over_screen():
    screen.fill(BLACK)

    # 별 배경
    for star in stars:
        pygame.draw.circle(screen, WHITE, (int(star["x"]), int(star["y"])), star["size"])

    # 텍스트
    title_text = title_font.render("Game Over", True, RED)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
    screen.blit(title_text, title_rect)

    score_text = subtitle_font.render(f"Final Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 280))
    screen.blit(score_text, score_rect)

    gems_text = subtitle_font.render(f"Crystals: {collected_gems}/{total_gems}", True, CYAN)
    gems_rect = gems_text.get_rect(center=(SCREEN_WIDTH // 2, 330))
    screen.blit(gems_text, gems_rect)

    pulse = (math.sin(timer / 10) + 1) / 2
    restart_color = (
        int(255 * pulse),
        int(255 * (1 - pulse)),
        int(100 * pulse)
    )
    restart_text = subtitle_font.render("Press R to Restart", True, restart_color)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
    screen.blit(restart_text, restart_rect)

    # 깨진 결정 표현
    crystal_pieces = [
        [(SCREEN_WIDTH // 2 - 40, 480), (SCREEN_WIDTH // 2 - 60, 500), (SCREEN_WIDTH // 2 - 30, 510)],
        [(SCREEN_WIDTH // 2 - 10, 470), (SCREEN_WIDTH // 2, 490), (SCREEN_WIDTH // 2 + 10, 480)],
        [(SCREEN_WIDTH // 2 + 20, 490), (SCREEN_WIDTH // 2 + 40, 470), (SCREEN_WIDTH // 2 + 30, 510)]
    ]
    for piece in crystal_pieces:
        color = (
            int(100 + 155 * abs(math.sin(timer / 20))),
            int(100 + 155 * abs(math.sin(timer / 15))),
            int(200 + 55 * abs(math.sin(timer / 10)))
        )
        pygame.draw.polygon(screen, color, piece)
        pygame.draw.polygon(screen, WHITE, piece, 1)


def draw_game_win_screen():
    screen.fill(BLACK)

    # 별 반짝임
    for star in stars:
        size = star["size"] + math.sin(timer / 10 + star["x"]) * 2
        pygame.draw.circle(screen, WHITE, (int(star["x"]), int(star["y"])), max(1, int(size)))

    title_text = title_font.render("Victory!", True, GOLD)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
    screen.blit(title_text, title_rect)

    subtitle_text = subtitle_font.render("You've Saved the Crystal Caverns!", True, CYAN)
    subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 220))
    screen.blit(subtitle_text, subtitle_rect)

    score_text = subtitle_font.render(f"Final Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 280))
    screen.blit(score_text, score_rect)

    gems_text = subtitle_font.render(f"Crystals: {collected_gems}/{total_gems}", True, CYAN)
    gems_rect = gems_text.get_rect(center=(SCREEN_WIDTH // 2, 330))
    screen.blit(gems_text, gems_rect)

    pulse = (math.sin(timer / 10) + 1) / 2
    restart_color = (
        int(100 * pulse),
        int(255 * pulse),
        int(100 * pulse)
    )
    restart_text = subtitle_font.render("Press R to Play Again", True, restart_color)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
    screen.blit(restart_text, restart_rect)

    # 거대한 결정
    crystal_center_x = SCREEN_WIDTH // 2
    crystal_center_y = 500
    crystal_size = 50 + math.sin(timer / 15) * 5

    crystal_points = [
        (crystal_center_x, crystal_center_y - crystal_size),
        (crystal_center_x + crystal_size * 0.7, crystal_center_y),
        (crystal_center_x, crystal_center_y + crystal_size * 0.7),
        (crystal_center_x - crystal_size * 0.7, crystal_center_y)
    ]

    # 아우라/글로우
    for i in range(5, 0, -1):
        glow_size = i * 3
        glow_points = [
            (crystal_center_x, crystal_center_y - crystal_size - glow_size),
            (crystal_center_x + crystal_size * 0.7 + glow_size, crystal_center_y),
            (crystal_center_x, crystal_center_y + crystal_size * 0.7 + glow_size),
            (crystal_center_x - crystal_size * 0.7 - glow_size, crystal_center_y)
        ]
        glow_color = (
            int(100 + (5 - i) * 30),
            int(100 + (5 - i) * 30),
            int(200 + (5 - i) * 10)
        )
        pygame.draw.polygon(screen, glow_color, glow_points)

    # 결정 본체
    crystal_color = (
        int(100 + 155 * abs(math.sin(timer / 20))),
        int(100 + 155 * abs(math.sin(timer / 15))),
        int(200 + 55 * abs(math.sin(timer / 10)))
    )
    pygame.draw.polygon(screen, crystal_color, crystal_points)
    pygame.draw.polygon(screen, WHITE, crystal_points, 2)

    # 반사선
    pygame.draw.line(
        screen, WHITE,
        (crystal_center_x - 10, crystal_center_y - crystal_size * 0.6),
        (crystal_center_x + 5, crystal_center_y - crystal_size * 0.2)
    )
    pygame.draw.line(
        screen, WHITE,
        (crystal_center_x + 10, crystal_center_y - crystal_size * 0.4),
        (crystal_center_x - 5, crystal_center_y - crystal_size * 0.1)
    )


def handle_input():
    """
    플레이어 입력 처리
    """
    keys = pygame.key.get_pressed()

    # 좌우 이동
    if keys[pygame.K_LEFT]:
        player["velocity_x"] = -player["speed"]
        player["direction"] = -1
    elif keys[pygame.K_RIGHT]:
        player["velocity_x"] = player["speed"]
        player["direction"] = 1
    else:
        # 마찰력 적용 (얼음이면 적게, 아니면 크게)
        friction = 0.1 if player["on_ice"] else 0.3
        if abs(player["velocity_x"]) < friction:
            player["velocity_x"] = 0
        elif player["velocity_x"] > 0:
            player["velocity_x"] -= friction
        else:
            player["velocity_x"] += friction

    # 점프
    if keys[pygame.K_UP]:
        if player["on_ground"]:
            # 첫 점프
            player["velocity_y"] = -player["jump_force"]
            player["on_ground"] = False
            player["double_jump_used"] = False
        elif not player["double_jump_used"]:
            # 더블 점프
            player["velocity_y"] = -player["jump_force"]
            player["double_jump_used"] = True

    # 대쉬 (Shift)
    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
        if player["dash_ability"] and player["dash_cooldown"] <= 0:
            dash_power = 15
            player["velocity_x"] = dash_power * player["direction"]
            player["dash_cooldown"] = 30  # 대쉬 후 쿨타임

    # 슈팅 (Space)
    if keys[pygame.K_SPACE]:
        if player["shooting_cooldown"] <= 0:
            shoot_bullet()
            player["shooting_cooldown"] = 15  # 총알 발사 간격


def shoot_bullet():
    """
    플레이어가 총알 발사
    """
    bullet_speed = 8
    bullet_direction = player["direction"]
    bullet_x = player["x"] + player["width"] // 2
    bullet_y = player["y"] + player["height"] // 2

    player["bullets"].append({
        "x": bullet_x,
        "y": bullet_y,
        "radius": 5,
        "speed": bullet_speed * bullet_direction,
        "color": YELLOW
    })


def update_player():
    """
    플레이어 물리/상태 업데이트
    """
    # 중력
    player["velocity_y"] += player["gravity"]
    if player["velocity_y"] > 10:
        player["velocity_y"] = 10

    # 이동
    player["x"] += player["velocity_x"]
    player["y"] += player["velocity_y"]

    # 화면 밖으로 나가지 않도록
    if player["x"] < 0:
        player["x"] = 0
    if player["x"] + player["width"] > SCREEN_WIDTH:
        player["x"] = SCREEN_WIDTH - player["width"]
    if player["y"] < 0:
        player["y"] = 0
        player["velocity_y"] = 0
    if player["y"] > SCREEN_HEIGHT:  # 바닥 아래로 떨어지면 사망 처리
        damage_player(999)  # 즉시 사망

    # 대쉬 쿨타임
    if player["dash_cooldown"] > 0:
        player["dash_cooldown"] -= 1

    # 무적 시간
    if player["invincible"]:
        player["invincible_timer"] -= 1
        if player["invincible_timer"] <= 0:
            player["invincible"] = False

    # 사격 쿨타임
    if player["shooting_cooldown"] > 0:
        player["shooting_cooldown"] -= 1

    # 총알 업데이트
    for bullet in player["bullets"][:]:
        bullet["x"] += bullet["speed"]
        # 화면 밖으로 나가면 제거
        if bullet["x"] < 0 or bullet["x"] > SCREEN_WIDTH:
            player["bullets"].remove(bullet)

    # 플랫폼 충돌 체크
    check_platform_collisions()

    # 아이템/파워업 수거
    collect_items()
    collect_powerups()


def damage_player(amount):
    """
    플레이어 데미지 처리
    """
    global lives, game_state
    if player["invincible"]:
        return

    player["health"] -= amount
    if player["health"] <= 0:
        # 라이프 감소 후 체크
        lives -= 1
        if lives > 0:
            player["health"] = player["max_health"]
            reset_level()
        else:
            game_state = GameState.GAME_OVER


def check_platform_collisions():
    """
    플랫폼 충돌로 플레이어 on_ground 체크, y위치 보정 등
    (움직이는 플랫폼이면 플랫폼과 함께 이동 처리)
    """
    player_rect = pygame.Rect(player["x"], player["y"], player["width"], player["height"])
    player["on_ground"] = False

    for p in level_designs[current_level]["platforms"]:
        platform_rect = pygame.Rect(p["x"], p["y"], p["width"], p["height"])
        if player_rect.colliderect(platform_rect):
            # 수직 충돌 감지
            # 플레이어가 위에서 내려오고 있으면
            if player["velocity_y"] > 0 and player_rect.bottom <= platform_rect.bottom:
                player["y"] = p["y"] - player["height"]
                player["velocity_y"] = 0
                player["on_ground"] = True
                # 얼음 여부 체크
                if level_designs[current_level]["theme"] == LevelTheme.ICE:
                    player["on_ice"] = True
                else:
                    player["on_ice"] = False

                # 움직이는 플랫폼이면, 플랫폼의 움직임에 따라 x 이동
                if "moving" in p and p["moving"]:
                    # 플레이어가 플랫폼 위에 있는 동안 함께 이동
                    player["x"] += p["speed"] * p["direction"]

    # 용암 테마면, 바닥(0번 플랫폼)이 용암
    if level_designs[current_level]["theme"] == LevelTheme.LAVA:
        # 바닥 플랫폼 y=550 (전체 너비)
        # 플레이어가 y+height>=550이면, 데미지
        if player["y"] + player["height"] >= 550:
            # 용암 데미지
            damage_player(0.1)  # 매 프레임마다 조금씩 데미지


def collect_items():
    """
    레벨에 놓인 크리스탈(collectibles) 습득 처리
    """
    global score, collected_gems
    player_rect = pygame.Rect(player["x"], player["y"], player["width"], player["height"])

    for c in level_designs[current_level]["collectibles"]:
        if not c["collected"]:
            c_rect = pygame.Rect(c["x"], c["y"], 20, 20)
            if player_rect.colliderect(c_rect):
                c["collected"] = True
                collected_gems += 1
                score += 100  # 보석 하나당 100점 추가


def collect_powerups():
    """
    레벨에 놓인 파워업 습득 처리
    """
    player_rect = pygame.Rect(player["x"], player["y"], player["width"], player["height"])

    for p in level_designs[current_level]["power_ups"]:
        if not p["collected"]:
            p_rect = pygame.Rect(p["x"], p["y"], 20, 20)
            if player_rect.colliderect(p_rect):
                p["collected"] = True
                # 파워업 적용
                apply_powerup(p["type"])


def apply_powerup(power_type):
    """
    파워업 종류별 적용 로직
    """
    global player

    if power_type == "health":
        # 체력 회복
        player["health"] = min(player["max_health"], player["health"] + 30)
        # 효과음 or 이펙트 ...
    elif power_type == "speed":
        # 일시적 속도 증가
        player["speed"] += 2
        # 일정 시간 후 원상 복귀를 위한 효과
        effects.append({
            "type": "speed",
            "timer": 300  # 5초 정도
        })
    elif power_type == "jump":
        # 점프력 증가
        player["jump_force"] += 5
        effects.append({
            "type": "jump",
            "timer": 300
        })
    elif power_type == "shield":
        # 무적
        player["invincible"] = True
        player["invincible_timer"] = 180  # 3초 정도


def update_enemies():
    """
    적 AI 업데이트
    """
    for e in level_designs[current_level]["enemies"]:
        # walker: 좌우로 움직임
        if e["type"] == "walker":
            # 간단히 좌우 왕복 AI 등...
            # 화면 영역에서 되돌아가도록
            e["x"] += e["speed"]
            if e["x"] < 0 or e["x"] + e["width"] > SCREEN_WIDTH:
                e["speed"] *= -1

        # jumper: 일정 간격으로 점프
        if e["type"] == "jumper":
            # 점프 중인지 여부는 저장 안 했으므로 간단히 충돌 판단
            # 플레이어 것과 달리 아주 단순화
            # y가 플랫폼 위에 있다고 가정하면
            if random.randint(0, 100) == 0:  # 가끔 점프
                e["velocity_y"] = -e["jump_force"]
            # 중력
            if "velocity_y" not in e:
                e["velocity_y"] = 0
            e["velocity_y"] += 0.5
            e["y"] += e["velocity_y"]
            # 바닥 충돌
            if e["y"] + e["height"] > 550:
                e["y"] = 550 - e["height"]
                e["velocity_y"] = 0

        # flyer: 상하 or 좌우 부유
        if e["type"] == "flyer":
            e["y"] += math.sin(timer / 30) * e["speed"]

    # 플레이어와 적 충돌 체크
    check_enemy_collisions()


def check_enemy_collisions():
    """
    적과 플레이어, 적과 플레이어 총알 충돌 처리
    """
    global score
    player_rect = pygame.Rect(player["x"], player["y"], player["width"], player["height"])

    for e in level_designs[current_level]["enemies"][:]:
        e_rect = pygame.Rect(e["x"], e["y"], e["width"], e["height"])

        # 플레이어와 충돌
        if player_rect.colliderect(e_rect):
            damage_player(0.5)  # 부딪힐 때 조금씩 데미지

        # 플레이어 총알과 충돌
        for bullet in player["bullets"][:]:
            b_rect = pygame.Rect(bullet["x"] - bullet["radius"], bullet["y"] - bullet["radius"],
                                 bullet["radius"] * 2, bullet["radius"] * 2)
            if b_rect.colliderect(e_rect):
                # 적 제거
                if e in level_designs[current_level]["enemies"]:
                    level_designs[current_level]["enemies"].remove(e)
                # 점수 상승
                score += 50
                # 총알도 제거
                player["bullets"].remove(bullet)
                break  # 한 번에 여러 번 처리되지 않도록


def update_boss():
    """
    보스 존재 시 업데이트 (보스 총알 패턴 등)
    """
    global boss_bullets, score, game_state
    if not boss or not boss.get("active", False):
        return

    # 간단한 이동 AI (좌우로 움직이거나 등등)
    boss["x"] += boss["speed"]
    # 화면 범위에서 반전
    if boss["x"] < 0 or boss["x"] + boss["width"] > SCREEN_WIDTH:
        boss["speed"] *= -1

    # 보스 공격 쿨타임
    boss["attack_cooldown"] -= 1
    if boss["attack_cooldown"] <= 0:
        boss["attack_cooldown"] = 60
        # 스파이럴 패턴
        angle_step = 45
        for angle in range(0, 360, angle_step):
            rad = math.radians(angle + timer * 2)
            vx = boss["bullet_speed"] * math.cos(rad)
            vy = boss["bullet_speed"] * math.sin(rad)
            boss_bullets.append({
                "x": boss["x"] + boss["width"] // 2,
                "y": boss["y"] + boss["height"] // 2,
                "vx": vx,
                "vy": vy,
                "radius": 6,
                "color": RED
            })

    # 보스 총알 이동
    for b in boss_bullets[:]:
        b["x"] += b["vx"]
        b["y"] += b["vy"]
        # 화면 벗어나면 제거
        if b["x"] < 0 or b["x"] > SCREEN_WIDTH or b["y"] < 0 or b["y"] > SCREEN_HEIGHT:
            boss_bullets.remove(b)

    # 플레이어와 보스 총알 충돌
    player_rect = pygame.Rect(player["x"], player["y"], player["width"], player["height"])
    for b in boss_bullets[:]:
        b_rect = pygame.Rect(b["x"] - b["radius"], b["y"] - b["radius"],
                             b["radius"] * 2, b["radius"] * 2)
        if player_rect.colliderect(b_rect):
            damage_player(1)
            boss_bullets.remove(b)

    # 플레이어 총알이 보스에 맞으면 체력 감소
    boss_rect = pygame.Rect(boss["x"], boss["y"], boss["width"], boss["height"])
    for bullet in player["bullets"][:]:
        b_rect = pygame.Rect(bullet["x"] - bullet["radius"], bullet["y"] - bullet["radius"],
                             bullet["radius"] * 2, bullet["radius"] * 2)
        if b_rect.colliderect(boss_rect):
            boss["health"] -= 5
            player["bullets"].remove(bullet)
            # 보스 사망
            if boss["health"] <= 0:
                boss["active"] = False
                score += 1000
                # 게임 승리
                game_state = GameState.GAME_WIN


def update_moving_platforms():
    """
    움직이는 플랫폼 처리
    """
    for p in level_designs[current_level]["platforms"]:
        if "moving" in p and p["moving"]:
            p["x"] += p["speed"] * p["direction"]
            # 범위 이탈 시 방향 전환
            # range: 시작점 기준 왕복
            # p["range"] 만큼 왔다갔다
            # 일단 x 초기값 기억용 변수가 없으므로, 간단히 화면 범위로 판단
            if p["x"] < 0 or (p["x"] + p["width"]) > SCREEN_WIDTH:
                p["direction"] *= -1


def draw_gameplay():
    """
    게임 플레이 중 화면 그리기
    - 레벨 테마별 동적 배경
    - 플랫폼/적/보스/플레이어
    - 포털
    - HUD
    """
    # ---------------------------
    # 배경 그리기 (레벨 테마별)
    # ---------------------------
    theme = level_designs[current_level]["theme"]
    if theme == LevelTheme.FOREST:
        draw_forest_background()
    elif theme == LevelTheme.CAVE:
        draw_cave_background()
    elif theme == LevelTheme.LAVA:
        draw_lava_background()
    elif theme == LevelTheme.ICE:
        draw_ice_background()
    elif theme == LevelTheme.SPACE:
        draw_space_background()
    else:
        screen.fill(BLACK)

    # ---------------------------
    # 플랫폼 그리기 (pygame.draw)
    # ---------------------------
    for p in level_designs[current_level]["platforms"]:
        # 테마별 색상
        color = BROWN
        if theme == LevelTheme.CAVE:
            color = GRAY
        elif theme == LevelTheme.LAVA:
            color = (255, 80, 0)
        elif theme == LevelTheme.ICE:
            color = LIGHT_BLUE
        elif theme == LevelTheme.SPACE:
            color = (50, 50, 70)

        pygame.draw.rect(screen, color, (p["x"], p["y"], p["width"], p["height"]))

        # 용암바닥이면 상단 테두리에 빨간색
        if theme == LevelTheme.LAVA and p["y"] == 550:
            pygame.draw.line(screen, RED, (p["x"], p["y"]), (p["x"] + p["width"], p["y"]), 3)

    # ---------------------------
    # 포털 그리기
    # ---------------------------
    portal = level_designs[current_level]["exit_portal"]
    if portal:
        # 반짝이는 원형 포털
        portal_x = portal["x"]
        portal_y = portal["y"]
        portal_radius = 20 + int(5 * abs(math.sin(timer / 10)))
        pygame.draw.circle(screen, (0, 255, 100), (portal_x, portal_y), portal_radius)
        pygame.draw.circle(screen, WHITE, (portal_x, portal_y), portal_radius, 2)

    # ---------------------------
    # 아이템/파워업/수집품
    # ---------------------------
    for c in level_designs[current_level]["collectibles"]:
        if not c["collected"]:
            # 작은 보석 형태
            crystal_points = [
                (c["x"], c["y"] - 5),
                (c["x"] + 10, c["y"]),
                (c["x"], c["y"] + 10),
                (c["x"] - 10, c["y"])
            ]
            pygame.draw.polygon(screen, CYAN, crystal_points)
            pygame.draw.polygon(screen, WHITE, crystal_points, 1)

    # 파워업
    for p in level_designs[current_level]["power_ups"]:
        if not p["collected"]:
            color = YELLOW
            if p["type"] == "health":
                color = GREEN
            elif p["type"] == "speed":
                color = ORANGE
            elif p["type"] == "jump":
                color = PINK
            elif p["type"] == "shield":
                color = WHITE

            # 번쩍이는 사각형
            size = 10 + int(3 * abs(math.sin(timer / 5)))
            pygame.draw.rect(screen, color, (p["x"] - size//2, p["y"] - size//2, size, size))
            pygame.draw.rect(screen, BLACK, (p["x"] - size//2, p["y"] - size//2, size, size), 1)

    # ---------------------------
    # 적 그리기
    # ---------------------------
    for e in level_designs[current_level]["enemies"]:
        # 적 타입별로 색 지정
        color = RED
        if e["type"] == "walker":
            color = (200, 0, 0)
        elif e["type"] == "flyer":
            color = (255, 128, 0)
        elif e["type"] == "jumper":
            color = (255, 0, 128)

        pygame.draw.rect(screen, color, (e["x"], e["y"], e["width"], e["height"]))

    # ---------------------------
    # 보스 그리기 (마지막 레벨)
    # ---------------------------
    if current_level == 4 and boss and boss.get("active", False):
        pygame.draw.rect(screen, PURPLE, (boss["x"], boss["y"], boss["width"], boss["height"]))
        # 보스 체력바
        bar_width = 200
        bar_height = 10
        bar_x = SCREEN_WIDTH // 2 - bar_width // 2
        bar_y = 50
        ratio = boss["health"] / 100
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, int(bar_width * ratio), bar_height))

        # 보스 총알
        for b in boss_bullets:
            pygame.draw.circle(screen, b["color"], (int(b["x"]), int(b["y"])), b["radius"])

    # ---------------------------
    # 플레이어 그리기
    # ---------------------------
    # 무적 상태면 반짝이는 효과
    if player["invincible"]:
        blink = int(timer % 2)
        if blink == 0:
            player_color = BLUE
        else:
            player_color = WHITE
    else:
        player_color = BLUE

    pygame.draw.rect(screen, player_color, (player["x"], player["y"], player["width"], player["height"]))
    # 머리(원)
    pygame.draw.circle(screen, LIGHT_BLUE, (player["x"] + player["width"]//2, player["y"] - 10), 10)

    # 플레이어 총알
    for bullet in player["bullets"]:
        pygame.draw.circle(screen, bullet["color"], (int(bullet["x"]), int(bullet["y"])), bullet["radius"])

    # ---------------------------
    # HUD (점수, 라이프, 체력)
    # ---------------------------
    score_text = hud_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    lives_text = hud_font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(lives_text, (10, 40))

    health_ratio = player["health"] / player["max_health"]
    pygame.draw.rect(screen, RED, (10, 70, 100, 10))
    pygame.draw.rect(screen, GREEN, (10, 70, int(100 * health_ratio), 10))

    gem_text = hud_font.render(f"Gems: {collected_gems}/{total_gems}", True, CYAN)
    screen.blit(gem_text, (10, 90))


def draw_forest_background():
    screen.fill(DARK_GREEN)
    # 구름 이동
    for cloud in clouds:
        cloud["x"] += cloud["speed"]
        if cloud["x"] > SCREEN_WIDTH + 200:
            cloud["x"] = -200
            cloud["y"] = random.randint(50, 150)
        # 구름 그리기
        cloud_width = int(80 * cloud["size"])
        cloud_height = int(40 * cloud["size"])
        pygame.draw.ellipse(screen, WHITE, (cloud["x"], cloud["y"], cloud_width, cloud_height))


def draw_cave_background():
    screen.fill(BLACK)
    # 물방울 상승
    for bubble in bubbles:
        bubble["y"] -= bubble["speed"]
        if bubble["y"] < -50:
            bubble["y"] = SCREEN_HEIGHT + 50
            bubble["x"] = random.randint(0, SCREEN_WIDTH)
        pygame.draw.circle(screen, BLUE, (bubble["x"], int(bubble["y"])), bubble["size"])


def draw_lava_background():
    screen.fill((100, 0, 0))
    # 용암 파티클
    for lp in lava_particles:
        lp["y"] -= lp["speed"]
        lp["lifetime"] -= 1
        if lp["lifetime"] <= 0:
            lp["x"] = random.randint(0, SCREEN_WIDTH)
            lp["y"] = random.randint(550, 600)
            lp["lifetime"] = random.randint(30, 60)

        pygame.draw.rect(screen, (255, 80, 0), (lp["x"], lp["y"], 3, lp["height"]))


def draw_ice_background():
    screen.fill((180, 220, 255))
    # 눈
    for flake in snowflakes:
        flake["y"] += flake["speed"]
        flake["x"] += flake["wobble"]
        if flake["y"] > SCREEN_HEIGHT:
            flake["y"] = random.randint(-50, 0)
            flake["x"] = random.randint(0, SCREEN_WIDTH)
        pygame.draw.circle(screen, WHITE, (int(flake["x"]), int(flake["y"])), flake["size"])


def draw_space_background():
    screen.fill(BLACK)
    # 별
    for star in stars:
        star["y"] += star["speed"]
        if star["y"] > SCREEN_HEIGHT:
            star["x"] = random.randint(0, SCREEN_WIDTH)
            star["y"] = 0
        pygame.draw.circle(screen, WHITE, (int(star["x"]), int(star["y"])), star["size"])

    # 우주 잔해
    for debris in space_debris:
        debris["x"] += debris["speed_x"]
        debris["y"] += debris["speed_y"]
        debris["rotation"] += debris["rotation_speed"]
        if debris["x"] < 0 or debris["x"] > SCREEN_WIDTH:
            debris["speed_x"] *= -1
        if debris["y"] < 0 or debris["y"] > SCREEN_HEIGHT:
            debris["speed_y"] *= -1

        # 잔해는 간단히 사각형으로 그리고 회전은 무시(시각효과로 치환)
        size = debris["size"]
        color = GRAY
        # 회전 효과 대신 색상 번쩍
        r = int(100 + 155 * abs(math.sin(debris["rotation"] / 20)))
        g = int(100 + 155 * abs(math.cos(debris["rotation"] / 25)))
        b = int(100 + 155 * abs(math.sin(debris["rotation"] / 30)))
        color = (r, g, b)

        pygame.draw.rect(screen, color, (debris["x"], debris["y"], size, size))


def check_portal_collision():
    """
    플레이어가 포털에 닿았는지 체크해서 레벨 이동
    """
    global current_level, game_state
    portal = level_designs[current_level]["exit_portal"]
    if not portal:
        return
    portal_rect = pygame.Rect(portal["x"] - 20, portal["y"] - 20, 40, 40)
    player_rect = pygame.Rect(player["x"], player["y"], player["width"], player["height"])

    if player_rect.colliderect(portal_rect):
        # 다음 레벨로 이동
        current_level += 1
        if current_level >= len(level_designs):
            # 마지막 레벨 이후면 게임 승리
            game_state = GameState.GAME_WIN
        else:
            # 레벨 초기화
            reset_level()


def update_effects():
    """
    파워업 효과 해제 등을 위한 타이머 처리
    """
    global player
    for eff in effects[:]:
        eff["timer"] -= 1
        if eff["timer"] <= 0:
            # 효과 종료
            if eff["type"] == "speed":
                player["speed"] = 5
            elif eff["type"] == "jump":
                player["jump_force"] = 12
            effects.remove(eff)


def main():
    global game_state, timer, current_level, score, lives, collected_gems

    running = True
    while running:
        clock.tick(FPS)
        timer += 1

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if game_state == GameState.TITLE:
                    if event.key == pygame.K_SPACE:
                        # 게임 시작
                        game_state = GameState.PLAYING
                elif game_state in (GameState.GAME_OVER, GameState.GAME_WIN):
                    if event.key == pygame.K_r:
                        # 재시작
                        current_level = 0
                        score = 0
                        lives = 3
                        collected_gems = 0
                        game_state = GameState.PLAYING
                        reset_level()

        # 상태별 로직
        if game_state == GameState.TITLE:
            draw_title_screen()

        elif game_state == GameState.PLAYING:
            handle_input()
            update_player()
            update_enemies()
            update_boss()
            update_moving_platforms()
            update_effects()
            check_portal_collision()

            # 플레이 화면 그리기
            draw_gameplay()

            # 플레이어 체력이 0 이하이면 이미 처리됨
            # 레벨 완료/승리는 보스 잡았거나 포털 통과

        elif game_state == GameState.GAME_OVER:
            draw_game_over_screen()

        elif game_state == GameState.GAME_WIN:
            draw_game_win_screen()

        pygame.display.flip()

    pygame.quit()
    sys.exit()


# 실제 게임 실행
if __name__ == "__main__":
    main()
