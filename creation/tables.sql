CREATE TYPE document_type AS ENUM ('passport', 'medical_certificate', 'registration_of_residence', 'autoschool_certificate', 'inspector_certificate');
CREATE TYPE gearbox_type AS ENUM ('manual', 'automatic');
CREATE TYPE car_owner_type AS ENUM ('service', 'autoschool');
CREATE TYPE exam_result_type AS ENUM ('pending', 'passed', 'failed');
CREATE TYPE fine_status_type AS ENUM ('pending', 'paid');
CREATE TYPE driving_license_status_type AS ENUM ('suspended', 'revoked');
CREATE TYPE ticket_status_type AS ENUM ('pending', 'used', 'cancelled', 'expired');
CREATE TYPE category_type AS ENUM ('A', 'A1', 'B', 'B1', 'C', 'C1', 'D', 'D1', 'T', 'BE', 'C1E', 'CE', 'D1E', 'DE');

--

CREATE TABLE client (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL CHECK (date_of_birth < CURRENT_DATE),
    address VARCHAR(100) NOT NULL,
    phone_number VARCHAR(30) NOT NULL UNIQUE,
    email VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE service_center (
    id SERIAL PRIMARY KEY,
    address VARCHAR(100) NOT NULL UNIQUE,
    number INT NOT NULL UNIQUE
);

CREATE TABLE inspector (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50) NOT NULL,
    service_center_id INT NOT NULL REFERENCES service_center(id) ON DELETE CASCADE
); 

CREATE TABLE document (
    id SERIAL PRIMARY KEY,
    type document_type NOT NULL,
    end_date DATE NOT NULL CHECK (end_date > CURRENT_DATE),
    info_file_path VARCHAR(255) NOT NULL UNIQUE,
    client_id INT REFERENCES client(id) ON DELETE CASCADE,
    inspector_id INT REFERENCES inspector(id) ON DELETE CASCADE,
    CHECK (client_id IS NOT NULL OR inspector_id IS NOT NULL)
);

CREATE TABLE car (
    id SERIAL PRIMARY KEY,
    car_owner car_owner_type NOT NULL,
    gearbox gearbox_type NOT NULL,
    license_plate VARCHAR(10) NOT NULL UNIQUE,
    category category_type NOT NULL,
    service_center_id INT NOT NULL REFERENCES service_center(id) ON DELETE CASCADE
);

CREATE TABLE theory_ticket (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP NOT NULL,
    status ticket_status_type NOT NULL DEFAULT 'pending',
    service_center_id INT NOT NULL REFERENCES service_center(id) ON DELETE CASCADE,
    client_id INT NOT NULL REFERENCES client(id) ON DELETE CASCADE
);

CREATE TABLE driving_ticket (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP NOT NULL,
    status ticket_status_type NOT NULL DEFAULT 'pending',
    gearbox gearbox_type NOT NULL,
    category category_type NOT NULL,
    car_owner car_owner_type NOT NULL,
    service_center_id INT NOT NULL REFERENCES service_center(id) ON DELETE CASCADE,
    client_id INT NOT NULL REFERENCES client(id) ON DELETE CASCADE
);

CREATE TABLE theory_exam (
    id SERIAL PRIMARY KEY,
    theory_ticket_id INT NOT NULL UNIQUE REFERENCES theory_ticket(id) ON DELETE CASCADE
);

CREATE TABLE question (
    id SERIAL PRIMARY KEY,
    text VARCHAR(500) NOT NULL UNIQUE,
    photo_file_path VARCHAR(255) UNIQUE
);

CREATE TABLE answer (
    id SERIAL PRIMARY KEY,
    text VARCHAR(500) NOT NULL,
    photo_file_path VARCHAR(255) UNIQUE,
    is_correct BOOLEAN NOT NULL,
    question_id INT NOT NULL REFERENCES question(id) ON DELETE CASCADE,
    UNIQUE (question_id, text)
);

CREATE TABLE theory_exam_result (
    id SERIAL PRIMARY KEY,
    theory_exam_id INT NOT NULL REFERENCES theory_exam(id) ON DELETE CASCADE,
    question_id INT NOT NULL REFERENCES question(id) ON DELETE CASCADE,
    selected_answer_id INT NOT NULL REFERENCES answer(id) ON DELETE CASCADE,
    UNIQUE (theory_exam_id, question_id)
);

CREATE TABLE driving_exam (
    id SERIAL PRIMARY KEY,
    exam_result exam_result_type NOT NULL DEFAULT 'pending',
    video_file_path VARCHAR(255) UNIQUE,
    driving_ticket_id INT NOT NULL UNIQUE REFERENCES driving_ticket(id) ON DELETE CASCADE,
    inspector_id INT NOT NULL REFERENCES inspector(id) ON DELETE CASCADE,
    car_id INT REFERENCES car(id) ON DELETE CASCADE
);

CREATE TABLE driving_license (
    id SERIAL PRIMARY KEY,
    start_date DATE DEFAULT CURRENT_DATE CHECK (start_date = CURRENT_DATE),
    end_date DATE NOT NULL,
    client_id INT REFERENCES client(id) ON DELETE CASCADE,
    inspector_id INT REFERENCES inspector(id) ON DELETE CASCADE,
    CHECK (
        (inspector_id IS NOT NULL AND client_id IS NULL) OR
        (inspector_id IS NULL AND client_id IS NOT NULL)
    ),
    CHECK (end_date > start_date)
);

CREATE TABLE driving_license_category (
    id SERIAL PRIMARY KEY,
    category category_type NOT NULL,
    gearbox gearbox_type NOT NULL,
    driving_license_id INT NOT NULL REFERENCES driving_license(id) ON DELETE CASCADE,
    UNIQUE (category, gearbox, driving_license_id)
);

CREATE TABLE fine (
    id SERIAL PRIMARY KEY,
    status fine_status_type NOT NULL DEFAULT 'pending',
    issued_date DATE DEFAULT CURRENT_DATE CHECK (issued_date = CURRENT_DATE),
    reason VARCHAR(500) NOT NULL,
    sum INT NOT NULL CHECK (sum > 0),
    driving_license_id INT NOT NULL REFERENCES driving_license(id) ON DELETE CASCADE
);

CREATE TABLE driving_license_status (
    id SERIAL PRIMARY KEY,
    status driving_license_status_type NOT NULL,
    start_date DATE DEFAULT CURRENT_DATE CHECK (start_date = CURRENT_DATE),
    end_date DATE,
    reason VARCHAR(500) NOT NULL,
    driving_license_id INT NOT NULL REFERENCES driving_license(id) ON DELETE CASCADE,
    CHECK (end_date IS NULL OR end_date > start_date)
);

CREATE INDEX theory_ticket_datetime_index ON theory_ticket(datetime);
CREATE INDEX driving_ticket_datetime_gearbox_category_index ON driving_ticket(datetime, gearbox, category);
CREATE INDEX driving_exam_exam_result_index ON driving_exam(exam_result);
CREATE INDEX document_type_index ON document(type);
CREATE INDEX fine_status_index ON fine(status);
CREATE INDEX driving_license_status_index ON driving_license_status(status);
CREATE INDEX driving_license_end_date_index ON driving_license(end_date);