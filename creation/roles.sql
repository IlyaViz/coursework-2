REASSIGN OWNED BY theory_manager TO postgres;
REASSIGN OWNED BY service_center_manager TO postgres;
REASSIGN OWNED BY main_manager TO postgres;
REASSIGN OWNED BY theory_exam_result_manager TO postgres;
REASSIGN OWNED BY driving_license_manager TO postgres;
REASSIGN OWNED BY analysis_manager TO postgres;

DROP OWNED BY theory_manager;
DROP OWNED BY service_center_manager;
DROP OWNED BY main_manager;
DROP OWNED BY theory_exam_result_manager;
DROP OWNED BY driving_license_manager;
DROP OWNED BY analysis_manager;

DROP ROLE theory_manager;
DROP ROLE service_center_manager;
DROP ROLE main_manager;
DROP ROLE theory_exam_result_manager;
DROP ROLE driving_license_manager;
DROP ROLE analysis_manager;

--

CREATE USER theory_manager WITH PASSWORD '1';
GRANT SELECT, INSERT, UPDATE, DELETE ON question TO theory_manager;
GRANT SELECT, INSERT, UPDATE, DELETE ON answer TO theory_manager;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO theory_manager;

CREATE USER service_center_manager WITH PASSWORD '1';
GRANT SELECT, INSERT, UPDATE, DELETE ON service_center TO service_center_manager;
GRANT SELECT, INSERT, UPDATE, DELETE ON car TO service_center_manager;
GRANT SELECT, INSERT, UPDATE, DELETE ON inspector TO service_center_manager;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO theory_manager;

CREATE USER main_manager WITH PASSWORD '1';
GRANT SELECT, INSERT, UPDATE, DELETE ON client TO main_manager;
GRANT SELECT, INSERT, UPDATE, DELETE ON document TO main_manager;
GRANT SELECT, INSERT, UPDATE, DELETE ON driving_ticket TO main_manager;
GRANT SELECT, INSERT, UPDATE, DELETE ON theory_ticket TO main_manager;
GRANT SELECT, INSERT, UPDATE, DELETE ON driving_exam TO main_manager;
GRANT SELECT, INSERT, UPDATE, DELETE ON theory_exam TO main_manager;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO theory_manager;

CREATE USER theory_exam_result_manager WITH PASSWORD '1';
GRANT SELECT, INSERT, UPDATE, DELETE ON theory_exam_result TO theory_exam_result_manager;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO theory_manager;

CREATE USER driving_license_manager WITH PASSWORD '1';
GRANT SELECT, INSERT, UPDATE, DELETE ON driving_license TO driving_license_manager;
GRANT SELECT, INSERT, UPDATE, DELETE ON driving_license_category TO driving_license_manager;
GRANT SELECT, INSERT, UPDATE, DELETE ON driving_license_status TO driving_license_manager;
GRANT SELECT, INSERT, UPDATE, DELETE ON fine TO driving_license_manager;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO theory_manager;

CREATE USER analysis_manager WITH PASSWORD '1';
GRANT SELECT ON ALL TABLES IN SCHEMA public TO analysis_manager;