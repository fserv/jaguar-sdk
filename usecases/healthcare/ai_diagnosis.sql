

The patient table is a database of patient profile:

create table patient
( 
    key: 
        patientid uuid, 
    value: 
        first_name          char(64),
        middle_name         char(64),
        last_name           char(64),
        gender              char(16), 
        birthyear           smallint, 
        drivers_license     char(32),
        address             char(64),
        state               char(64)
);

The patient visits table records all patients visiting history:

create table  patient_visit
(
    key:
        patientid char(32),
        diagnoid  char(32),
    value:
        dtvisit   timestampsec
);


The diagnosis table has all the diagnosis history:

create table diagnosis
(
    key: 
        diagnoid uuid, 
    value: 
        exercise_per_week   tinyint,  
        height              smallint,
        weight              smallint,
        alcohol_per_week    smallint,
        cigarets_per_week   smallint,
        daily_sleep_hours   tinyint,
        blood_pressure_high smallint,
        blood_pressure_low  smallint,
        heart_rate          smallint,
        is_vegetarian       boolean, 
        cholesterol_ldl     smallint,
        cholesterol_hdl     smallint,

        symptoms_txt        char(2048),
        symptoms_vec        vector(1024, 'euclidean_fraction_float'),

        patient_input_txt   char(2048),
        patient_input_vec   vector(1024, 'euclidean_fraction_float'),

        ecg_image           file,
        ecg_vec             vector(1024, 'euclidean_fraction_float'),

        xray_image          file,
        xray_vec            vector(1024, 'euclidean_fraction_float'),

        mri_image           file,
        mri_vec             vector(1024, 'euclidean_fraction_float'),

        catscan_image       file,
        catscan_vec         vector(1024, 'euclidean_fraction_float'),
);


Register patients:

    insert into patient values ( 'Adam', 'D', 'Doe', 'M', 2000, 'B200220023', '123 ABC Street, San Francisco CA 92001', 'CA' );
    insert into patient values ( 'Eve', 'D', 'Doe', 'F', 1000, 'B200520823', '123 ABC Street, San Francisco CA 92001', 'CA' );


### https://www.rubomedical.com/dicom_files/
Record a patient visit and a diagnosis:

    insert into diagnosis values ( '8', '71', '165', '0', '0', '8', '120', '80','50', '0', '90', '60', 'Fever or chills, Cough, Shortness of breath or difficulty breathing, Fatigue, Muscle or body aches, Headache', 'symptoms_vector_string', 'Morgan had a rash on her hands, a rapid heart rate and unusually low blood pressure, developed red eyes and the skin on her lips cracked and split, Morgan complained of being sore all over and could barely stay awake', 'img/diagram_photo.dicom', 'vector_of_ecg_diagram_photo.dicom', 'img/xray.dicom', 'vector_of_xray.dicom', 'img/mri.dicom', 'vector_of_mdr.dicom', 'img/cat.dicom', 'vector_of_cat.dicom' );


Insert more diagnosis cases as shown above.


Record the patient and visit:

    insert into patient_visit values ( 'patient_id', 'diagnosis_id' );


Search all diagnostic cases which are similar to a reported symptom:

   select similarity(symptoms_vec, 'query_vector', 'topk=1000,type=euclidean_fraction_float')
   from diagnosis;


Search diagnostic cases which are similar to a reported symptom and satisfy age group and gender criteria:

   select similarity(symptoms_vec, 'query_vector', 'topk=1000,type=euclidean_fraction_float')
   from diagnosis
   where birthyear > 1980 and birthyear < 2000 and gender='Male'; 


Search diagnostic cases which are similar to a cat scan and satisfy drinking and smoking criteria:

   select similarity(symptoms_vec, 'query_vector', 'topk=1000,type=euclidean_fraction_float')
   from diagnosis
   where alcohol_per_week < 3 and cigarets_per_week < 3;


