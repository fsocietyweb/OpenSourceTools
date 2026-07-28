import pygame
import random
import time
import sys
import os
import json
from pypresence import Presence

# ==========================================
# SAVE STATE SETUP (~/.fnafpp-savestates)
# ==========================================
SAVE_DIR = os.path.expanduser("~")
SAVE_FILE = os.path.join(SAVE_DIR, ".fnafpp-savestates")

def load_save_state():
    default_data = {
        "lang": "EN",
        "diff_idx": 0,
        "faz_coins": 0,
        "max_battery": 100,
        "noise_reduction": 0,
        "has_distraction": False,
        "shift_number": 1
    }
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
                for k, v in default_data.items():
                    if k not in data:
                        data[k] = v
                return data
        except Exception:
            return default_data
    return default_data

def save_game_state(game_instance):
    data = {
        "lang": game_instance.lang,
        "diff_idx": game_instance.diff_idx,
        "faz_coins": game_instance.faz_coins,
        "max_battery": game_instance.max_battery,
        "noise_reduction": game_instance.noise_reduction,
        "has_distraction": game_instance.has_distraction,
        "shift_number": game_instance.shift_number
    }
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)
    except Exception:
        pass

saved_data = load_save_state()

# ==========================================
# DISCORD RICH PRESENCE SETUP
# ==========================================
CLIENT_ID = "1531424838231658576"

rpc = None
try:
    rpc = Presence(CLIENT_ID)
    rpc.connect()
    print("[+] Discord Rich Presence v2.6 verbunden!")
except Exception:
    rpc = None

shift_start_time = time.time()

def update_discord_status(state_text, details_text="Version 2.6 - Night Shift", keep_timer=True):
    global shift_start_time
    if rpc:
        try:
            if not keep_timer:
                shift_start_time = time.time()
            rpc.update(state=state_text, details=details_text, start=shift_start_time)
        except Exception:
            pass

update_discord_status("Booting Up v2.6...", "FNaF Pizza Plex", keep_timer=False)

# ==========================================
# PYGAME SETUP
# ==========================================
try:
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
except Exception:
    pygame.init()

pygame.font.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("FNaF Pizza Plex - v2.6")

# Farben (Verbesserte Farbpalette für moderneres GUI-Design)
BG_DARK = (12, 12, 18)
PANEL_BG = (22, 22, 32)
WHITE = (240, 240, 240)
GREEN = (46, 204, 113)
RED = (231, 76, 60)
YELLOW = (241, 196, 15)
GRAY = (127, 140, 141)
DARK_GRAY = (35, 35, 50)
BLUE = (52, 152, 219)
PURPLE = (155, 89, 182)
CYAN = (0, 255, 255)

# Schriften
FONT_LARGE = pygame.font.SysFont("Arial", 36, bold=True)
FONT_MED = pygame.font.SysFont("Arial", 22, bold=True)
FONT_SMALL = pygame.font.SysFont("Arial", 16)

# Spielzustände
STATE_WARNING = "WARNING"
STATE_MAIN_MENU = "MAIN_MENU"
STATE_SETTINGS = "SETTINGS"
STATE_PAUSE_MENU = "PAUSE_MENU"  # NEU: Ersetzt Exit bei ESC im Game
STATE_MENU = "MENU"
STATE_SHOP = "SHOP"
STATE_WORKING = "WORKING"
STATE_CAMS = "CAMS"
STATE_HIDDEN = "HIDDEN"
STATE_MINIGAME = "MINIGAME"
STATE_FUSE_RESET = "FUSE_RESET"
STATE_GAME_OVER = "GAME_OVER"
STATE_NEXT_SHIFT_PROMPT = "NEXT_SHIFT_PROMPT"
STATE_EXIT_MSG = "EXIT_MSG"

TASK_GROUPS = {
    "Reboot.task": [
        ("Reboot security systems", 3), 
        ("Calibrate security cameras", 4), 
        ("Override firewall", 5)
    ],
    "Cooling.task": [
        ("Cool down pizza ovens", 2), 
        ("Fix main ventilation A/C", 4), 
        ("Replace coolant tubes", 6)
    ],
    "Cleaning.task": [
        ("Clean animatronic parts", 5), 
        ("Clean up party rooms", 3), 
        ("Sanitize ball pit", 4)
    ],
    "Service.task": [
        ("Empty trash compactors", 2), 
        ("Restock Gift Shop", 4), 
        ("Collect Faz-Coins", 2), 
        ("Repair Arcade Cabinet", 5)
    ],
    "Audio.task": [
        ("Fix stage speakers", 3), 
        ("Tune Freddy's microphone", 4), 
        ("Reset soundboard", 3)
    ]
}

DIFF_LEVELS = ["Super Easy", "Easy", "Medium", "Hard", "Super Hard", "Insane", "Super Insane", "Extreme Insane"]

# TRANSLATION DICTIONARY
TEXTS = {
    "DE": {
        "warn_title": "=== WARNUNG & CREDITS (v2.6) ===",
        "warn_1": "WARNUNG: Dieses Spiel enthält blinkende Lichter, laute Geräusche und Jumpscares.",
        "warn_2": "Sicherheits-Protokoll: Überwache die erweiterte Mini-Map und halte deine Türen intakt.",
        "warn_3": "Credits: ItsShytech & LennyDev | Save-State aktiv in ~/.fnafpp-savestates",
        "warn_press": "Drücke [ENTER] um fortzufahren",
        "main_title": "=== FNAF PIZZA PLEX v2.6 ===",
        "m_start": "[1] Start Shift {shift}",
        "m_options": "[2] Options (Settings & Language)",
        "m_exit": "[3] Exit Game",
        "pause_title": "=== SPIEL PAUSIERT ===",
        "p_resume": "[1] Weiterspielen",
        "p_settings": "[2] Options",
        "p_menu": "[3] Zurück zum Hauptmenü",
        "lang_title": "=== SPRACHE AUSWÄHLEN / SELECT LANGUAGE ===",
        "diff_title": "SCHWIERIGKEITSGRAD WÄHLEN",
        "prompt_title": "🎉 SCHICHT GESCHAFFT! 6:00 AM 🎉",
        "prompt_ask": "Möchtest du weitermachen?",
        "prompt_y": "Drücke [Y] - Ja, nächste Schicht (+1 Schwerer!)",
        "prompt_n": "Drücke [N] - Nein, Schicht beenden",
        "exit_thanks": "Danke fürs Spielen! Dein Fortschritt wurde gespeichert.",
        "exit_press": "Drücke [ALT + F4], um das Spiel zu beenden.",
        "door_warn": "⚡ ANIMATRONIC NAHE DER {side} TÜR! Spamme {key} 3x zum Schließen! ({time:.1f}s) ⚡",
        "door_status": "Tür-Status: {count}/3 Drücke"
    },
    "EN": {
        "warn_title": "=== WARNING & CREDITS (v2.6) ===",
        "warn_1": "WARNING: This game contains flashing lights, loud noises and sudden jump scares.",
        "warn_2": "Security Protocol: Monitor the expanded Mini-Map and keep your doors secured.",
        "warn_3": "Credits: ItsShytech & LennyDev | Save-State active in ~/.fnafpp-savestates",
        "warn_press": "Press [ENTER] to Continue",
        "main_title": "=== FNAF PIZZA PLEX v2.6 ===",
        "m_start": "[1] Start Shift {shift}",
        "m_options": "[2] Options (Settings & Language)",
        "m_exit": "[3] Exit Game",
        "pause_title": "=== GAME PAUSED ===",
        "p_resume": "[1] Resume Shift",
        "p_settings": "[2] Options",
        "p_menu": "[3] Return to Main Menu",
        "lang_title": "=== SELECT LANGUAGE ===",
        "diff_title": "SELECT DIFFICULTY LEVEL",
        "prompt_title": "🎉 SHIFT COMPLETED! 6:00 AM 🎉",
        "prompt_ask": "Do you want to continue?",
        "prompt_y": "Press [Y] - Yes, next shift (+1 Harder!)",
        "prompt_n": "Press [N] - No, end shift",
        "exit_thanks": "Thanks for playing! Your progress has been saved.",
        "exit_press": "Press [ALT + F4] to exit the game.",
        "door_warn": "⚡ ANIMATRONIC NEAR {side} DOOR! Spam {key} 3x to Close! ({time:.1f}s) ⚡",
        "door_status": "Door Status: {count}/3 Presses"
    },
    "FEMISH": {
        "warn_title": "=== OwO WAWNING & CWEDITS (v2.6) UwU ===",
        "warn_1": "WAWNING: Bwinkin wights, woud nwoises and jwumpscawes... OwO be cawefuw!",
        "warn_2": "Secuwity Pwotocow: Watch da expanded Mini-Map and keep doowies safe UwU",
        "warn_3": "Cwewits: ItsShytech & WennyDev | Save-State active in ~/.fnafpp-savestates >w<",
        "warn_press": "Pwwess [ENTER] to Cwontinue OwO",
        "main_title": "=== OwO FNAF PIZZA PLEX v2.6 UwU ===",
        "m_start": "[1] Stawt Shift {shift} OwO",
        "m_options": "[2] Options (Settings & Wanguage) UwU",
        "m_exit": "[3] Bwye Bwye Game OwO",
        "pause_title": "=== OwO PAUSE MENU UwU ===",
        "p_resume": "[1] Cwontinue Pwaying OwO",
        "p_settings": "[2] Options UwU",
        "p_menu": "[3] Bwack to Main Menwu >w<",
        "lang_title": "=== S3W3CT WANGUAGE OwO ===",
        "diff_title": "CHOOSE DIFFICUWTY UwU",
        "prompt_title": "🎉 SHIFT COMPWETED 6:00 AM! OwO 🎉",
        "prompt_ask": "Wanna cwontinue? UwU",
        "prompt_y": "Pwwess [Y] - Yesh (+1 Hawdew!) OwO",
        "prompt_n": "Pwwess [N] - Nwo, bwye bwye UwU",
        "exit_thanks": "Thawnk ywooo fow pwaying! Saved in ~/.fnafpp-savestates OwO",
        "exit_press": "Pwwess [ALT + F4] to gwo away UwU",
        "door_warn": "⚡ OwO ANIMATWONIC NEAR {side} DWOOW! Spam {key} 3x! ({time:.1f}s) UwU ⚡",
        "door_status": "Dwoow Stwatus: {count}/3 Pwwesses OwO"
    }
}

class Game:
    def __init__(self):
        self.version = "2.6"
        self.state = STATE_WARNING
        self.lang = saved_data["lang"]
        self.shift_number = saved_data["shift_number"]
        self.diff_idx = saved_data["diff_idx"]
        self.difficulty = DIFF_LEVELS[self.diff_idx]
        
        self.max_battery = saved_data["max_battery"]
        self.battery = self.max_battery
        self.faz_coins = saved_data["faz_coins"]
        self.noise_reduction = saved_data["noise_reduction"]
        self.has_distraction = saved_data["has_distraction"]
        
        self.tasks = []
        self.completed_count = 0
        self.total_task_count = 25
        self.current_task = None
        self.task_step = 0
        self.task_noise = 0
        
        # Animatronic / Map Variablen
        self.attack_timer_start = 0
        self.danger_active = False
        self.attack_side = "LEFT"
        self.anim_spawn_point = 1 
        self.anim_progress = 0.0  
        self.door_spam_count = 0
        self.is_level_5 = False
        self.is_fast_attack = False
        self.hide_timer_start = 0
        self.hide_time_limit = 0
        self.level_5_wait_end = 0
        
        self.recharging = False
        self.recharge_end_time = 0
        self.active_cam = 1
        self.cam_distraction_used = False

        # Minigame & Fuse Box
        self.minigame_type = None
        self.mg_score = 0
        self.mg_timer = 0
        self.mg_coin_x = 0
        self.mg_coin_y = 0
        self.mg_basket_x = WIDTH // 2
        self.fuses_needed = 3
        self.fuses_fixed = 0

    def get_txt(self, msg_key, **kwargs):
        t = TEXTS[self.lang].get(msg_key, "")
        return t.format(**kwargs) if kwargs else t

    def auto_start_shift(self):
        self.diff_idx = min(self.shift_number - 1, len(DIFF_LEVELS) - 1)
        self.difficulty = DIFF_LEVELS[self.diff_idx]
        self.init_shift()

    def increase_difficulty_and_shift(self):
        self.shift_number += 1
        if self.diff_idx < len(DIFF_LEVELS) - 1:
            self.diff_idx += 1
        self.difficulty = DIFF_LEVELS[self.diff_idx]
        save_game_state(self)
        self.init_shift()

    def init_shift(self):
        if self.difficulty == "Super Easy":
            self.total_task_count = 20
        elif self.difficulty == "Easy":
            self.total_task_count = 22
        elif self.difficulty == "Medium":
            self.total_task_count = 25
        elif self.difficulty == "Hard":
            self.total_task_count = 25
        elif self.difficulty == "Super Hard":
            self.total_task_count = 30
        elif self.difficulty == "Insane":
            self.total_task_count = 12
        elif self.difficulty == "Super Insane":
            self.total_task_count = 8
        elif self.difficulty == "Extreme Insane":
            self.total_task_count = 40

        self.completed_count = 0
        self.battery = self.max_battery
        self.tasks = []
        self.attack_timer_start = time.time()
        self.cam_distraction_used = False
        
        for i in range(1, self.total_task_count + 1):
            group_name = random.choice(list(TASK_GROUPS.keys()))
            sub_task_info = random.choice(TASK_GROUPS[group_name])
            sub_task_name, duration = sub_task_info
            self.tasks.append({
                "id": i,
                "group": group_name,
                "name": f"{sub_task_name} #{i}",
                "duration": duration,
                "completed": False
            })
            
        self.state = STATE_MENU
        save_game_state(self)
        update_discord_status(f"Shift {self.shift_number} | Tasks: 0/{self.total_task_count}", f"Diff: {self.difficulty}", keep_timer=False)

    def cheat_skip_night(self):
        print("[⚡] CHEAT CODE ACTIVATED! Skipping Night...")
        for task in self.tasks:
            task["completed"] = True
        self.completed_count = self.total_task_count
        self.danger_active = False
        update_discord_status("Cheater! Skipped Shift...", "Using Dev Hax")
        self.start_random_minigame()

    def start_task(self, task):
        if not task["completed"]:
            self.current_task = task
            self.task_step = 0
            self.task_noise = 0
            self.danger_active = False
            self.state = STATE_WORKING
            update_discord_status(f"Shift {self.shift_number} | Tasks: {self.completed_count}/{self.total_task_count}", f"Working: Task #{task['id']}")

    def get_animatronic_count(self):
        if self.difficulty == "Super Easy": return 1
        elif self.difficulty == "Easy": return 2
        elif self.difficulty == "Medium": return 3
        elif self.difficulty == "Hard": return 4
        elif self.difficulty == "Super Hard": return 5
        elif self.difficulty == "Insane": return 6
        elif self.difficulty == "Extreme Insane": return 7
        return 9

    def trigger_danger_event(self):
        if self.has_distraction:
            self.has_distraction = False
            save_game_state(self)
            print("[+] Distraction Device used automatically! Danger averted.")
            return

        self.danger_active = True
        self.attack_side = random.choice(["LEFT", "RIGHT"])
        self.anim_spawn_point = random.randint(1, 3) 
        self.anim_progress = 0.0  
        self.door_spam_count = 0
        self.is_level_5 = random.random() < (0.4 if "Hard" in self.difficulty or "Insane" in self.difficulty else 0.15)
        self.is_fast_attack = random.random() < 0.3 if "Super" in self.difficulty else False
        
        base_time = 4.0 + (self.anim_spawn_point * 3.0) 
        if self.is_fast_attack:
            self.hide_time_limit = random.uniform(2.5, 4.0)
        else:
            self.hide_time_limit = base_time + (5 if self.is_level_5 else 3)
            
        self.hide_timer_start = time.time()
        update_discord_status(f"Shift {self.shift_number} | Tasks: {self.completed_count}/{self.total_task_count}", f"DANGER! Attack from {self.attack_side} (Spawn {self.anim_spawn_point})")

    def handle_door_block(self, key_pressed):
        if not self.danger_active:
            return

        correct_key = pygame.K_l if self.attack_side == "LEFT" else pygame.K_r
        if key_pressed == correct_key:
            self.door_spam_count += 1
            if self.door_spam_count >= 3:
                if random.random() < 0.98:
                    self.danger_active = False
                    self.door_spam_count = 0
                    self.anim_progress = 0.0
                    print("[+] Animatronic blocked by door!")
                    update_discord_status(f"Shift {self.shift_number} | Tasks: {self.completed_count}/{self.total_task_count}", "Door Blocked Successfully")
                else:
                    self.state = STATE_GAME_OVER
                    update_discord_status("Game Over", "Door failed (2% breach)!")

    def do_task_step(self):
        if self.danger_active or self.state == STATE_HIDDEN:
            return

        self.task_step += 1
        self.battery -= random.randint(2, 4)
        
        raw_noise = random.randint(20, 95)
        self.task_noise = max(0, raw_noise - self.noise_reduction)

        if self.battery <= 0:
            self.battery = 0
            self.fuses_fixed = 0
            self.state = STATE_FUSE_RESET
            update_discord_status(f"Shift {self.shift_number} | Tasks: {self.completed_count}/{self.total_task_count}", "POWER OUTAGE!")
            return

        chance = 0.05 if self.difficulty == "Super Easy" else 0.2
        if "Hard" in self.difficulty or "Insane" in self.difficulty:
            chance = 0.45

        if self.task_noise > 60 and random.random() < chance:
            self.trigger_danger_event()

        if self.task_step >= self.current_task["duration"] and not self.danger_active:
            self.current_task["completed"] = True
            self.completed_count += 1
            self.faz_coins += random.randint(5, 12)
            save_game_state(self)
            
            if self.completed_count == self.total_task_count:
                self.start_random_minigame()
            else:
                self.state = STATE_MENU
                update_discord_status(f"Shift {self.shift_number} | Tasks: {self.completed_count}/{self.total_task_count}", f"Diff: {self.difficulty}")

    def trigger_hide(self):
        if not self.danger_active:
            return

        elapsed = time.time() - self.hide_timer_start
        if elapsed <= self.hide_time_limit:
            self.state = STATE_HIDDEN
            wait_sec = random.randint(6, 10) if self.is_level_5 else 2
            self.level_5_wait_end = time.time() + wait_sec
            update_discord_status(f"Shift {self.shift_number} | Tasks: {self.completed_count}/{self.total_task_count}", "Hiding in the Dark...")
        else:
            self.state = STATE_GAME_OVER
            update_discord_status("Game Over", "Caught by Animatronic")

    def switch_cam(self, cam_num):
        self.active_cam = cam_num
        self.battery -= 1
        if self.battery <= 0:
            self.battery = 0
            self.fuses_fixed = 0
            self.state = STATE_FUSE_RESET

    def use_cam_distraction(self):
        if self.danger_active and not self.cam_distraction_used:
            self.cam_distraction_used = True
            self.danger_active = False
            self.anim_progress = 0.0
            print("[+] Camera Audio Distraction deployed! Animatronic distracted.")
            update_discord_status(f"Shift {self.shift_number} | Tasks: {self.completed_count}/{self.total_task_count}", "Cam Distraction Success")

    def start_random_minigame(self):
        self.state = STATE_MINIGAME
        self.minigame_type = random.choice(["coin_catcher", "speed_click"])
        self.mg_score = 0
        self.mg_timer = time.time() + 10
        self.mg_coin_x = random.randint(100, WIDTH - 100)
        self.mg_coin_y = 0

    def draw_office_map(self):
        map_w, map_h = 240, 190
        map_x = WIDTH - map_w - 20
        map_y = HEIGHT - map_h - 20

        # Modernes HUD-Panel Design für die Map
        pygame.draw.rect(SCREEN, PANEL_BG, (map_x, map_y, map_w, map_h), border_radius=8)
        pygame.draw.rect(SCREEN, BLUE, (map_x, map_y, map_w, map_h), 2, border_radius=8)

        lbl = FONT_SMALL.render(f"EXPANDED MAP (Spawn {self.anim_spawn_point})", True, WHITE)
        SCREEN.blit(lbl, (map_x + 12, map_y + 8))

        pygame.draw.rect(SCREEN, DARK_GRAY, (map_x + 20, map_y + 30, map_w - 40, 20), border_radius=4)
        s_lbl = FONT_SMALL.render("SPAWNS [1, 2, 3]", True, GRAY)
        SCREEN.blit(s_lbl, (map_x + (map_w//2) - 45, map_y + 32))

        pygame.draw.line(SCREEN, GRAY, (map_x + 35, map_y + 50), (map_x + 35, map_y + 145), 3)
        pygame.draw.line(SCREEN, GRAY, (map_x + map_w - 35, map_y + 50), (map_x + map_w - 35, map_y + 145), 3)

        off_x, off_y, off_w, off_h = map_x + 60, map_y + 140, map_w - 120, 40
        pygame.draw.rect(SCREEN, DARK_GRAY, (off_x, off_y, off_w, off_h), border_radius=4)
        pygame.draw.rect(SCREEN, WHITE, (off_x, off_y, off_w, off_h), 1, border_radius=4)

        door_w, door_h = 6, 20
        pygame.draw.rect(SCREEN, YELLOW, (off_x - door_w, off_y + 10, door_w, door_h), border_radius=2)
        pygame.draw.rect(SCREEN, YELLOW, (off_x + off_w, off_y + 10, door_w, door_h), border_radius=2)

        pygame.draw.circle(SCREEN, GREEN, (off_x + (off_w // 2), off_y + (off_h // 2)), 6)

        if self.danger_active:
            start_y_offset = 35 + ((self.anim_spawn_point - 1) * 15)
            start_y_pos = map_y + start_y_offset
            end_y_pos = off_y + 20
            curr_y = start_y_pos + (end_y_pos - start_y_pos) * self.anim_progress

            if self.attack_side == "LEFT":
                curr_x = map_x + 35
            else:
                curr_x = map_x + map_w - 35

            pygame.draw.circle(SCREEN, RED, (int(curr_x), int(curr_y)), 7)

    def update(self):
        interval = 9999
        if "Hard" in self.difficulty or "Super Hard" in self.difficulty:
            interval = random.randint(80, 130)

        if self.state in [STATE_MENU, STATE_WORKING] and time.time() - self.attack_timer_start >= interval:
            self.attack_timer_start = time.time()
            self.trigger_danger_event()

        if self.recharging and time.time() >= self.recharge_end_time:
            self.battery = min(self.max_battery, self.battery + 35)
            self.recharging = False

        if self.danger_active and self.state == STATE_WORKING:
            elapsed = time.time() - self.hide_timer_start
            self.anim_progress = min(1.0, elapsed / self.hide_time_limit)

            if elapsed > self.hide_time_limit:
                self.state = STATE_GAME_OVER
                update_discord_status("Game Over", "Too Slow!")

        if self.state == STATE_HIDDEN and time.time() >= self.level_5_wait_end:
            self.danger_active = False
            self.state = STATE_WORKING
            if self.task_step >= self.current_task["duration"]:
                self.current_task["completed"] = True
                self.completed_count += 1
                self.faz_coins += random.randint(5, 12)
                save_game_state(self)
                
                if self.completed_count == self.total_task_count:
                    self.start_random_minigame()
                else:
                    self.state = STATE_MENU

        if self.state == STATE_MINIGAME:
            if time.time() >= self.mg_timer:
                self.faz_coins += self.mg_score * 2
                save_game_state(self)
                self.state = STATE_NEXT_SHIFT_PROMPT
                update_discord_status("6:00 AM!", "Shift Completed")
            elif self.minigame_type == "coin_catcher":
                self.mg_coin_y += 8
                if self.mg_coin_y >= HEIGHT - 100:
                    if abs(self.mg_coin_x - self.mg_basket_x) < 80:
                        self.mg_score += 1
                    self.mg_coin_x = random.randint(100, WIDTH - 100)
                    self.mg_coin_y = 0

game = Game()
clock = pygame.time.Clock()

# Main Loop
while True:
    SCREEN.fill(BG_DARK)
    game.update()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_u] and keys[pygame.K_n] and keys[pygame.K_b]:
        if game.state in [STATE_MENU, STATE_WORKING, STATE_CAMS, STATE_HIDDEN, STATE_FUSE_RESET]:
            game.cheat_skip_night()
            time.sleep(0.3)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game_state(game)
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game.state in [STATE_MENU, STATE_WORKING, STATE_CAMS, STATE_SHOP]:
                    game.state = STATE_PAUSE_MENU
                elif game.state == STATE_SETTINGS:
                    game.state = STATE_MAIN_MENU
                elif game.state == STATE_PAUSE_MENU:
                    game.state = STATE_MENU
                elif game.state == STATE_MAIN_MENU:
                    save_game_state(game)
                    pygame.quit()
                    sys.exit()

            if game.state == STATE_WARNING:
                if event.key == pygame.K_RETURN:
                    game.state = STATE_MAIN_MENU

            elif game.state == STATE_MAIN_MENU:
                if event.key == pygame.K_1:
                    game.auto_start_shift()
                elif event.key == pygame.K_2:
                    game.state = STATE_SETTINGS
                elif event.key == pygame.K_3:
                    save_game_state(game)
                    pygame.quit()
                    sys.exit()

            elif game.state == STATE_PAUSE_MENU:
                if event.key == pygame.K_1:
                    game.state = STATE_MENU
                elif event.key == pygame.K_2:
                    game.state = STATE_SETTINGS
                elif event.key == pygame.K_3:
                    game.state = STATE_MAIN_MENU

            elif game.state == STATE_SETTINGS:
                if event.key == pygame.K_1:
                    game.lang = "DE"
                    save_game_state(game)
                elif event.key == pygame.K_2:
                    game.lang = "EN"
                    save_game_state(game)
                elif event.key == pygame.K_3:
                    game.lang = "FEMISH"
                    save_game_state(game)
                elif event.key == pygame.K_b:
                    if game.battery > 0:
                        game.state = STATE_MENU
                    else:
                        game.state = STATE_MAIN_MENU

            elif game.state == STATE_MENU:
                if event.key == pygame.K_s:
                    game.state = STATE_SHOP
                elif event.key == pygame.K_c:
                    game.state = STATE_CAMS

            elif game.state == STATE_SHOP:
                if event.key == pygame.K_s or event.key == pygame.K_ESCAPE:
                    game.state = STATE_MENU
                elif event.key == pygame.K_1 and game.faz_coins >= 10 and not game.recharging:
                    game.faz_coins -= 10
                    game.recharging = True
                    game.recharge_end_time = time.time() + 5
                    save_game_state(game)
                elif event.key == pygame.K_2 and game.faz_coins >= 20:
                    game.faz_coins -= 20
                    game.noise_reduction += 15
                    save_game_state(game)
                elif event.key == pygame.K_3 and game.faz_coins >= 30 and not game.has_distraction:
                    game.faz_coins -= 30
                    game.has_distraction = True
                    save_game_state(game)
                elif event.key == pygame.K_4 and game.faz_coins >= 50 and game.max_battery == 100:
                    game.faz_coins -= 50
                    game.max_battery = 150
                    game.battery = 150
                    save_game_state(game)

            elif game.state == STATE_CAMS:
                if event.key == pygame.K_c or event.key == pygame.K_ESCAPE:
                    game.state = STATE_MENU
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    game.switch_cam(int(event.unicode))
                elif event.key == pygame.K_SPACE: 
                    game.use_cam_distraction()

            elif game.state == STATE_WORKING:
                if event.key == pygame.K_RETURN and not game.danger_active:
                    game.do_task_step()
                elif event.key == pygame.K_h and game.danger_active:
                    game.trigger_hide()
                elif game.danger_active and event.key in [pygame.K_l, pygame.K_r]:
                    game.handle_door_block(event.key)

            elif game.state == STATE_FUSE_RESET:
                if event.key == pygame.K_SPACE:
                    game.fuses_fixed += 1
                    if game.fuses_fixed >= game.fuses_needed:
                        game.battery = 35
                        game.state = STATE_MENU

            elif game.state == STATE_MINIGAME and game.minigame_type == "speed_click":
                if event.key == pygame.K_SPACE:
                    game.mg_score += 1

            elif game.state == STATE_NEXT_SHIFT_PROMPT:
                if event.key == pygame.K_y:
                    game.increase_difficulty_and_shift()
                elif event.key == pygame.K_n:
                    game.state = STATE_EXIT_MSG

        elif event.type == pygame.MOUSEBUTTONDOWN and game.state == STATE_MENU:
            mx, my = pygame.mouse.get_pos()
            start_x = 50
            start_y = 150
            col_width = 240
            row_height = 65

            for idx, task in enumerate(game.tasks):
                col = idx // 5
                row = idx % 5
                tx = start_x + (col * col_width)
                ty = start_y + (row * row_height)

                task_rect = pygame.Rect(tx, ty, col_width - 15, row_height - 10)
                if task_rect.collidepoint(mx, my):
                    game.start_task(task)
                    break

    if game.state == STATE_MINIGAME and game.minigame_type == "coin_catcher":
        if keys[pygame.K_LEFT] and game.mg_basket_x > 50:
            game.mg_basket_x -= 10
        if keys[pygame.K_RIGHT] and game.mg_basket_x < WIDTH - 50:
            game.mg_basket_x += 10

    # RENDER ZUSTÄNDE (Mit verbessertem, modernen GUI-Design & abgerundeten Panels)
    if game.state == STATE_WARNING:
        SCREEN.blit(FONT_LARGE.render(game.get_txt("warn_title"), True, RED), (WIDTH//2 - 240, 80))
        w1 = FONT_MED.render(game.get_txt("warn_1"), True, WHITE)
        w2 = FONT_MED.render(game.get_txt("warn_2"), True, YELLOW)
        w3 = FONT_MED.render(game.get_txt("warn_3"), True, CYAN)
        w4 = FONT_LARGE.render(game.get_txt("warn_press"), True, GREEN)
        
        SCREEN.blit(w1, (WIDTH//2 - w1.get_width()//2, 220))
        SCREEN.blit(w2, (WIDTH//2 - w2.get_width()//2, 280))
        SCREEN.blit(w3, (WIDTH//2 - w3.get_width()//2, 340))
        SCREEN.blit(w4, (WIDTH//2 - w4.get_width()//2, 450))

    elif game.state == STATE_MAIN_MENU:
        SCREEN.blit(FONT_LARGE.render(game.get_txt("main_title"), True, CYAN), (WIDTH//2 - 220, 120))
        
        ms1 = FONT_MED.render(game.get_txt("m_start", shift=game.shift_number), True, GREEN)
        ms2 = FONT_MED.render(game.get_txt("m_options"), True, WHITE)
        ms3 = FONT_MED.render(game.get_txt("m_exit"), True, RED)

        SCREEN.blit(ms1, (WIDTH//2 - 180, 240))
        SCREEN.blit(ms2, (WIDTH//2 - 180, 310))
        SCREEN.blit(ms3, (WIDTH//2 - 180, 380))

        save_info = FONT_SMALL.render(f"Save-State Loaded: ~/.fnafpp-savestates | Coins: {game.faz_coins}", True, GRAY)
        SCREEN.blit(save_info, (WIDTH//2 - save_info.get_width()//2, HEIGHT - 80))

    elif game.state == STATE_PAUSE_MENU:
        # Dunkleres Overlay für das Pausemenü
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        SCREEN.blit(overlay, (0, 0))

        panel_w, panel_h = 420, 300
        panel_x = (WIDTH - panel_w) // 2
        panel_y = (HEIGHT - panel_h) // 2
        pygame.draw.rect(SCREEN, PANEL_BG, (panel_x, panel_y, panel_w, panel_h), border_radius=12)
        pygame.draw.rect(SCREEN, BLUE, (panel_x, panel_y, panel_w, panel_h), 2, border_radius=12)

        p_title = FONT_LARGE.render(game.get_txt("pause_title"), True, CYAN)
        p1 = FONT_MED.render(game.get_txt("p_resume"), True, GREEN)
        p2 = FONT_MED.render(game.get_txt("p_settings"), True, WHITE)
        p3 = FONT_MED.render(game.get_txt("p_menu"), True, RED)

        SCREEN.blit(p_title, (panel_x + (panel_w - p_title.get_width())//2, panel_y + 30))
        SCREEN.blit(p1, (panel_x + 40, panel_y + 110))
        SCREEN.blit(p2, (panel_x + 40, panel_y + 170))
        SCREEN.blit(p3, (panel_x + 40, panel_y + 230))

    elif game.state == STATE_SETTINGS:
        SCREEN.fill(BG_DARK)
        SCREEN.blit(FONT_LARGE.render("--- OPTIONS & SETTINGS (v2.6) ---", True, BLUE), (WIDTH//2 - 240, 60))
        
        lang_header = FONT_MED.render(f"Current Language: [{game.lang}] (Press 1: DE, 2: EN, 3: FEMISH)", True, YELLOW)
        SCREEN.blit(lang_header, (150, 140))

        c1 = FONT_MED.render("Controls & Info:", True, GREEN)
        c2 = FONT_SMALL.render("[S] - Open / Close Shop", True, WHITE)
        c3 = FONT_SMALL.render("[C] - Open Security Cams (Press SPACE for Cam Audio Distraction)", True, WHITE)
        c4 = FONT_SMALL.render("[H] - Hide from Animatronics when warned", True, WHITE)
        c5 = FONT_SMALL.render("[L] / [R] - Spam 3x to close Left or Right Door", True, CYAN)
        c6 = FONT_SMALL.render("[SPACE] - Fix Fuses during Power Outage", True, WHITE)
        c7 = FONT_SMALL.render("[ESC] - Open Pause Menu during gameplay", True, PURPLE)

        SCREEN.blit(c1, (150, 200))
        SCREEN.blit(c2, (150, 240))
        SCREEN.blit(c3, (150, 280))
        SCREEN.blit(c4, (150, 320))
        SCREEN.blit(c5, (150, 360))
        SCREEN.blit(c6, (150, 400))
        SCREEN.blit(c7, (150, 440))

        back = FONT_MED.render("Press [B] to return", True, GRAY)
        SCREEN.blit(back, (150, 520))

    elif game.state == STATE_MENU:
        title = FONT_MED.render(f"=== Shift {game.shift_number} | Tasks: {game.completed_count}/{game.total_task_count} | Diff: {game.difficulty} ===", True, WHITE)
        SCREEN.blit(title, (50, 30))
        
        status = FONT_SMALL.render(f"Battery: {game.battery}/{game.max_battery}% | Faz-Coins: {game.faz_coins} | Noise Red: -{game.noise_reduction}% | Distraction: {'YES' if game.has_distraction else 'NO'}", True, GREEN if game.battery > 30 else RED)
        SCREEN.blit(status, (50, 65))

        nav_info = FONT_SMALL.render("Press [S] Shop | [C] Security Cams | [ESC] Pause Menu", True, BLUE)
        SCREEN.blit(nav_info, (WIDTH - 500, 65))

        start_x = 50
        start_y = 150
        col_width = 240
        row_height = 65

        for idx, task in enumerate(game.tasks):
            col = idx // 5
            row = idx % 5
            tx = start_x + (col * col_width)
            ty = start_y + (row * row_height)

            box_color = PANEL_BG
            border_color = GREEN if task["completed"] else WHITE
            pygame.draw.rect(SCREEN, box_color, (tx, ty, col_width - 15, row_height - 10), border_radius=6)
            pygame.draw.rect(SCREEN, border_color, (tx, ty, col_width - 15, row_height - 10), 2, border_radius=6)

            status_str = "[DONE]" if task["completed"] else "[PENDING]"
            t_num = FONT_SMALL.render(f"Task #{task['id']}: {status_str}", True, GREEN if task["completed"] else YELLOW)
            t_grp = FONT_SMALL.render(f"{task['group']} ({task['duration']}s)", True, WHITE)

            SCREEN.blit(t_num, (tx + 10, ty + 8))
            SCREEN.blit(t_grp, (tx + 10, ty + 28))

        game.draw_office_map()

    elif game.state == STATE_FUSE_RESET:
        SCREEN.fill((20, 0, 0))
        SCREEN.blit(FONT_LARGE.render("⚡ POWER OUTAGE! FUSES BLOWN! ⚡", True, RED), (WIDTH//2 - 250, 150))
        SCREEN.blit(FONT_MED.render(f"Spam [SPACEBAR] to reset main fuse ({game.fuses_fixed}/{game.fuses_needed})", True, YELLOW), (WIDTH//2 - 260, 250))

    elif game.state == STATE_SHOP:
        SCREEN.fill((15, 15, 30))
        SCREEN.blit(FONT_LARGE.render("--- FAZ-BEAR SHOP (v2.6) ---", True, YELLOW), (WIDTH//2 - 200, 60))
        coins_txt = FONT_MED.render(f"Your Faz-Coins: {game.faz_coins}", True, WHITE)
        SCREEN.blit(coins_txt, (WIDTH//2 - coins_txt.get_width()//2, 110))

        s1 = FONT_MED.render("[Press 1] Recharge Battery (+35%) - Cost: 10 Faz-Coins", True, WHITE)
        s2 = FONT_MED.render("[Press 2] Noise Dampener (-15% Noise) - Cost: 20 Faz-Coins", True, WHITE)
        s3 = FONT_MED.render("[Press 3] Distraction Device (Auto-block 1 attack) - Cost: 30 Faz-Coins", True, CYAN)
        s4 = FONT_MED.render("[Press 4] Battery Upgrade (Max Battery 150%) - Cost: 50 Faz-Coins", True, GREEN)
        back = FONT_MED.render("Press [S] or [ESC] to Exit Shop", True, GRAY)

        SCREEN.blit(s1, (150, 180))
        SCREEN.blit(s2, (150, 240))
        SCREEN.blit(s3, (150, 300))
        SCREEN.blit(s4, (150, 360))
        SCREEN.blit(back, (150, 480))

    elif game.state == STATE_CAMS:
        SCREEN.fill((10, 20, 10))
        anim_count = game.get_animatronic_count()
        cam_title = FONT_LARGE.render(f"--- SECURITY CAM 0{game.active_cam} | Active Animatronics: {anim_count} ---", True, GREEN)
        SCREEN.blit(cam_title, (50, 50))
        pygame.draw.rect(SCREEN, GREEN, (50, 120, WIDTH - 100, HEIGHT - 250), 3, border_radius=8)
        SCREEN.blit(FONT_MED.render("NO IMMEDIATE ANIMATRONIC MOVEMENT IN THIS SECTOR", True, GREEN), (100, 200))
        
        distract_status = "READY" if not game.cam_distraction_used else "USED"
        SCREEN.blit(FONT_MED.render(f"Cam Audio Distraction System: [{distract_status}] - Press [SPACE] to Deploy", True, YELLOW), (100, 260))
        
        cam_controls = FONT_MED.render("Press [1], [2], [3], [4] to switch Cams | Press [C] or [ESC] to Close", True, WHITE)
        SCREEN.blit(cam_controls, (50, HEIGHT - 80))

    elif game.state == STATE_WORKING:
        title = FONT_LARGE.render(f"--- Task #{game.current_task['id']}: {game.current_task['name']} ---", True, WHITE)
        SCREEN.blit(title, (50, 100))

        progress = int((game.task_step / game.current_task["duration"]) * 100)
        SCREEN.blit(FONT_MED.render(f"Progress: {progress}%", True, WHITE), (50, 200))
        SCREEN.blit(FONT_MED.render(f"Noise Level: {game.task_noise}%", True, RED if game.task_noise > 70 else GREEN), (50, 250))
        SCREEN.blit(FONT_MED.render(f"Battery: {game.battery}%", True, YELLOW), (50, 300))

        if not game.danger_active:
            SCREEN.blit(FONT_MED.render("Press [ENTER] to perform action...", True, WHITE), (50, 400))
        else:
            rem_time = max(0, game.hide_time_limit - (time.time() - game.hide_timer_start))
            key_name = "[L]" if game.attack_side == "LEFT" else "[R]"
            warn_str = game.get_txt("door_warn", side=game.attack_side, key=key_name, time=rem_time)
            SCREEN.blit(FONT_LARGE.render(warn_str, True, RED), (50, 450))
            SCREEN.blit(FONT_MED.render(game.get_txt("door_status", count=game.door_spam_count), True, YELLOW), (50, 500))

        game.draw_office_map()

    elif game.state == STATE_HIDDEN:
        SCREEN.fill((5, 5, 15))
        SCREEN.blit(FONT_LARGE.render("... You are hiding in the dark ...", True, WHITE), (WIDTH//2 - 200, HEIGHT//2))

    elif game.state == STATE_MINIGAME:
        rem_time = max(0, int(game.mg_timer - time.time()))
        SCREEN.blit(FONT_LARGE.render(f"END OF SHIFT MINIGAME - Time Left: {rem_time}s | Score: {game.mg_score}", True, YELLOW), (50, 50))
        if game.minigame_type == "coin_catcher":
            SCREEN.blit(FONT_MED.render("Use [LEFT] & [RIGHT] Arrows to catch Faz-Coins!", True, WHITE), (50, 100))
            pygame.draw.circle(SCREEN, YELLOW, (game.mg_coin_x, int(game.mg_coin_y)), 20)
            pygame.draw.rect(SCREEN, BLUE, (game.mg_basket_x - 50, HEIGHT - 100, 100, 20), border_radius=6)
        elif game.minigame_type == "speed_click":
            SCREEN.blit(FONT_MED.render("SPAM [SPACEBAR] as fast as you can!", True, WHITE), (WIDTH//2 - 200, HEIGHT//2 - 50))

    elif game.state == STATE_NEXT_SHIFT_PROMPT:
        SCREEN.fill((0, 30, 0))
        SCREEN.blit(FONT_LARGE.render(game.get_txt("prompt_title"), True, GREEN), (WIDTH//2 - 250, 180))
        SCREEN.blit(FONT_MED.render(game.get_txt("prompt_ask"), True, WHITE), (WIDTH//2 - 140, 280))
        SCREEN.blit(FONT_MED.render(game.get_txt("prompt_y"), True, YELLOW), (WIDTH//2 - 230, 350))
        SCREEN.blit(FONT_MED.render(game.get_txt("prompt_n"), True, RED), (WIDTH//2 - 180, 400))

    elif game.state == STATE_EXIT_MSG:
        SCREEN.fill((10, 10, 10))
        SCREEN.blit(FONT_LARGE.render(game.get_txt("exit_thanks"), True, YELLOW), (WIDTH//2 - 220, HEIGHT//2 - 60))
        SCREEN.blit(FONT_MED.render(game.get_txt("exit_press"), True, WHITE), (WIDTH//2 - 200, HEIGHT//2 + 10))

    elif game.state == STATE_GAME_OVER:
        SCREEN.fill((40, 0, 0))
        SCREEN.blit(FONT_LARGE.render("GAME OVER - YOU WERE CAUGHT!", True, RED), (WIDTH//2 - 250, HEIGHT//2))

    pygame.display.flip()
    clock.tick(60)
