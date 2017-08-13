/*Creation of the tables*/

CREATE TABLE Storyline(
PageNo VARCHAR(50) PRIMARY KEY NOT NULL,
PageText TEXT NOT NULL,
MilestoneJournalEntry TEXT
); 

CREATE TABLE ReferenceDictionary(
Reference VARCHAR(50) PRIMARY KEY NOT NULL,
Name VARCHAR(255) NOT NULL,
Description TEXT
);

CREATE TABLE Interactions(
ReferenceDictionary_Reference VARCHAR(50) NOT NULL,
Name VARCHAR(255) NOT NULL,
Storyline_PageNo VARCHAR(50),
MapNo VARCHAR(50),
EmpathyValue INT,
SanityValue INT,
Description TEXT,
OptionalJournalEntry TEXT,
FOREIGN KEY(ReferenceDictionary_Reference) REFERENCES ReferenceDictionary(Reference),
FOREIGN KEY(Storyline_PageNo) REFERENCES Storyline(PageNo),
PRIMARY KEY(ReferenceDictionary_Reference,Name)
);

CREATE TABLE SavedSettings(
themes_themeName VARCHAR(50) NOT NULL
);

CREATE TABLE Colors(
Name VARCHAR(50) PRIMARY KEY NOT NULL, 
R FLOAT,
G FLOAT,
B FLOAT,
A FLOAT
);

CREATE TABLE Themes(
themeName VARCHAR(50) PRIMARY KEY NOT NULL,
themeDescription VARCHAR(50),
customButtonTextColor VARCHAR(50),
customButtonBackgrondColor VARCHAR(50), 
customLayoutCanvasColor VARCHAR(50), 
FOREIGN KEY(customButtonTextColor) REFERENCES Colors(Name),
FOREIGN KEY(customButtonBackgrondColor) REFERENCES Colors(Name),
FOREIGN KEY(customLayoutCanvasColor) REFERENCES Colors(Name)   
);

/*Populating the tables with test data*/
/*Opening database from command line: .open "Empathy.db" */

INSERT INTO Storyline
VALUES('page1','[ref=here]Here[/ref] goes the [ref=story][b][color=0000ff]story [/color][/b][/ref]lololol \nlol [ref=aegis][b][color=0000ff]aegis[/color][/b][/ref] Non [ref=lol][b][color=0000ff]existing[/color][/b][/ref] reference ','This is first milestone journal entry'); 

UPDATE Storyline
SET PageText = '[ref=here]Here[/ref] goes the [ref=story][b][color=0000ff]story [/color][/b][/ref]lololol 
lol [ref=aegis][b][color=0000ff]aegis[/color][/b][/ref] Non [ref=lol][b][color=0000ff]existing[/color][/b][/ref] reference.'
WHERE PageNo = 'page1';

INSERT INTO Storyline
VALUES('page2','[ref=here]Here[/ref] goes the [ref=story][b][color=0000ff]sadasd [/color][/b][/ref]lololol \n lol [ref=aegis][b][color=0000ff]kjkjaskj[/color][/b][/ref]','This is second milestone journal entry');

UPDATE Storyline
SET PageText = '[ref=here]Here[/ref] goes the [ref=story][b][color=0000ff]sadasd [/color][/b][/ref]lololol
lol [ref=aegis][b][color=0000ff]kjkjaskj[/color][/b][/ref]'
WHERE PageNo = 'page2';

INSERT INTO ReferenceDictionary
VALUES('story','enigmatic story','story written in 19th century');

INSERT INTO ReferenceDictionary
VALUES('aegis','aegis shield','Very old Greek shield');

INSERT INTO Interactions
VALUES('story','read','page1','map1',0,0,'What an interesting story!','This is optional journal entry'); 

INSERT INTO Interactions
VALUES('story','write','page1','map1',1,-2,'Who knows how to write?','');

INSERT INTO Interactions
VALUES('story','kiss','page1','map1',-2,-5,'What?','I just kissed that book!');

INSERT INTO SavedSettings
VALUES('Green_Theme'
);

INSERT INTO Colors VALUES('white',1,1,1,1);
INSERT INTO Colors VALUES('light_green',0.1,0.3, 0.06, 1);
INSERT INTO Colors VALUES('dark_green',0.03,0.07,0.01,1);
INSERT INTO Colors VALUES('light_blue',0,0,0.5,1);
INSERT INTO Colors VALUES('dark_blue',0,0,0.1,1);
INSERT INTO Colors VALUES('black',0,0,0,1);
INSERT INTO Colors VALUES('light_grey',0.88,0.88,0.88,1);
INSERT INTO Colors VALUES('dark_grey',0.94,0.94,0.94,1);

INSERT INTO Themes
VALUES('Green_Theme','Green Theme','white','light_green','dark_green'
);
INSERT INTO Themes
VALUES('Blue_Theme','Blue Theme','white','light_blue','dark_blue'
);
INSERT INTO Themes
VALUES('Grey_Theme','Grey Theme','black','light_grey','dark_grey'
);

/*testowe zapytania*/

UPDATE SavedSettings
SET themes_themeName='Blue_Theme';