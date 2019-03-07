import random as random    
import pygame as pygame

pygame.init()                                 #Starter Pygame spillmotoren
clock = pygame.time.Clock()                   #Delta tid. Det må vi snakke mer om!!
Screen = pygame.display.set_mode([650, 650])  #Lag et vindu på skjermen
Done = False                                  #Variabel for å holde styr på om vi trenger vinduet
MapSize = 25                                  #Hvor mange "fliser" nedover og bortover i spillet/brettet

TileWidth = 20                                #Hvor mange pixler per flis
TileHeight = 20
TileMargin = 4                                #Avstand mellom flisene

BLACK = (0, 0, 0)                             #Definer noen farger
WHITE = (255, 255, 255)                       #Tallene er verdier for hvor mye RØD, GRØNN og BLÅ
GREEN = (0, 255, 0)                           #Minimum 0, maks 255
RED = (255, 0, 0)                             #Man kan blande farger som man vil
BLUE = (0, 0, 255)



class MapTile(object):                       #En klasse for alt som står i ro. Gress, steiner, trær...
    def __init__(self, Name, Column, Row):
        self.Name = Name
        self.Column = Column
        self.Row = Row


class Character(object):                    #En klasse for spillfiguren, med Navn, HP og posisjon i kartet
    def __init__(self, Name, HP, Column, Row):  #Column er alle rutene nedover, men bare en rute bred
        self.Name = Name                    #Row er alle rutene bortover, men bare en rute høy
        self.HP = HP                        #Når man har en Row og en Column på kartet, danner de et plusstegn
        self.Column = Column                #Midt i plussen er spillfiguren. Vi kaller dette koordinater.
        self.Row = Row

    def Move(self, Direction):              #En funksjon for å bevege spillfiguren

        if Direction == "UP":
            if self.Row > 0:                #Sjekk om du er helt i toppen
                if self.CollisionCheck("UP") == False: #Sjekk om det er noe i veien
                   self.Row -= 1            #Gå en rute opp

        elif Direction == "LEFT":
            if self.Column > 0:
                if self.CollisionCheck("LEFT") == False:
                    self.Column -= 1

        elif Direction == "RIGHT":
            if self.Column < MapSize-1:
                if self.CollisionCheck("RIGHT") == False:
                         self.Column += 1

        elif Direction == "DOWN":
            if self.Row < MapSize-1:
                if self.CollisionCheck("DOWN") == False:
                    self.Row += 1

        Map.update()       

#Sjekk om det ligger noe på gresset i den retningen du vil gå. Brukt i "move"-funksjonen.
    def CollisionCheck(self, Direction):
        if Direction == "UP":
            if len(Map.Grid[self.Column][(self.Row)-1]) > 1:
                return True
        elif Direction == "LEFT":
            if len(Map.Grid[self.Column-1][(self.Row)]) > 1:
                return True
        elif Direction == "RIGHT":
            if len(Map.Grid[self.Column+1][(self.Row)]) > 1:
                return True
        elif Direction == "DOWN":
            if len(Map.Grid[self.Column][(self.Row)+1]) > 1:
                return True
        return False

    def Location(self):
        print("Coordinates: " + str(self.Column) + ", " + str(self.Row))


class Map(object): #Her er selve kartet, som en egen klasse
    global MapSize

    Grid = []

    for Row in range(MapSize):     #Lag et rutenett
        Grid.append([])
        for Column in range(MapSize):
            Grid[Row].append([])

    for Row in range(MapSize):     #Fyll rutenettet med gress
        for Column in range(MapSize):
            TempTile = MapTile("Grass", Column, Row)
            Grid[Column][Row].append(TempTile)

    for Row in range(MapSize):     #Legg ut noen steiner
        for Column in range(MapSize):
            TempTile = MapTile("Rock", Column, Row)
            if Row == 1:
                Grid[Column][Row].append(TempTile)

    for i in range(10):          #Sett ut noen trær
        RandomRow = random.randint(0, MapSize - 1)
        RandomColumn = random.randint(0, MapSize - 1)
        TempTile = MapTile("Tree", RandomColumn, RandomRow)
        Grid[RandomColumn][RandomRow].append(TempTile)

    RandomRow = random.randint(0, MapSize - 1)      #Sett spillfiguren en tilfeldig plass
    RandomColumn = random.randint(0, MapSize - 1)
    Hero = Character("Hero", 10, RandomColumn, RandomRow)

    def update(self):        #En veldig viktig funksjon.
                             #Den sjekker om objektenes egene koordinater
                             #stemmer med posisjonen i kartet.
                             #Hvis de er forskjellige, blir tingen flyttet
                             #til den plassen i kartet som stemmer med tingens
                             #egene koordinater.

        for Column in range(MapSize):      
            for Row in range(MapSize):
                for i in range(len(Map.Grid[Column][Row])):
                    if Map.Grid[Column][Row][i].Column != Column:
                        Map.Grid[Column][Row].remove(Map.Grid[Column][Row][i])
                    elif Map.Grid[Column][Row][i].Name == "Hero":
                        Map.Grid[Column][Row].remove(Map.Grid[Column][Row][i])
        Map.Grid[int(Map.Hero.Column)][int(Map.Hero.Row)].append(Map.Hero)

Map = Map()

while not Done:     #Selve hoved-loopen i pygame

    for event in pygame.event.get():         #Lytt til hendelser
        if event.type == pygame.QUIT:
            Done = True       

        elif event.type == pygame.MOUSEBUTTONDOWN:
            Pos = pygame.mouse.get_pos()
            Column = Pos[0] // (TileWidth + TileMargin)  #Oversetter muspekerens posisjon til koordinater i rutenettet.
            Row = Pos[1] // (TileHeight + TileMargin)
            print(str(Row) + ", " + str(Column))

            for i in range(len(Map.Grid[Column][Row])):
                print(str(Map.Grid[Column][Row][i].Name))  #Printer hva som er på kartet der du trykket

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                Map.Hero.Move("LEFT")
            if event.key == pygame.K_RIGHT:
                Map.Hero.Move("RIGHT")
            if event.key == pygame.K_UP:
                Map.Hero.Move("UP")
            if event.key == pygame.K_DOWN:
                Map.Hero.Move("DOWN")

    Screen.fill(BLACK)

    for Row in range(MapSize):           #Tegn rutenettet
        for Column in range(MapSize):
            for i in range(0, len(Map.Grid[Column][Row])):
                Color = WHITE
                if len(Map.Grid[Column][Row]) == 2:
                    Color = RED
                if Map.Grid[Column][Row][i].Name == "Hero":
                    Color = GREEN


            pygame.draw.rect(Screen, Color, [(TileMargin + TileWidth) * Column + TileMargin,
                                             (TileMargin + TileHeight) * Row + TileMargin,
                                             TileWidth,
                                             TileHeight])

    clock.tick(60)      #Begrens FPS til 60

    pygame.display.flip()     #Oppdaterer skjermen, slik at alt vi har endret med koden vises i vinduet.
    Map.update() #Oppdaterer kartet i minnet på maskinen.

pygame.quit()
