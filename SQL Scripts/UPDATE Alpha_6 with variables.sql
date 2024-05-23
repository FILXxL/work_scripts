-- Declare variables
DECLARE
    personennummer VARCHAR2(20 CHAR) := '6942069';  -- <-- KUNDENNUMMER eingeben
    alphakey VARCHAR2(150 CHAR) := 'xxx69420xxx';  -- <-- den Alpha6 Key eingeben
    
BEGIN
    -- Update the row
    UPDATE PERS_DYN
    SET alpha6 = alphakey
    WHERE pers_id IN (SELECT pers_id FROM pers WHERE PERS_NR = personennummer);

COMMIT;
END; 