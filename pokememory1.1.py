# Importierung der nötigen Module
import pygame, cv2, random, os


# Definierung der Tile Klasse
class Tile(pygame.sprite.Sprite):

    # Initialisierung der Tile-Klasse
    def __init__(self, filename, x, y):
        super().__init__()

        # Erhalte den Namen der Bilddatei ohne Dateierweiterung und Punkt
        self.name = filename.split('.')[0]

        # Lade das Bild für die Vorder- und Rückseite der Tile
        self.original_image = pygame.image.load('img/pokemon/' + filename)
        self.back_image = pygame.image.load('img/backimage/star.png')

        # Setze die Bild- und Rechteckattribute für die Kachel
        self.image = self.back_image
        self.rect = self.image.get_rect(topleft=(x, y))

        # Setze den Zustand der Tile auf versteckt
        self.shown = False

    # Mit dieser Funktion aktualisiert man das Bild der Tile, um die Vorder- oder Rückseite anzuzeigen
    def update(self):
        self.image = self.original_image if self.shown else self.back_image

    # Setze den Zustand der Tile auf angezeigt
    def show(self):
        self.shown = True

    # Setze den Zustand der Tile auf versteckt
    def hide(self):
        self.shown = False


# Definierung der Game Klasse
class Game:

    # Initialisierung der Game-Klasse
    def __init__(self):
        # Setze das Anfangsniveau des Spiels und den Abschluss des Levels
        self.level = 1
        self.level_complete = False
        # Setze den Zähler für Versuche und die Höchstpunktzahl
        self.try_count = 0
        self.best_score = 68

        # Erhalte eine Liste(Array) aller Pokemon-Bilddateinamen, die in dem Ordner Pokemon gespeichert sind.
        self.all_pokemon = [f for f in os.listdir('img/pokemon') if os.path.join('img/pokemon')]

        # Setze einige Layout-Parameter für das Spielbrett
        self.img_width, self.img_height = (128, 128)
        self.padding = 20
        self.margin_top = 160
        self.cols = 4
        self.rows = 2
        self.width = 1280

        # Erstelle eine Gruppe von Sprites, um die Kacheln zu halten mit Hilfe der Pygame Funktion sprite.Group()
        self.tiles_group = pygame.sprite.Group()

        # Setze einige Spielparameter für das Flippen von Kacheln und das Timing, in clicked_tiles werden die namen der
        # Tiles temporär gespeichert
        self.clicked_tiles = []
        self.frame_count = 0
        self.block_game = False

        # Generiere die Level
        self.generate_level(self.level)

        # Initialisierung des Hintergrundvideos
        self.is_video_playing = True
        self.get_video()

        # Initialisierung der Musik
        self.is_music_playing = True
        self.sound_on = pygame.image.load('img/volume.png')
        self.sound_off = pygame.image.load('img/mute.png')
        self.music_toggle = self.sound_on
        self.music_toggle_rect = self.music_toggle.get_rect(topright=(WINDOW_WIDTH - 10, 10))

        # Lade die Spielmusik und Soundeffekte der Pokemon
        pygame.mixer.music.load('audio/Night_Walk.mp3')
        self.abra_sound = pygame.mixer.Sound('audio/abra.mp3')
        self.zubat_sound = pygame.mixer.Sound('audio/zubat.mp3')
        self.venonat_sound = pygame.mixer.Sound('audio/venonat.mp3')
        self.squirtle_sound = pygame.mixer.Sound('audio/squirtle.mp3')
        self.snorlax_sound = pygame.mixer.Sound('audio/snorlax.mp3')
        self.rattata_sound = pygame.mixer.Sound('audio/rattata.mp3')
        self.pikachu_sound = pygame.mixer.Sound('audio/pikachu-starter.mp3')
        self.pidgey_sound = pygame.mixer.Sound('audio/pidgey.mp3')
        self.meowth_sound = pygame.mixer.Sound('audio/meowth.mp3')
        self.mankey_sound = pygame.mixer.Sound('audio/mankey.mp3')
        self.eevee_sound = pygame.mixer.Sound('audio/eevee.ogg')
        self.dratini_sound = pygame.mixer.Sound('audio/dratini.mp3')
        self.charmander_sound = pygame.mixer.Sound('audio/charmander.mp3')
        self.bulbasaur_sound = pygame.mixer.Sound('audio/bulbasaur.mp3')
        self.bellsprout_sound = pygame.mixer.Sound('audio/bellsprout.mp3')
        self.caterpie_sound = pygame.mixer.Sound('audio/caterpie.mp3')
        self.psyduck_sound = pygame.mixer.Sound('audio/psyduck.mp3')
        self.jigglypuff_sound = pygame.mixer.Sound('audio/jigglypuff.mp3')
        self.victory_sound = pygame.mixer.Sound('audio/victory.mp3')
        self.victory_end_sound = pygame.mixer.Sound('audio/victory_end.mp3')

        # Reduziere die Lautsrtärke der Sounds um 20%
        for sound in [self.victory_end_sound, self.victory_sound, self.jigglypuff_sound, self.psyduck_sound, self.caterpie_sound, self.bellsprout_sound, self.bulbasaur_sound, self.charmander_sound, self.dratini_sound, self.eevee_sound, self.mankey_sound, self.meowth_sound, self.pidgey_sound, self.pikachu_sound, self.rattata_sound, self.snorlax_sound, self.squirtle_sound, self.venonat_sound, self.zubat_sound, self.abra_sound]:
            sound.set_volume(0.2)

        # Reduziere die Lautstärke der Hintergrundmusik um 30 %
        pygame.mixer.music.set_volume(.3)
        # Setze das Endevent, um die Musik zu stoppen, wenn das Spiel beendet wird.
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        # Spiele die Hintergrundmusik ab.
        pygame.mixer.music.play()

    def update(self, event_list):
        """
        Die Funktion update() aktualisiert das Spiel durch Ausführen mehrerer Schritte. Zuerst wird überprüft,
        ob ein Video abgespielt wird und in diesem Fall werden Frames vom Videoaufnahmeobjekt gelesen und das Bild aktualisiert.
        Dann werden die Benutzereingabe-Events verarbeitet und die draw()-Funktion aufgerufen. Schließlich wird überprüft,
        ob das Level abgeschlossen ist, indem die check_level_complete()-Funktion aufgerufen wird und das entsprechende Verhalten ausgeführt wird.
        """
        # Wenn ein Video abgespielt wird, lies Frames vom Videoaufnahmeobjekt und aktualisiere das Bild.
        if self.is_video_playing:
            self.success, self.img = self.cap.read()

        # Behandle die Benutzereingabe-Events.
        self.user_input(event_list)

        # Aufruf der draw() Funktion in der update() Funktion
        self.draw()

        # Überprüfe, ob das Level abgeschlossen ist.
        self.check_level_complete(event_list)

    def tile_sound(self, tile):
        if tile.name == 'abra':
            self.abra_sound.play()
        if tile.name == 'zubat':
            self.zubat_sound.play()
        if tile.name == 'venonat':
            self.venonat_sound.play()
        if tile.name == 'squirtle':
            self.squirtle_sound.play()
        if tile.name == 'snorlax':
            self.snorlax_sound.play()
        if tile.name == 'rattata':
            self.rattata_sound.play()
        if tile.name == 'pikachu':
            self.pikachu_sound.play()
        if tile.name == 'pidgey':
            self.pidgey_sound.play()
        if tile.name == 'eevee':
            self.eevee_sound.play()
        if tile.name == 'dratini':
            self.dratini_sound.play()
        if tile.name == 'charmander':
            self.charmander_sound.play()
        if tile.name == 'bullbasaur':
            self.bulbasaur_sound.play()
        if tile.name == 'bellsprout':
            self.bellsprout_sound.play()
        if tile.name == 'caterpie':
            self.caterpie_sound.play()
        if tile.name == 'psyduck':
            self.psyduck_sound.play()
        if tile.name == 'jigglypuff':
            self.jigglypuff_sound.play()
        if tile.name == 'mankey':
            self.mankey_sound.play()
        if tile.name == 'meowth':
            self.meowth_sound.play()

    def compare_tiles(self):
        """
        Nach dem umdrehen Kacheln vergleichen
        bei übereinstimmung
        => angeklickte Kacheln leeren

        => prüfen ob Level beendet
        => bei beendigung sound wechseln
        :return:
        """
        if len(self.clicked_tiles) == 2:
            self.try_count += 1
            if self.clicked_tiles[0].name != self.clicked_tiles[1].name:
                self.block_game = True

            # Wenn die Kacheln übereinstimmen
            else:
                # entferne sie aus der Liste der angeklickten Kacheln
                self.clicked_tiles = []

                # Prüfen ob Level beendet. Sobald eine Kachel nicht umgedreht ist wird level_complete auf FALSE gesetzt
                for tile in self.tiles_group:
                    if tile.shown:
                        self.level_complete = True
                    else:
                        self.level_complete = False
                        break

                # wenn level_complete => sound spielen
                if self.level_complete and not self.level == 5:
                    self.victory_sound.play()
                    pygame.mixer.music.pause()
                if self.level_complete and self.level == 5:
                    self.victory_end_sound.play()
                    pygame.mixer.music.pause()
                    self.get_winvideo()


    def check_level_complete(self, event_list):
        """
        Die Funktion check_level_complete wird aufgerufen, um zu überprüfen, ob ein Level abgeschlossen wurde.
        Zunächst wird überprüft, ob das Spiel blockiert ist. Wenn es nicht blockiert ist, werden Benutzereingabe-Events behandelt,
        um zu bestimmen, ob eine Kachel angeklickt wurde. Wenn eine Kachel angeklickt wurde,
        wird sie in eine Liste der angeklickten Kacheln aufgenommen und der zugehörige Soundeffekt wird abgespielt.
        Wenn zwei Kacheln angeklickt wurden, wird geprüft, ob sie übereinstimmen. Wenn sie nicht übereinstimmen, wird das Spiel blockiert.
        Wenn sie übereinstimmen, werden sie aus der Liste der angeklickten Kacheln entfernt und es wird überprüft, ob das Level abgeschlossen ist.

        Wenn das Level abgeschlossen ist und es das fünfte Level ist, wird überprüft, ob die Anzahl der Klicks des Spielers niedriger ist als der Highscore.
        Wenn das Spiel blockiert ist, erhöht die Funktion die Frame-Zählung, bis sie 40 erreicht. Wenn die Frame-Zählung 40 erreicht, wird das Spiel nicht mehr blockiert,
        alle angeklickten Kacheln werden ausgeblendet und die Liste der angeklickten Kacheln wird geleert.
        """
        # Wenn das Spiel nicht blockiert ist, überprüfe Benutzereingabe-Events, um zu bestimmen, ob ein Kachel angeklickt wurde.
        if not self.block_game:
            for event in event_list:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Gehe durch die Kacheln in der Kachelgruppe und überprüfe, ob eine Kachel angeklickt wurde.
                    for tile in self.tiles_group:
                        if tile.rect.collidepoint(event.pos) and tile not in self.clicked_tiles and not tile.shown:
                            # Wenn eine Kachel angeklickt wurde, füge sie der Liste der angeklickten Kacheln hinzu, zeige sie an und spiele ihren zugehörigen Soundeffekt ab.
                            self.clicked_tiles.append(tile)
                            tile.show()
                            self.tile_sound(tile)
                            # Wenn zwei Kacheln angeklickt wurden, vergleiche und prüfe ob alle Kacheln umgedreht wurden
                            self.compare_tiles()
            if self.level_complete and self.level == 5:
                # Prüfe, ob die Anzahl der Klicks des Spielers niedriger ist als der Highscore.
                if self.try_count < self.best_score:
                    self.best_score = self.try_count
        else:
            # Wenn das Spiel blockiert ist, erhöhe die Frame-Zählung, bis sie 40 erreicht.
            self.frame_count += 1
            if self.frame_count == 30:
                self.frame_count = 0
                self.block_game = False
                # Verberge alle angeklickten Kacheln und leere die Liste der angeklickten Kacheln.
                for tile in self.clicked_tiles:
                    tile.hide()
                self.clicked_tiles = []


    def generate_level(self, level):
        """
        Die Funktion generate_level erstellt ein neues Level, indem sie eine zufällige Gruppe von Pokémon basierend auf dem aktuellen Level auswählt,
        die Anzahl der Zeilen und Spalten auf Basis des aktuellen Levels setzt und das Kachelset mit den ausgewählten Pokémon generiert.
        Das level_complete-Flag wird auf False gesetzt, um anzuzeigen, dass das Level noch nicht abgeschlossen ist.
        """
        # Wähle eine zufällige Gruppe von Pokemon basierend auf dem aktuellen Level aus.
        self.pokemon = self.select_random_pokemon(self.level)

        # Setze das level_complete-Flag auf False.
        self.level_complete = False

        # Setze die Anzahl der Zeilen und Spalten basierend auf dem aktuellen Level.
        self.rows = self.level + 1
        self.cols = 4

        # Generiere das Kachelset mit den ausgewählten Pokemon.
        self.generate_tileset(self.pokemon)

    def generate_tileset(self, pokemon):
        """
        Die Funktion generate_tileset generiert ein Kachelset (eine Gruppe von Kacheln), um das Spiel zu spielen.
        Es nimmt eine Liste von Pokémon als Eingabe und generiert für jedes Pokemon in der Liste eine Kachel.
        Die Anzahl der Zeilen und Spalten im Kachelset wird angepasst, um ein quadratisches Layout zu gewährleisten.
        Die Größe und die Position jeder Kachel werden berechnet und ein neues Kachelobjekt wird für jedes Pokemon in der Liste erstellt und der Kachelgruppe hinzugefügt.
        Die Funktion leert auch die Kachelgruppe, um Platz für die neue Gruppe zu schaffen.
        """
        # Passe die Anzahl der Zeilen und Spalten an, um das quadratische Kachelset-Layout zu gewährleisten.
        self.cols = self.rows = self.cols if self.cols >= self.rows else self.rows

        # Berechne die Breite des Kachelsets und die Ränder auf beiden Seiten.
        TILES_WIDTH = (self.img_width * self.cols + self.padding * 3)
        LEFT_MARGIN = RIGHT_MARGIN = (self.width - TILES_WIDTH) // 2

        # Leere die Kachelgruppe, um Platz für die neue Gruppe zu schaffen.
        self.tiles_group.empty()

        # Generiere neue Kachelobjekte und füge sie der Gruppe hinzu.
        for i in range(len(pokemon)):
            x = LEFT_MARGIN + ((self.img_width + self.padding) * (i % self.cols))
            y = self.margin_top + (i // self.rows * (self.img_height + self.padding))
            tile = Tile(pokemon[i], x, y)
            self.tiles_group.add(tile)

    def select_random_pokemon(self, level):
        """
        Die Funktion select_random_pokemon wählt eine zufällige Stichprobe von Pokemon für das aktuelle Level aus,
        indem sie level + level + 2 zufällige Pokemon aus einer Liste von verfügbaren Pokemon auswählt.
        Dann erstellt sie eine Kopie der Liste und fügt diese Liste der ausgewählten Pokemon hinzu, um Paare von Pokemon zu erstellen.
        Schließlich mischt sie die Liste, um die Reihenfolge zu randomisieren, und gibt sie zurück.
        """
        # Wählt eine zufällige Stichprobe von Pokémon für das aktuelle Level aus
        pokemon = random.sample(self.all_pokemon, (self.level + self.level + 2))
        # Erstellt eine Kopie der Liste und erweitert sie, um passende Paare zu erstellen
        pokemon_copy = pokemon.copy()
        pokemon.extend(pokemon_copy)
        # Mischt die Liste, um die Reihenfolge zu randomisieren
        random.shuffle(pokemon)
        return pokemon

    def user_input(self, event_list):
        """
        Die Funktion user_input überprüft die Benutzereingabeereignisse und aktualisiert den Spielstand entsprechend.
        Es werden zwei Mausklick-Events abgefangen, um die Musik und das Video ein- bzw. auszuschalten und die zugehörigen Symbole entsprechend zu aktualisieren.
        Wenn das aktuelle Level abgeschlossen ist und die Leertaste gedrückt wird, geht das Spiel zum nächsten Level über.
        Wenn das aktuelle Level höher als sechs wird, wird das Level auf eins zurückgesetzt und die Anzahl der Versuche (try_count) wird auf null zurückgesetzt.
        Schließlich wird die generate_level-Funktion aufgerufen, um das neue Level zu generieren.
        """
        # Überprüft Benutzereingabeereignisse und aktualisiert den Spielstand entsprechend
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Schaltet die Musik ein/aus und aktualisiert das Musiksymbol entsprechend
                if self.music_toggle_rect.collidepoint(pygame.mouse.get_pos()):
                    if self.is_music_playing:
                        self.is_music_playing = False
                        self.music_toggle = self.sound_off
                        pygame.mixer.music.pause()
                    else:
                        self.is_music_playing = True
                        self.music_toggle = self.sound_on
                        pygame.mixer.music.unpause()
            # Geht zum nächsten Level über, wenn das aktuelle Level abgeschlossen ist und die Leertaste gedrückt wird
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.level_complete:
                    self.level += 1
                    pygame.mixer.music.unpause()
                    self.victory_sound.stop()
                    self.victory_end_sound.stop()
                    if self.level >= 6:
                        self.level = 1
                        self.try_count = 0
                        pygame.mixer.music.play()
                        self.get_video()
                    self.generate_level(self.level)

    def draw(self):
        """
        Die Funktion zeichnet das Spiel auf dem Bildschirm. Zunächst lädt sie Schriftarten und definiert Text für den Titel des Spiels,
        die Levelnummer und andere Informationen. Wenn ein Video abgespielt wird, wird es auf dem Bildschirm angezeigt oder ein Bild wird angezeigt.
        Je nach Levelnummer wird eine entsprechende Textnachricht angezeigt.
        Das Kachelset wird auf dem Bildschirm gezeichnet und die Funktion zeigt auch den Highscore und den Versuchszähler an.
        Wenn das Level abgeschlossen ist, zeigt die Funktion eine entsprechende Textnachricht an.
        """
        # Lade die Schriftarten
        title_font = pygame.font.Font('font/Pokemon_Solid.ttf', 74)
        content_font = pygame.font.Font('font/Pokemon_Solid.ttf', 30)

        # Definieren Sie den Text für den Titel des Spiels, die Levelnummer und die Spielinformationen.
        title_text = title_font.render('Pokémon Memory', True, RED)
        title_rect = title_text.get_rect(midtop=(WINDOW_WIDTH // 2, 10))

        level_text = content_font.render('Level ' + str(self.level), True, WHITE)
        level_rect = level_text.get_rect(midtop=(WINDOW_WIDTH // 2, 90))

        info_text = content_font.render('find 2 of each', True, WHITE)
        info_rect = info_text.get_rect(midtop=(WINDOW_WIDTH // 2, 120))

        highscore = content_font.render(f"Champion: {self.best_score}", True, GOLD)
        highscore_rect = highscore.get_rect(topleft = (WINDOW_WIDTH - 1270, 10))

        click = content_font.render(f"Your tries: {self.try_count}", True, RED)
        click_rect = click.get_rect(topleft = (WINDOW_WIDTH - 1270, 45))

        # Wenn das Video abgespielt wird, zeigen Sie das Video an oder zeigen Sie ein Bild an.
        if self.is_video_playing:
            if self.success:
                screen.blit(pygame.image.frombuffer(self.img.tobytes(), self.shape, 'BGR'), (0, 0))
            else:
                self.get_video()
        else:
            screen.blit(pygame.image.frombuffer(self.img.tobytes(), self.shape, 'BGR'), (0, 20))

        # Je nach Levelnummer wird die entsprechende Textnachricht angezeigt.
        if not self.level == 5:
            next_text = content_font.render('Level clear... Press space for the next level !', True, RED)
        else:
            if self.try_count == self.best_score:
                next_text = content_font.render('WOW!!! YOU ARE THE NEW CHAMP!!! Press space to try it again !', True, RED)
            else:
                next_text = content_font.render('Great, you finished the Game !!! Press space to play again !', True, RED)
        next_rect = next_text.get_rect(midbottom=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))

        screen.blit(title_text, title_rect)  # Zeigt den Titel des Spiels an.
        screen.blit(level_text, level_rect)  # Zeigt die Levelnummer an.
        screen.blit(info_text, info_rect)  # Zeigt die Spielinformationen an.
        screen.blit(highscore, highscore_rect)  # Zeigt den Highscore an
        screen.blit(click, click_rect)  # Zeigt den Versuchszähler an
        screen.blit(self.music_toggle, self.music_toggle_rect)  # Zeigt die Musik-Umschalttaste an.

        # Zeichnen Sie das Kachelset auf dem Bildschirm.
        self.tiles_group.draw(screen)
        self.tiles_group.update()

        # Zeigt die entsprechende Textnachricht an, wenn das Level abgeschlossen ist.
        if self.level_complete:
            screen.blit(next_text, next_rect)

    def get_video(self):
        """
        Diese Funktion lädt ein Video von einer Datei und liest das erste Frame des Videos als Bild ein.
        Das Attribut success wird auf True gesetzt, wenn das Lesen erfolgreich ist, ansonsten auf False. Das eingelesene Bild wird als img gespeichert,
        und die Form des Bildes wird in shape gespeichert.
        """
        self.cap = cv2.VideoCapture('vid/pokemon_background_long.mp4')
        self.success, self.img = self.cap.read()
        self.shape = self.img.shape[1::-1]

    def get_winvideo(self):

        self.cap = cv2.VideoCapture('vid/win.mp4')
        self.success, self.img = self.cap.read()
        self.shape = self.img.shape[1::-1]


# Pygame-Modul initialisieren
pygame.init()

# Richten Sie die Bildschirmabmessungen ein
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 860
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Legen Sie die Beschriftung des Spielfensters fest
pygame.display.set_caption('POKEMON MEMORY')

# Definieren Sie die RGB-Farbwerte für Weiß und Rot
WHITE = (255, 255, 255)
RED = (238, 21, 21)
GOLD = (207, 181, 59)

# Stellen Sie die Bilder pro Sekunde des Spiels ein
FPS = 60
clock = pygame.time.Clock()

# Erstelle eine neue Spielinstanz
game = Game()

# Setzen Sie die Laufvariable auf True und starten Sie die Spielschleife
running = True
while running:
    event_list = pygame.event.get()
    for event in event_list:
        # Spielen Sie Musik ab, wenn ein Benutzerereignis auftritt
        if event.type == pygame.USEREVENT:
            pygame.mixer.music.play()
        # Beenden Sie das Spiel, wenn ein Beendigungsereignis auftritt
        if event.type == pygame.QUIT:
            running = False
    # Aktualisiere das Spiel mit der aktuellen Eventliste
    game.update(event_list)
    # Aktualisieren Sie die Anzeige
    pygame.display.update()
    # Beschränken Sie das Spiel auf die Ausführung mit einem bestimmten FPS
    clock.tick(FPS)

pygame.quit()
