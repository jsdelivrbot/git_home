SELECT admissions.subject_id AS subject_id,
       admissions.hadm_id AS hadm_id,
       admissions.admittime,
       admissions.dischtime,
       admissions.deathtime,
       admissions.admission_type,
       admissions.diagnosis,
       STRING_AGG(diagnoses_icd.seq_num, ' ') AS diagnosis_seq,
       STRING_AGG(diagnoses_icd.icd9_code, ' ') AS diagnoses,
       STRING_AGG(procedures_icd.seq_num, ' ') AS procedures_seq,
       STRING_AGG(procedures_icd.icd9_code, ' ') AS procedures,
       patients.gender AS gender,
       patients.dob AS DOB,
       patients.dod AS DOD,
       patients.dod_hosp AS DOD_HOSP,
       patients.dod_ssn AS DOD_SSN,
       patients.expire_flag,
       STRING_AGG(prescription.drug_type, ' ') AS drug_types,
       STRING_AGG(prescription.drug, ' ') AS drugs

FROM admissions,
     diagnoses_icd,
     procedures_icd,
     patients,
     prescription

WHERE admissions.subject_id = diagnoses_icd.subject_id
      AND admissions.hadm_id = diagnoses_icd.hadm_id
      AND admissions.subject_id = procedures_icd.subject_id
      AND admissions.hadm_id = procedures_icd.hadm_id
      AND admissions.subject_id = patients.subject_id
      AND admissions.subject_id = prescription.subject_id
      AND admissions.hadm_id = prescription.hadm_id

GROUP BY admissions.subject_id,
         admissions.hadm_id,
         admissions.admittime,
         admissions.dischtime,
         admissions.deathtime,
         admissions.admission_type,
         admissions.diagnosis
         patients.gender,
         patients.dob,
         patients.dod,
         patients.dod_hosp,
         patients.dod_ssn,
         patients.expire_flag

ORDER BY subject_id ASC,
         hadm_id ASC
