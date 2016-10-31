COPY (
	WITH diagnosis AS (
		SELECT subject_id,
			   hadm_id,
			   STRING_AGG(diagnoses_icd.seq_num::character, ' ') AS diagnosis_seq,
			   STRING_AGG(diagnoses_icd.icd9_code, ' ') AS diagnoses
		FROM diagnoses_icd
		GROUP BY subject_id,
				 hadm_id
	),
	procedures AS (
		SELECT subject_id,
			   hadm_id,
			   STRING_AGG(procedures_icd.seq_num::character, ' ') AS procedures_seq,
			   STRING_AGG(procedures_icd.icd9_code, ' ') AS procedures
		FROM procedures_icd
		GROUP BY subject_id,
				 hadm_id
	),
	prescription AS (
		SELECT subject_id,
			   hadm_id,
			   STRING_AGG(prescriptions.drug_type, ' ') AS drug_types,
			   STRING_AGG(prescriptions.drug, ' ') AS drugs
		FROM prescriptions
		GROUP BY subject_id,
				 hadm_id
	),
	admission AS (
		SELECT subject_id,
			   hadm_id,
			   admittime,
			   dischtime,
			   deathtime,
			   admission_type,
			   diagnosis
		FROM admissions
	),
	patient AS (
		SELECT subject_id,
			   gender,
			   dob,
			   dod,
			   dod_hosp,
			   dod_ssn,
			   expire_flag
		FROM patients
	)
	SELECT admission.subject_id AS subject_id,
		   admission.hadm_id AS hadm_id,
		   gender,
		   TO_CHAR(dob, 'YYYY/MM/DD') AS dob,
		   TO_CHAR(dod, 'YYYY/MM/DD') AS dod,
		   TO_CHAR(dod_hosp, 'YYYY/MM/DD') AS dod_hosp,
		   TO_CHAR(dod_ssn, 'YYYY/MM/DD') AS dod_ssn,
		   expire_flag,
		   TO_CHAR(admittime, 'YYYY/MM/DD') AS admittime,
		   TO_CHAR(dischtime, 'YYYY/MM/DD') AS dischtime,
		   TO_CHAR(deathtime, 'YYYY/MM/DD') AS deathtime,
		   admission_type,
		   admission.diagnosis AS initial_diagnosis,
		   diagnosis_seq,
		   diagnoses,
		   procedures_seq,
		   procedures.procedures AS procedures,
		   drug_types,
		   drugs
	FROM admission,
		 patient,
		 diagnosis,
		 procedures,
		 prescription
	WHERE admission.subject_id = patient.subject_id
		  AND admission.hadm_id = diagnosis.hadm_id
		  AND admission.subject_id = diagnosis.subject_id
		  AND admission.subject_id = procedures.subject_id
		  AND admission.hadm_id = procedures.hadm_id
		  AND admission.subject_id = prescription.subject_id
		  AND admission.hadm_id = prescription.hadm_id

	ORDER BY subject_id ASC,
			 hadm_id ASC
) TO 'E:\Data\mimic3\postgresql\extract_diagnosis_2.csv' WITH CSV DELIMITER ',' HEADER;