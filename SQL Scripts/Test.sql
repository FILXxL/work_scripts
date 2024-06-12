SELECT
  DISTINCT
  (Anm.anm_id) as ANM_ID, 
  (anm.anm_nr) as ANM_NR, 
  (pers.pers_id) as PERS_ID, 
  (pers.pers_nr) as PERS_NR, 
  (pers.pers_titel) as PERS_TITEL, 
  (pers.pers_name) as PERS_NAME, 
  (pers.pers_vname) as PERS_VNAME, 
  (pers.pers_geschl) as PERS_GESCHL, 
  (decode (pers.pers_geschl,'M','Sehr geehrter Herr','W','Sehr geehrte Frau','Guten Tag') ) as ANREDE, 
  (ver.ver_id) as VER_ID, 
  (ver.ver_nr) as VER_NR, 
  (ver.ver_titel1) as VER_TITEL, 
  (to_char (ver.ver_beginn, 'dd.mm.yyyy') ) as VER_BEGINN, 
  (to_char (ver.VER_ENDE, 'dd.mm.yyyy') ) as VER_ENDE, 
  (ver_dyn.alpha5) as VER_DYN_ALPHA5, 
  (ver_dyn.alpha1) as VER_DYN_ALPHA1, 
  (CASE WHEN ver_dyn.alpha5 IS NOT NULL THEN ver_dyn.alpha5 ELSE ver.ver_titel1 END) AS Leistungsbeschreibung, 
  (vort.vort_id) as VORT_ID, 
  (vort.VORT_NAME1) as VORT_NAME1, 
  (vort.vort_name2) as VORT_NAME2, 
  (vort.vort_name3) as VORT_NAME3, 
  (vort.VORT_NATKENNZ) as VORT_NATKENNZ, 
  (vort.VORT_PLZ) as VORT_PLZ, 
  (vort.VORT_ORT) as VORT_ORT, 
  (vort.vort_str) as VORT_STR, 
  (vort.VORT_TEL) as VORT_TEL, 
  (vort.VORT_EMAIL) as VORT_EMAIL, 
  (vtyp.vtyp_id) as VTYP_ID, 
  (anm_ertr.anm_ertr_id) as ANM_ERTR_ID, 
  (anm_ertr.anm_ertr_bez) as ANM_ERTR_BEZ, 
  (anm_ertr.anm_ertr_preis) as ANM_ERTR_PREIS, 
  (anm_ertr.ANM_ERTR_ZTEXT) as ANM_ERTR_ZTEXT, 
  ( (decode (substr (anm_ertr.anm_ertr_ztext,1,11) , 'Teilnehmer:', substr (anm_ertr.anm_ertr_ztext,1,200) , pers.pers_name || ' ' || pers.pers_vname) ) ) as TEILNEHMER, 
  (ertr.ertr_id) as ERTR_ID, 
  (ertr.ertr_bez) as ERTR_BEZ, 
  (anm_dyn.anm_id) as ANM_DYN_ANM_ID, 
  (anm_dyn.alpha1) as ANM_DYN_ALPHA1, 
  (re.re_id) as RE_ID, 
  (re.re_nr) as RE_NR, 
  (re.RE_ADR1_NAME1) as RE_ADR1_NAME1, 
  (re.RE_ADR1_NAME2) as RE_ADR1_NAME2, 
  (re.RE_ADR1_STR) as RE_ADR1_STR, 
  (re.RE_ADR1_NATKENNZ) as RE_ADR1_NATKENNZ, 
  (re.RE_ADR1_PLZ) as RE_ADR1_PLZ, 
  (re.RE_ADR1_ORT) as RE_ADR1_ORT, 
  (re.RE_ADR1_NR) as RE_ADR1_NR, 
  (re.RE_DATUM) as RE_DATUM, 
  (repos.re_id) as REPOS_RE_ID, 
  (repos.repos_text) as REPOS_TEXT, 
  (repos.REPOS_MENGE) as REPOS_MENGE, 
  (repos.REPOS_MWST) as REPOS_MWST, 
  (ROUND ( ( (anm_ertr.anm_ertr_preis * (1 + (repos.REPOS_MWST / 100) ) ) * repos.repos_Menge) , 2.00) ) AS Brutto_Gelistet, 
  (ROUND ( (anm_ertr.anm_ertr_preis * (1 + (repos.REPOS_MWST / 100) ) ) , 2.00) - anm_ertr.anm_ertr_preis) AS MwSt_Gelistet, 
  (ROUND ( (anm_ertr.anm_ertr_preis * repos.REPOS_MENGE) , 2.00) ) AS Netto_Gesamtbetrag, 
  (SELECT
  SUM (TO_NUMBER (anm_ertr.anm_ertr_preis ) ) 
FROM
  anm_ertr, re 
WHERE 
anm_ertr.anm_ertr_rnr = re.re_nr 
AND re.re_id = re.re_id and re.re_nr= '1898034'
GROUP BY 
  re.re_nr) as NETTOmitMENGE 
FROM
  anm, 
  pers, 
  ver, 
  ver_dyn, 
  vort, 
  VTYP, 
  anm_ertr, 
  ertr, 
  anm_dyn, 
  re, 
  repos 
WHERE 
anm.pers_id = pers.pers_id 
AND anm.ver_id = ver.ver_id 
AND anm.ver_id = ver_dyn.ver_id 
AND ver.vort_id = vort.vort_id 
AND ver.vtyp_id = vtyp.vtyp_id 
AND anm.anm_id = anm_ertr.anm_id 
AND anm_ertr.ertr_id = ertr.ertr_id 
AND anm.anm_id = anm_dyn.anm_id 
AND anm_ertr.anm_ertr_rnr = re.re_nr 
AND re.re_id = repos.re_id and re.re_nr= '1898034';