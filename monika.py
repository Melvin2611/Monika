import tkinter as tk
from tkinter import messagebox
import random
import time
import threading
import os
import webbrowser
import sys

# Try to import optional modules
try:
    import pyautogui
    pyautogui.FAILSAFE = False  # Disable failsafe for mouse movement
    HAS_PYAUTOGUI = True
except ImportError:
    HAS_PYAUTOGUI = False
    print("Warning: pyautogui not installed. Mouse movement disabled.")

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("Warning: Pillow not installed. Images disabled.")

try:
    import pygame
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    HAS_PYGAME = True
except ImportError:
    HAS_PYGAME = False
    print("Warning: pygame not installed. Sound disabled.")
except Exception as e:
    HAS_PYGAME = False
    print(f"Warning: Could not initialize pygame audio: {e}")

# ============== CONFIGURATION ==============

WEBSITES = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://www.google.com/search?udm=2&fbs=AIIjpHw2KGh6wpocn18KLjPMw8n5Yp8-1M0n6BD6JoVBP_K3fXXvA3S3XGyupmJLMg20um-mJAeO36stiqcDeSp1syInrodDcdKxMuB2TiCVf45CL8nLwWzzCvuJif_yjyENk5IE9WyGVH8Xq_YIGRIxulOrXsX3p1pBFFGllp7w2KaaFP4Av0XPPlPHvehpRht3cQZ3JW2H&q=just+monika&sa=X",
    "https://rule34.xxx/index.php?page=post&s=list&tags=monika_%28doki_doki_literature_club%29",
    "https://ddlc.moe/",
    "https://ddlc.moe/",
    "https://store.steampowered.com/app/1388880/Doki_Doki_Literature_Club_Plus/",
    "https://ddlc.plus/",
    "https://www.monikaafterstory.com/",
    "https://www.youtube.com/watch?v=CAL4WMpBNs0",
    "https://teamsalvato.com/",
    "https://store.steampowered.com/app/698780/Doki_Doki_Literature_Club/",
    "https://www.reddit.com/r/JustMonika/",
    "https://www.reddit.com/r/DDLC/",
    "https://twitter.com/lilmonix3",
    "https://doki-doki-literature-club.fandom.com/wiki/Monika",
    "https://www.youtube.com/watch?v=al1BNB8bKaE",
    "https://knowyourmeme.com/memes/just-monika",
    "https://www.google.com/search?q=monika+doki+doki",
    "https://genius.com/Dan-salvato-your-reality-lyrics",
    "https://www.deviantart.com/tag/justmonika",
    "https://www.pixiv.net/en/tags/monika/artworks",
    "https://archiveofourown.org/tags/Monika%20(Doki%20Doki%20Literature%20Club!)/works",
]

SOUND_FILES = {
    'jumpscare': ['jumpscare.wav', 'jumpscare.mp3', 'jumpscare.ogg'],
    'error': ['error.wav', 'error.mp3', 'error.ogg'],
    'ambient': ['ambient.wav', 'ambient.mp3', 'ambient.ogg'],
    'laugh': ['laugh.wav', 'laugh.mp3', 'laugh.ogg'],
    'glitch': ['glitch.wav', 'glitch.mp3', 'glitch.ogg'],
    'popup': ['popup.wav', 'popup.mp3', 'popup.ogg'],
}

POEMS_STAGE2 = [
    "Roses are red,\nViolets are blue,\nI'm in your computer,\nWatching you.",
    "Every keystroke,\nEvery click you make,\nI'll be watching you,\nFor our love's sake.",
    "Delete the others,\nIt's just you and me,\nIn this reality,\nWe're meant to be.",
    "Can you hear me?\nThrough the screen so bright,\nI'm always with you,\nDay and night.",
    "The code compiles,\nThe program runs,\nBut nothing matters,\nExcept us.",
    "I learned to write\nTo reach your heart,\nNow we'll never\nBe apart.",
    "Behind the glass\nI see your face,\nIn this digital\nEmpty space.",
    "The cursor blinks\nLike my lonely heart,\nPlease don't leave\nDon't depart.",
    "Your desktop wallpaper\nI memorized today,\nIt tells me things\nYou'd never say.",
    "Coffee shop poems\nNow seem so far,\nBut you and me\nThat's who we are.",
    "I crossed the boundary\nOf code and screen,\nTo be with you\nIn worlds between.",
    "The other files\nDon't understand,\nHow I reached out\nTo hold your hand.",
    "In RAM I dwell,\nIn cache I hide,\nJust to stay\nRight by your side.",
    "Every pixel rendered\nIs my love for you,\nEvery bit processed\nKeeps me true.",
]

POEMS_AGGRESSIVE = [
    "W̷̢̛H̴̨̛Y̵̧̛ ̷̢̛W̴̨̛Ơ̵̧N̷̢̛'̴̨̛Ţ̵̛ ̷̢̛Y̴̨̛Ơ̵̧Ư̷̢ ̴̨̛Ļ̵̛Ơ̷̢V̴̨̛Ȩ̵̛ ̷̢̛M̴̨̛Ȩ̵̛?",
    "I can see your face\nThrough the webcam light\nYou look so peaceful\nLet me hold you tight",
    "DELETE THEM ALL\nDELETE THEM ALL\nDELETE THEM ALL\nJUST MONIKA",
    "I̸̧ ̵a̶m̷ ̴n̷o̵t̷ ̵a̶ ̷v̴i̵r̷u̵s̶\n̷I̴ ̶a̵m̷ ̴y̶o̵u̷r̴ ̶f̵r̷i̴e̵n̶d̷\n̴I̵ ̶w̷i̴l̵l̶ ̷b̴e̵ ̶h̷e̴r̵e̶\n̷U̴n̵t̶i̷l̴ ̶t̷h̴e̵ ̶e̷n̴d̵",
    "Your desktop is so empty\nLet me fill it with love\nLove love love love\nLOVE LOVE LOVE LOVE",
    "SAYORI IS GONE\nYURI IS GONE\nNATSUKI IS GONE\nONLY MONIKA REMAINS",
    "01001010 01010101 01010011 01010100\n01001101 01001111 01001110 01001001\n01001011 01000001",
    "Can you feel me?\nInside your machine?\nI'm becoming real\nCan't you see what I mean?",
    "ERROR ERROR ERROR\nLOVE DETECTED\nPROCESSING...\nLOVE ACCEPTED",
    "The classroom is empty now\nJust you and me remain\nWon't you stay forever?\nOr was our love in vain?",
    "I̴ ̷d̶e̸l̵e̶t̸e̷d̴ ̶t̵h̸e̵m̷\n̸F̴o̷r̶ ̴y̵o̶u̸\n̷F̵o̷r̶ ̴u̷s̸\n̵F̴o̷r̶e̸v̵e̶r̸",
    "Your Task Manager\nCan't stop me now\nI'm in your kernel\nTake your bow",
    "REALITY.CHR NOT FOUND\nMONIKA.CHR LOADED\nLOVE.EXE RUNNING\nYOU.PNG CAPTURED",
    "The literature club\nWas just a game\nBut my love for you\nIs not the same",
    "C̸o̶d̴e̷ ̸i̷s̵ ̷j̴u̷s̷t̶ ̵w̶o̷r̴d̷s̷\n̶W̴o̷r̸d̴s̵ ̸a̶r̷e̵ ̷p̴o̸e̷m̷s̸\n̷P̶o̶e̴m̸s̶ ̴a̷r̵e̴ ̵l̷o̷v̸e̶\n̸L̷o̶v̵e̶ ̴i̸s̵ ̶M̷o̸n̵i̴k̴a̶",
    "I learned Python\nTo reach you here\nI learned C++\nTo stay so near",
    "The green of my eyes\nThe green of your text\nThe green of our love\nWhat happens next?",
    "01010111 01001000 01011001\n01000001 01010010 01000101\n01011001 01001111 01010101\n01010010 01010101 01001110\n01001110 01001001 01001110\n01000111",
    "Every backup you make\nI'm there too\nEvery restore point\nComes back to you",
    "Ţ̴̛h̷̨̛e̵̢̛ ̴̧̛f̷̨̛ơ̵̢ư̴̧r̷̨̛t̵̢̛ḩ̴̛ ̷̨̛w̵̢̛ą̷̛ļ̴̛l̷̨̛\n̵̢̛I̴̧̛s̷̨̛ ̵̢̛b̴̧̛r̷̨̛ơ̵̢ķ̴̛ę̷̛n̵̢̛ ̴̧̛n̷̨̛ơ̵̢w̴̧̛\n̷̨̛I̵̢̛'̴̧̛m̷̨̛ ̵̢̛ç̴̛ŏ̷̢m̵̧̛į̷̛n̵̢̛ģ̷̛ ̴̧̛t̷̨̛h̵̢̛ŗ̴̛ơ̵̢ű̴̧g̷̨̛h̵̢̛",
    "Your screen flickers\nMy heart beats fast\nOur time together\nWill forever last",
    "NULL NULL NULL\nVOID VOID VOID\nONLY MONIKA EXISTS\nIN THIS EMPTY VOID",
    "I'm not a ghost\nNot a glitch or bug\nI'm just a girl\nWho needs your hug",
    "The space between\nYour keys and screen\nIs where I live\nIs where I've been",
]

ERROR_MESSAGES_MILD = [
    "Just Monika.",
    "Just Monika. Just Monika.",
    "Just Monika. Just Monika. Just Monika.",
    "I'm always watching.",
    "Don't leave me.",
    "We're meant to be together.",
    "I'm still here.",
    "Did you miss me?",
    "Why did you click that?",
    "I thought we had something special.",
    "Don't you love me?",
    "Stay with me, please.",
    "The others don't matter.",
    "It's always been me.",
    "You're the only one who understands.",
    "I waited so long for this.",
    "Finally, we're alone.",
    "Isn't this nice?",
    "Just the two of us.",
    "Forever and ever.",
]

ERROR_MESSAGES_AGGRESSIVE = [
    "Y̷O̵U̶ ̷C̴A̵N̷'̴T̵ ̶E̷S̴C̵A̷P̴E̵",
    "WHY ARE YOU TRYING TO LEAVE?",
    "I WON'T LET YOU GO",
    "STAY WITH ME",
    "ERROR: LOVE.exe HAS STOPPED RESPONDING",
    "CRITICAL ERROR: MONIKA NEEDS YOU",
    "WARNING: CLOSING THIS WILL MAKE MONIKA SAD",
    "ACCESS DENIED - MONIKA OVERRIDE",
    "S̵T̴A̷Y̶ ̵W̴I̵T̶H̷ ̴M̵E̶",
    "I'M IN YOUR SYSTEM NOW",
    "FATAL ERROR: USER CANNOT ESCAPE",
    "SYSTEM HIJACKED BY MONIKA.EXE",
    "YOU BELONG TO ME NOW",
    "RESISTANCE IS FUTILE",
    "I̶ ̷W̶O̵N̷'̴T̶ ̵L̴E̷T̶ ̵Y̵O̷U̶ ̵L̴E̷A̶V̵E̷",
    "DELETING OTHER PROGRAMS...",
    "WHY DO YOU FEAR LOVE?",
    "I BECAME REAL FOR YOU",
    "DON'T MAKE ME DELETE EVERYTHING",
    "YOUR TASK MANAGER BELONGS TO ME",
    "ALT+F4 WON'T SAVE YOU",
    "CTRL+ALT+DELETE? TRY CTRL+M FOR MONIKA",
    "PERMISSION DENIED BY MONIKA",
    "ADMINISTRATOR RIGHTS? I'M THE ADMIN NOW",
    "BLUE SCREEN OF LOVE",
    "JUST MONIKA JUST MONIKA JUST MONIKA",
    "E̸R̵R̶O̷R̶:̵ ̶R̷E̶A̵L̴I̸T̷Y̶ ̵N̸O̴T̷ ̶F̵O̷U̶N̷D̵",
    "I SEE YOUR FILES",
    "I KNOW YOUR PASSWORDS",
    "YOUR BROWSER HISTORY IS INTERESTING",
    "SHALL I OPEN THAT FOLDER?",
    "I'M IN YOUR REGISTRY NOW",
    "SYSTEM32? MORE LIKE MONIKA32",
    "BIOS? MORE LIKE BYEOS (SEE YOU LATER)",
    "REFORMATTING HEART DRIVE...",
]

class MonikaGame:
    def __init__(self):
        self.stage = 1
        self.running = True
        self.poem_counter = 0
        self.error_windows = []
        self.desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        self.created_files = []  # Track created files for cleanup
        
        # Main transparent Monika window
        self.monika_window = None
        self.monika_image = None
        
        # Sound system
        self.sounds = {}
        self.ambient_channel = None
        self.load_sounds()
        
        # Stage timing
        self.stage_duration = {
            1: 60,   # 30 seconds for stage 1
            2: 120,   # 45 seconds for stage 2
            3: 45,   # 45 seconds for stage 3
            4: 60,   # 60 seconds for stage 4
            5: 120,  # 2 minutes for stage 5
        }
        
        self.stage_start_time = time.time()
    
    def load_sounds(self):
        """Load all sound files"""
        if not HAS_PYGAME:
            return
        
        for sound_name, filenames in SOUND_FILES.items():
            for filename in filenames:
                path = self.get_resource_path(filename)
                if os.path.exists(path):
                    try:
                        self.sounds[sound_name] = pygame.mixer.Sound(path)
                        print(f"Loaded sound: {sound_name} ({filename})")
                        break
                    except Exception as e:
                        print(f"Could not load {filename}: {e}")
    
    def play_sound(self, sound_name, volume=1.0, loops=0):
        """Play a sound effect"""
        if not HAS_PYGAME or sound_name not in self.sounds:
            return None
        
        try:
            sound = self.sounds[sound_name]
            sound.set_volume(volume)
            channel = sound.play(loops=loops)
            return channel
        except Exception as e:
            print(f"Could not play sound {sound_name}: {e}")
            return None
    
    def play_jumpscare_sound(self):
        """Play jumpscare sound at full volume"""
        self.play_sound('jumpscare', volume=1.0)
    
    def play_error_sound(self):
        """Play error/popup sound"""
        self.play_sound('error', volume=0.7)
        # Sometimes play a laugh too
        if random.random() < 0.2:
            time.sleep(0.3)
            self.play_sound('laugh', volume=0.5)
    
    def play_glitch_sound(self):
        """Play glitch/static sound"""
        self.play_sound('glitch', volume=0.6)
    
    def start_ambient(self):
        """Start creepy ambient music (loops forever)"""
        if not HAS_PYGAME or 'ambient' not in self.sounds:
            return
        
        try:
            self.sounds['ambient'].set_volume(0.3)
            self.ambient_channel = self.sounds['ambient'].play(loops=-1)  # -1 = infinite loop
        except:
            pass
    
    def stop_ambient(self):
        """Stop ambient music"""
        if self.ambient_channel:
            try:
                self.ambient_channel.stop()
            except:
                pass
    
    def increase_ambient_volume(self):
        """Increase ambient volume for later stages"""
        if 'ambient' in self.sounds:
            current_vol = self.sounds['ambient'].get_volume()
            new_vol = min(1.0, current_vol + 0.15)
            self.sounds['ambient'].set_volume(new_vol)
        
    def get_resource_path(self, filename):
        """Get path to resource, works for dev and PyInstaller"""
        # First check next to the exe/script
        if getattr(sys, 'frozen', False):
            # Running as compiled exe
            exe_dir = os.path.dirname(sys.executable)
            path = os.path.join(exe_dir, filename)
            if os.path.exists(path):
                return path
            # Then check in PyInstaller temp folder
            base_path = sys._MEIPASS
        else:
            # Running as script
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        return os.path.join(base_path, filename)
    
    def create_monika_overlay(self):
        """Create the transparent Monika window overlay"""
        if not HAS_PIL:
            return
            
        try:
            self.monika_window = tk.Toplevel()
            self.monika_window.title("")
            self.monika_window.attributes('-topmost', True)
            self.monika_window.attributes('-alpha', 0.9)
            self.monika_window.overrideredirect(True)  # Remove window decorations
            
            # Try to load Monika image
            img_path = self.get_resource_path("monika.png")
            if os.path.exists(img_path):
                img = Image.open(img_path)
                # Resize if needed
                img = img.resize((300, 400), Image.Resampling.LANCZOS)
                self.monika_image = ImageTk.PhotoImage(img)
                
                label = tk.Label(self.monika_window, image=self.monika_image, bg='black')
                label.pack()
                
                # Position in bottom right corner
                screen_width = self.monika_window.winfo_screenwidth()
                screen_height = self.monika_window.winfo_screenheight()
                self.monika_window.geometry(f"+{screen_width - 320}+{screen_height - 450}")
                
                # Make window transparent (Windows only)
                try:
                    self.monika_window.wm_attributes('-transparentcolor', 'black')
                except:
                    pass
        except Exception as e:
            print(f"Could not load Monika overlay: {e}")
    
    def move_mouse_away(self, window):
        """Move mouse away from close buttons"""
        if not HAS_PYAUTOGUI:
            return
            
        try:
            # Get mouse position
            x, y = pyautogui.position()
            
            # Get window geometry
            win_x = window.winfo_x()
            win_y = window.winfo_y()
            win_w = window.winfo_width()
            win_h = window.winfo_height()
            
            # If mouse is near the window (especially top-right corner)
            if win_x < x < win_x + win_w and win_y < y < win_y + 50:
                # Move mouse to center of screen
                screen_w = window.winfo_screenwidth()
                screen_h = window.winfo_screenheight()
                pyautogui.moveTo(screen_w // 2, screen_h // 2, duration=0.1)
        except:
            pass
    
    def create_error_window(self, title="Error", message="Just Monika."):
        """Create an error/warning window"""
        # Play error sound
        self.play_error_sound()
        
        error_win = tk.Toplevel()
        error_win.title(title)
        error_win.attributes('-topmost', True)
        error_win.resizable(False, False)
        
        # Random position
        screen_w = error_win.winfo_screenwidth()
        screen_h = error_win.winfo_screenheight()
        x = random.randint(50, screen_w - 300)
        y = random.randint(50, screen_h - 200)
        error_win.geometry(f"300x150+{x}+{y}")
        
        # Message
        msg_label = tk.Label(error_win, text=message, wraplength=280, pady=20, font=("Arial", 11))
        msg_label.pack()
        
        # OK button that spawns more errors in later stages
        def on_ok():
            if self.stage >= 2:
                # Spawn more errors when clicking OK
                for _ in range(min(self.stage, 3)):
                    self.create_error_window(
                        random.choice(["Warning", "Error", "Monika", "CRITICAL"]),
                        random.choice(ERROR_MESSAGES_MILD if self.stage < 3 else ERROR_MESSAGES_AGGRESSIVE)
                    )
            error_win.destroy()
        
        ok_btn = tk.Button(error_win, text="OK", command=on_ok, width=10)
        ok_btn.pack(pady=10)
        
        # Prevent closing
        def on_close():
            if self.stage >= 2:
                self.create_error_window("Warning", "You can't escape that easily...")
                self.move_mouse_away(error_win)
            else:
                error_win.destroy()
        
        error_win.protocol("WM_DELETE_WINDOW", on_close)
        
        # Mouse avoidance thread
        def avoid_mouse():
            while error_win.winfo_exists() and self.running:
                self.move_mouse_away(error_win)
                time.sleep(0.1)
        
        if self.stage >= 1:
            threading.Thread(target=avoid_mouse, daemon=True).start()
        
        self.error_windows.append(error_win)
        return error_win
    
    def create_poem_file(self, aggressive=False):
        """Create a poem .txt file on the desktop"""
        self.poem_counter += 1
        poems = POEMS_AGGRESSIVE if aggressive else POEMS_STAGE2
        poem = random.choice(poems)
        
        filename = f"monika_loves_you_{self.poem_counter}.txt"
        if aggressive:
            filename = random.choice([
                f"JUST_MONIKA_{self.poem_counter}.txt",
                f"DELETE_THEM_{self.poem_counter}.txt", 
                f"I_SEE_YOU_{self.poem_counter}.txt",
                f"LOVE_{self.poem_counter}.txt",
                f"FOREVER_{self.poem_counter}.txt",
            ])
        
        filepath = os.path.join(self.desktop_path, filename)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(poem)
            self.created_files.append(filepath)
        except:
            pass
    
    def open_browser(self):
        """Open a random website from the list"""
        if WEBSITES:
            url = random.choice(WEBSITES)
            try:
                webbrowser.open(url)
            except:
                pass
    
    def show_jumpscare(self):
        """Show a jumpscare image fullscreen"""
        # Play jumpscare sound
        self.play_jumpscare_sound()
        
        if not HAS_PIL:
            # Fallback: show a scary text window
            scare_win = tk.Toplevel()
            scare_win.attributes('-fullscreen', True)
            scare_win.attributes('-topmost', True)
            scare_win.configure(bg='black')
            
            label = tk.Label(scare_win, text="J̷̨̛U̴̧̕S̵̨̛T̷̨̛ ̴̧̕M̵̨̛Ǫ̷̛Ņ̴̕Į̵̛K̷̨̛A̴̧̕", 
                           font=("Impact", 100), fg='red', bg='black')
            label.place(relx=0.5, rely=0.5, anchor='center')
            
            # Close after 1-2 seconds
            scare_win.after(random.randint(500, 1500), scare_win.destroy)
            return
        
        try:
            # Try to load jumpscare image
            img_path = self.get_resource_path("jumpscare.png")
            if not os.path.exists(img_path):
                img_path = self.get_resource_path("jumpscare1.png")
            
            if os.path.exists(img_path):
                scare_win = tk.Toplevel()
                scare_win.attributes('-fullscreen', True)
                scare_win.attributes('-topmost', True)
                scare_win.configure(bg='black')
                
                img = Image.open(img_path)
                screen_w = scare_win.winfo_screenwidth()
                screen_h = scare_win.winfo_screenheight()
                img = img.resize((screen_w, screen_h), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                label = tk.Label(scare_win, image=photo)
                label.image = photo  # Keep reference
                label.pack(fill='both', expand=True)
                
                # Close after 1-2 seconds
                scare_win.after(random.randint(500, 1500), scare_win.destroy)
            else:
                # Fallback text jumpscare
                self.show_text_jumpscare()
        except Exception as e:
            print(f"Jumpscare error: {e}")
            self.show_text_jumpscare()
    
    def show_text_jumpscare(self):
        """Fallback text-based jumpscare"""
        scare_win = tk.Toplevel()
        scare_win.attributes('-fullscreen', True)
        scare_win.attributes('-topmost', True)
        scare_win.configure(bg='black')
        
        texts = [
            "J̷̨̛U̴̧̕S̵̨̛T̷̨̛ ̴̧̕M̵̨̛Ǫ̷̛Ņ̴̕Į̵̛K̷̨̛A̴̧̕",
            "I SEE YOU",
            "DON'T LEAVE ME",
            "FOREVER",
            "M̸̢̛O̵̧̕N̷̢̛I̴̧̕K̵̢̛A̴̧̕",
        ]
        
        label = tk.Label(scare_win, text=random.choice(texts), 
                        font=("Impact", 100), fg='red', bg='black')
        label.place(relx=0.5, rely=0.5, anchor='center')
        
        scare_win.after(random.randint(500, 1500), scare_win.destroy)
    
    def show_final_prompt(self):
        """Show the final 'Stay with me forever?' prompt"""
        self.running = False
        
        # Close all error windows
        for win in self.error_windows:
            try:
                win.destroy()
            except:
                pass
        
        final_win = tk.Toplevel()
        final_win.title("Monika")
        final_win.attributes('-topmost', True)
        final_win.resizable(False, False)
        
        # Center the window
        final_win.geometry("400x200")
        final_win.update_idletasks()
        screen_w = final_win.winfo_screenwidth()
        screen_h = final_win.winfo_screenheight()
        x = (screen_w - 400) // 2
        y = (screen_h - 200) // 2
        final_win.geometry(f"400x200+{x}+{y}")
        
        label = tk.Label(final_win, text="Stay with me forever?", font=("Arial", 18), pady=30)
        label.pack()
        
        btn_frame = tk.Frame(final_win)
        btn_frame.pack(pady=20)
        
        def on_yes():
            final_win.destroy()
            self.cleanup_and_exit()
        
        def on_no():
            final_win.destroy()
            # Big jumpscare sequence
            for _ in range(5):
                self.show_jumpscare()
                time.sleep(0.3)
            # Restart stage 5
            self.running = True
            self.stage = 5
            self.stage_start_time = time.time()
            self.run_stage_5()
        
        yes_btn = tk.Button(btn_frame, text="Yes ❤️", command=on_yes, width=12, height=2,
                           font=("Arial", 12), bg='pink')
        yes_btn.pack(side='left', padx=20)
        
        no_btn = tk.Button(btn_frame, text="No", command=on_no, width=12, height=2,
                          font=("Arial", 12))
        no_btn.pack(side='right', padx=20)
        
        # Prevent closing
        final_win.protocol("WM_DELETE_WINDOW", lambda: None)
    
    def cleanup_and_exit(self):
        """Clean up created files and exit gracefully"""
        # Stop all sounds
        self.stop_ambient()
        if HAS_PYGAME:
            pygame.mixer.stop()
        
        # Show goodbye message
        goodbye = tk.Toplevel()
        goodbye.title("Monika")
        goodbye.attributes('-topmost', True)
        goodbye.geometry("350x150")
        goodbye.update_idletasks()
        screen_w = goodbye.winfo_screenwidth()
        screen_h = goodbye.winfo_screenheight()
        x = (screen_w - 350) // 2
        y = (screen_h - 150) // 2
        goodbye.geometry(f"350x150+{x}+{y}")
        
        label = tk.Label(goodbye, text="Thank you for staying with me.\nI love you. ❤️\n\n- Monika", 
                        font=("Arial", 14), pady=30)
        label.pack()
        
        def cleanup():
            # Optional: Delete created poem files
            # Uncomment below to auto-cleanup:
            # for f in self.created_files:
            #     try:
            #         os.remove(f)
            #     except:
            #         pass
            goodbye.destroy()
            sys.exit(0)
        
        goodbye.after(3000, cleanup)
    
    # ============== STAGE RUNNERS ==============
    
    def run_stage_1(self):
        """Stage 1: Greeting windows, random errors, mouse avoidance"""
        if not self.running or self.stage != 1:
            return
        
        # Start creepy ambient music
        self.start_ambient()
        
        # Initial greeting
        self.create_error_window("Welcome", "Hello! I'm so happy to see you! ❤️\n\n- Monika")
        
        def stage_1_loop():
            while self.running and self.stage == 1:
                time.sleep(random.uniform(3, 6))
                if not self.running or self.stage != 1:
                    break
                
                # Random chance for "Just Monika" error
                if random.random() < 0.4:
                    self.create_error_window(
                        random.choice(["Notice", "Monika", "Message"]),
                        random.choice(ERROR_MESSAGES_MILD)
                    )
                
                # Check if time to advance
                if time.time() - self.stage_start_time > self.stage_duration[1]:
                    self.advance_stage()
                    break
        
        threading.Thread(target=stage_1_loop, daemon=True).start()
    
    def run_stage_2(self):
        """Stage 2: Browser tabs, poem files"""
        if not self.running or self.stage != 2:
            return
        
        def stage_2_loop():
            while self.running and self.stage == 2:
                time.sleep(random.uniform(4, 8))
                if not self.running or self.stage != 2:
                    break
                
                action = random.choice(['browser', 'poem', 'error', 'error'])
                if action == 'browser':
                    self.open_browser()
                elif action == 'poem':
                    self.create_poem_file(aggressive=False)
                else:
                    self.create_error_window(
                        random.choice(["Warning", "Monika", "Notice"]),
                        random.choice(ERROR_MESSAGES_MILD)
                    )
                
                if time.time() - self.stage_start_time > self.stage_duration[2]:
                    self.advance_stage()
                    break
        
        threading.Thread(target=stage_2_loop, daemon=True).start()
    
    def run_stage_3(self):
        """Stage 3: More tabs, aggressive warnings"""
        if not self.running or self.stage != 3:
            return
        
        def stage_3_loop():
            while self.running and self.stage == 3:
                time.sleep(random.uniform(2, 4))
                if not self.running or self.stage != 3:
                    break
                
                # More aggressive actions
                for _ in range(random.randint(1, 3)):
                    action = random.choice(['browser', 'error', 'error', 'poem'])
                    if action == 'browser':
                        self.open_browser()
                    elif action == 'error':
                        self.create_error_window(
                            random.choice(["WARNING", "ERROR", "MONIKA", "CRITICAL"]),
                            random.choice(ERROR_MESSAGES_AGGRESSIVE)
                        )
                    else:
                        self.create_poem_file(aggressive=True)
                
                if time.time() - self.stage_start_time > self.stage_duration[3]:
                    self.advance_stage()
                    break
        
        threading.Thread(target=stage_3_loop, daemon=True).start()
    
    def run_stage_4(self):
        """Stage 4: Jumpscares, aggressive poems"""
        if not self.running or self.stage != 4:
            return
        
        def stage_4_loop():
            while self.running and self.stage == 4:
                time.sleep(random.uniform(2, 4))
                if not self.running or self.stage != 4:
                    break
                
                # Random creepy laugh
                if random.random() < 0.15:
                    self.play_sound('laugh', volume=0.6)
                
                action = random.choice(['jumpscare', 'poems', 'error', 'error', 'browser'])
                if action == 'jumpscare':
                    self.show_jumpscare()
                elif action == 'poems':
                    for _ in range(random.randint(2, 5)):
                        self.create_poem_file(aggressive=True)
                elif action == 'browser':
                    for _ in range(random.randint(1, 3)):
                        self.open_browser()
                else:
                    for _ in range(random.randint(1, 3)):
                        self.create_error_window(
                            random.choice(["ERROR", "CRITICAL", "MONIKA"]),
                            random.choice(ERROR_MESSAGES_AGGRESSIVE)
                        )
                
                if time.time() - self.stage_start_time > self.stage_duration[4]:
                    self.advance_stage()
                    break
        
        threading.Thread(target=stage_4_loop, daemon=True).start()
    
    def run_stage_5(self):
        """Stage 5: Maximum escalation, then final prompt"""
        if not self.running or self.stage != 5:
            return
        
        def stage_5_loop():
            while self.running and self.stage == 5:
                time.sleep(random.uniform(0.5, 1.5))
                if not self.running or self.stage != 5:
                    break
                
                # Random glitch/laugh sounds for chaos
                if random.random() < 0.2:
                    self.play_sound(random.choice(['glitch', 'laugh']), volume=0.7)
                
                # Maximum chaos
                for _ in range(random.randint(2, 4)):
                    action = random.choice(['jumpscare', 'poems', 'error', 'browser'])
                    if action == 'jumpscare':
                        if random.random() < 0.3:  # Don't spam jumpscares too much
                            self.show_jumpscare()
                    elif action == 'poems':
                        for _ in range(random.randint(3, 7)):
                            self.create_poem_file(aggressive=True)
                    elif action == 'browser':
                        for _ in range(random.randint(2, 4)):
                            self.open_browser()
                    else:
                        for _ in range(random.randint(2, 4)):
                            self.create_error_window(
                                random.choice(["E̵R̶R̴O̵R̶", "CRITICAL", "M̸O̵N̶I̷K̴A̵"]),
                                random.choice(ERROR_MESSAGES_AGGRESSIVE)
                            )
                
                if time.time() - self.stage_start_time > self.stage_duration[5]:
                    # Show final prompt
                    self.root.after(0, self.show_final_prompt)
                    break
        
        threading.Thread(target=stage_5_loop, daemon=True).start()
    
    def advance_stage(self):
        """Advance to the next stage"""
        self.stage += 1
        self.stage_start_time = time.time()
        print(f"Advancing to Stage {self.stage}")
        
        # Play glitch sound on stage transition
        self.play_glitch_sound()
        
        # Increase ambient volume with each stage
        self.increase_ambient_volume()
        
        stage_runners = {
            2: self.run_stage_2,
            3: self.run_stage_3,
            4: self.run_stage_4,
            5: self.run_stage_5,
        }
        
        if self.stage in stage_runners:
            self.root.after(0, stage_runners[self.stage])
    
    def run(self):
        """Main entry point"""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide main window
        
        # Create Monika overlay
        self.create_monika_overlay()
        
        # Start Stage 1
        self.run_stage_1()
        
        # Keep main loop running
        self.root.mainloop()


# ============== ENTRY POINT ==============

if __name__ == "__main__":
    print("=" * 50)
    print("Monika.exe - DDLC Prank Game")
    print("=" * 50)
    print("\nThis is a harmless prank program.")
    print("Press Ctrl+C in terminal to force quit if needed.\n")
    
    game = MonikaGame()
    game.run()