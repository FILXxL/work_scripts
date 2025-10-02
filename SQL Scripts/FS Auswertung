-- Get dynstamm_id 

SELECT DYNSTAMM_ID, ALPHA1 from DYNSTAMM WHERE ALPHA1 LIKE '%Herz%';

-- Get all entries with this dynstamm_id 


SELECT anm.anm_id, anm.anm_nr
FROM anm, anm_dyn, dynstamm, anm_info
WHERE anm.anm_id = anm_dyn.anm_id
AND anm_dyn.dynstamm3_id = dynstamm.dynstamm_id
AND anm.anm_id = anm_info.anm_id
AND dynstamm.dynstamm_id = 292
AND to_char(anm_info.anm_ang_am, 'yyyy') = '2025';