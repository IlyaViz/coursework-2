COPY client(first_name, last_name, middle_name, date_of_birth, address, phone_number, email)
FROM 'C:\Users\User\Desktop/data/client.csv' DELIMITER ',' CSV;

COPY service_center(address, number)
FROM 'C:\Users\User\Desktop/data/service_center.csv' DELIMITER ',' CSV;

COPY inspector(first_name, last_name, middle_name, service_center_id)
FROM 'C:\Users\User\Desktop/data/inspector.csv' DELIMITER ',' CSV;

COPY driving_license(end_date, inspector_id)
FROM 'C:\Users\User\Desktop/data/inspector_driving_license.csv' DELIMITER ',' CSV;

COPY driving_license_category(category, gearbox, driving_license_id)
FROM 'C:\Users\User\Desktop/data/inspector_driving_license_category.csv' DELIMITER ',' CSV;

COPY document(type, end_date, info_file_path, client_id, inspector_id)
FROM 'C:\Users\User\Desktop/data/document.csv' DELIMITER ',' CSV;

COPY car(car_owner, gearbox, license_plate, category, service_center_id)
FROM 'C:\Users\User\Desktop/data/car.csv' DELIMITER ',' CSV;

COPY theory_ticket(datetime, status, service_center_id, client_id)
FROM 'C:\Users\User\Desktop/data/theory_ticket.csv' DELIMITER ',' CSV;

COPY theory_exam(theory_ticket_id)
FROM 'C:\Users\User\Desktop/data/theory_exam.csv' DELIMITER ',' CSV;

COPY question(text, photo_file_path)
FROM 'C:\Users\User\Desktop/data/question.csv' DELIMITER ',' CSV;

COPY answer(text, photo_file_path, is_correct, question_id)
FROM 'C:\Users\User\Desktop/data/answer.csv' DELIMITER ',' CSV;

COPY theory_exam_result(theory_exam_id, question_id, selected_answer_id)
FROM 'C:\Users\User\Desktop/data/theory_exam_result.csv' DELIMITER ',' CSV;

COPY driving_ticket(datetime, status, gearbox, car_owner, service_center_id, client_id, category)
FROM 'C:\Users\User\Desktop/data/driving_ticket.csv' DELIMITER ',' CSV;

COPY driving_exam(exam_result, video_file_path, driving_ticket_id, inspector_id, car_id)
FROM 'C:\Users\User\Desktop/data/driving_exam.csv' DELIMITER ',' CSV;

/*
COPY driving_license(end_date, client_id)
FROM 'C:\Users\User\Desktop/data/client_driving_license.csv' DELIMITER ',' CSV;

COPY driving_license_category(category, gearbox, driving_license_id)
FROM 'C:\Users\User\Desktop/data/client_driving_license_category.csv' DELIMITER ',' CSV;
*/

COPY fine(status, reason, sum, driving_license_id)
FROM 'C:\Users\User\Desktop/data/fine.csv' DELIMITER ',' CSV;

COPY driving_license_status(status, end_date, reason, driving_license_id)
FROM 'C:\Users\User\Desktop/data/driving_license_status.csv' DELIMITER ',' CSV;