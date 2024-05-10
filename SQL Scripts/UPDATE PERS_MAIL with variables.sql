-- Declare variables
DECLARE
    personennummer VARCHAR2(20 CHAR) := '19877471';  -- <-- KUNDENNUMMER eingeben
    mailneu VARCHAR2(150 CHAR) := 'hugo.test@gmail.com';  -- <-- die NEUE Mailadresse eingeben
    mailalt VARCHAR2(150 CHAR) := 'philipp.janicek@gmail.com';  -- <-- die ALTE Mailadresse eingeben
BEGIN
    -- Update the row
    UPDATE PERS
    SET PERS_EMAIL = mailneu,
        PERS_EMAIL2 = 'ALT: ' || mailalt
    WHERE PERS_NR = personennummer AND PERS_EMAIL = mailalt;

COMMIT;
END; 