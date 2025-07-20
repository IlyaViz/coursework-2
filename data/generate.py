import random
import csv
import datetime
from faker import Faker


fake = Faker()

document_types = ['passport', 'medical_certificate', 'registration_of_residence', 'autoschool_certificate', 'inspector_certificate']
gearbox_types = ['manual', 'automatic']
car_owner_types = ['service', 'autoschool']
exam_results = ['pending', 'passed', 'failed']
fine_statuses = ['pending', 'paid']
ticket_statuses = ['pending', 'used', 'cancelled', 'expired']
categories = ['A', 'A1', 'B', 'B1', 'C', 'C1', 'D', 'D1', 'T', 'BE', 'C1E', 'CE', 'D1E', 'DE']
license_statuses = ['suspended', 'revoked']

def calculate_age(born):
    today = datetime.date.today()

    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def generate_clients(num):
    clients = []

    for x in range(num):
        clients.append({
            "id": x + 1,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "middle_name": fake.first_name(),
            "date_of_birth": fake.date_of_birth(minimum_age=16, maximum_age=70),
            "address": fake.address(),
            "phone_number": fake.phone_number(),
            "email": f"{x}{fake.email()}",
        })

    return clients

def generate_service_centers(num):
    service_centers = []

    for x in range(num):
        service_centers.append({
            "id": x + 1,
            "address": f"{fake.street_address()}, {fake.city()}",
            "number": x
        })

    return service_centers

def generate_inspectors(num, service_centers):
    inspectors = []

    for x in range(num):
        inspectors.append({
            "id": x + 1,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "middle_name": fake.first_name(),
            "service_center_id": random.choice(service_centers)["id"]
        })

    return inspectors

def generate_documents(clients, inspectors):
    documents = []

    for num, client in enumerate(clients):
        is_driving_client = random.random() > 0.5

        documents.append({
            "type": "passport",
            "end_date": fake.future_date(end_date="+10y"),
            "info_file_path": f"{num + 1}_client_passport.pdf",
            "client_id": client["id"],
            "inspector_id": None })
        documents.append({
            "type": "registration_of_residence",
            "end_date": fake.future_date(end_date="+1y"),
            "info_file_path": f"{num + 1}_client_registration_of_residence.pdf",
            "client_id": client["id"],
            "inspector_id": None })
        
        if is_driving_client:
            client["is_driving_client"] = True

            documents.append({
                "type": "medical_certificate",
                "end_date": fake.future_date(end_date="+1y"),
                "info_file_path": f"{num + 1}_client_medical_certificate.pdf",
                "client_id": client["id"],
                "inspector_id": None })
            documents.append({
                "type": "autoschool_certificate",
                "end_date": fake.future_date(end_date="+1y"),
                "info_file_path": f"{num + 1}_client_autoschool_certificate.pdf",
                "client_id": client["id"],
                "inspector_id": None })
        else:
            client["is_driving_client"] = False

    for num, inspector in enumerate(inspectors):
        documents.append({
            "type": "passport",
            "end_date": fake.future_date(end_date="+10y"),
            "info_file_path": f"{num + 1}_inspector_passport.pdf",
            "client_id": None,
            "inspector_id": inspector["id"] })
        documents.append({
            "type": "inspector_certificate",
            "end_date": fake.future_date(end_date="+1y"),
            "info_file_path": f"{num + 1}_inspector_certificate.pdf",
            "client_id": None,
            "inspector_id": inspector["id"] })
            
    return documents

def generate_cars(num, service_centers):
    cars = []

    for x in range(num):
        cars.append({
            "id": x + 1,
            "car_owner": random.choice(car_owner_types),
            "gearbox": random.choice(gearbox_types),
            "license_plate": fake.license_plate(),
            "category": random.choice(categories),
            "service_center_id": random.choice(service_centers)["id"]
        })

    return cars

def generate_theory_tickets(clients, service_centers):
    tickets = []

    for client in clients:
        failed_attempts = random.randint(1, 3)
        last_datetime = fake.future_datetime(end_date="+1y")

        for _ in range(failed_attempts):
            tickets.append({
                "id": len(tickets) + 1,
                "datetime": last_datetime,
                "status": "used",
                "service_center_id": random.choice(service_centers)["id"],
                "client_id": client["id"]
            })

            last_datetime += datetime.timedelta(days=random.randint(10, 30))
      
        has_passed = random.random() > 0.5

        if has_passed:
            client["passed_theory"] = True
        else:
            client["passed_theory"] = False

            tickets.append({
                "id": len(tickets) + 1,
                "datetime": last_datetime,
                "status": "pending",
                "service_center_id": random.choice(service_centers)["id"],
                "client_id": client["id"]
            })

    return tickets

def generate_driving_tickets(clients, service_centers, cars):
    tickets = []

    for client in clients:
        if client["passed_theory"] and client["is_driving_client"]:
            attempts = random.randint(1, 3)
            last_datetime = fake.future_datetime(end_date="+1y")

            age = calculate_age(client["date_of_birth"])

            allowed_categories = []

            if age >= 16:
                allowed_categories += ['A', 'A1']
            if age >= 18:
                allowed_categories += ['B', 'B1', 'C', 'C1']
            if age >= 19:
                allowed_categories += ['BE', 'CE', 'C1E']
            if age >= 21:
                allowed_categories += ['D', 'D1', 'DE', 'D1E', 'T']

            service_center = random.choice(service_centers)

            allowed_cars = list(filter(lambda car: car["category"] in allowed_categories and car["service_center_id"] == service_center["id"], cars))
            car = random.choice(allowed_cars)

            for _ in range(attempts):
                tickets.append({
                    "id": len(tickets) + 1,
                    "datetime": last_datetime,
                    "status": "used",
                    "gearbox": car["gearbox"],
                    "car_owner": car["car_owner"],
                    "service_center_id": service_center["id"],
                    "client_id": client["id"],
                    "category": car["category"]
                })

                last_datetime += datetime.timedelta(days=random.randint(10, 30))

            has_passed = random.random() > 0.5

            if has_passed:
                client["passed_driving"] = True
            else:
                client["passed_driving"] = False

                tickets.append({
                    "id": len(tickets) + 1,
                    "datetime": last_datetime,
                    "status": "pending",
                    "gearbox": car["gearbox"],
                    "car_owner": car["car_owner"],
                    "service_center_id": service_center["id"],
                    "client_id": client["id"],
                    "category": car["category"]
                    })
        else:
            client["passed_driving"] = False

    return tickets

def generate_theory_exam(clients, theory_tickets):
    exams = []

    for client in clients:
        client_theory_tickets = [ticket for ticket in theory_tickets if ticket["client_id"] == client["id"]]

        if len(client_theory_tickets) > 1:
            for failed_ticket in client_theory_tickets[:-1]:
                exams.append({
                    "id": len(exams) + 1,
                    "theory_ticket_id": failed_ticket["id"]
                })

        if client["passed_theory"]:
            exams.append({
                "id": len(exams) + 1,
                "theory_ticket_id": client_theory_tickets[-1]["id"]
            })     

    return exams

def generate_questions(num):
    questions = []

    for x in range(num):
        questions.append({
            "id": x + 1,
            "text": fake.text(max_nb_chars=100),
            "photo_file_path": f"{x}_photo.jpg"
        })

    return questions

def generate_answers(questions):
    answers = []

    for question in questions:
        question_count = random.randint(2, 5)
        correct_question_number = random.randint(0, question_count - 1)

        for x in range(question_count):
            answers.append({
                "id": len(answers) + 1,
                "question_id": question["id"],
                "text": fake.text(max_nb_chars=50),
                "photo_file_path": f"{question['id']}_{x}_photo.jpg",
                "is_correct": x == correct_question_number
            })

    return answers

def generate_theory_exam_results(clients, theory_exams, theory_tickets, questions, answers):
    results = []

    for client in clients:
        client_theory_tickets = [ticket for ticket in theory_tickets if ticket["client_id"] == client["id"]]
        client_theory_exams = [exam for exam in theory_exams if exam["theory_ticket_id"] in [ticket["id"] for ticket in client_theory_tickets]]

        if len(client_theory_exams) > 1:
            for failed_exam in client_theory_exams[:-1]:
                selected_questions = random.sample(questions, random.randint(0, 17))

                for question in selected_questions:
                    correct_answer = list(filter(lambda answer: answer["question_id"] == question["id"] and answer["is_correct"], answers))[0]
                    
                    results.append({
                        "theory_exam_id": failed_exam["id"],
                        "question_id": question["id"],
                        "answer_id": correct_answer["id"]
                    })

                remaining_questions = list(filter(lambda question: question not in selected_questions, questions))
                selected_questions = random.sample(remaining_questions, 20 - len(selected_questions))

                for question in selected_questions:
                    incorrect_answer = list(filter(lambda answer: answer["question_id"] == question["id"] and not answer["is_correct"], answers))[0]

                    results.append({
                        "theory_exam_id": failed_exam["id"],
                        "question_id": question["id"],
                        "answer_id": incorrect_answer["id"]
                    })

        if client["passed_theory"]:
            selected_questions = random.sample(questions, random.randint(18, 20))

            for question in selected_questions:
                correct_answer = list(filter(lambda answer: answer["question_id"] == question["id"] and answer["is_correct"], answers))[0]

                results.append({
                    "theory_exam_id": client_theory_exams[-1]["id"],
                    "question_id": question["id"],
                    "answer_id": correct_answer["id"]
                })

            remaining_questions = list(filter(lambda question: question not in selected_questions, questions))
            selected_questions = random.sample(remaining_questions, 20 - len(selected_questions))

            for question in selected_questions:
                incorrect_answer = list(filter(lambda answer: answer["question_id"] == question["id"] and not answer["is_correct"], answers))[0]

                results.append({
                    "theory_exam_id": client_theory_exams[-1]["id"],
                    "question_id": question["id"],
                    "answer_id": incorrect_answer["id"]
                })

    return results

def generate_driving_exam(clients, driving_tickets, cars, inspectors):
    exams = []

    for client in clients:
        client_driving_tickets = [ticket for ticket in driving_tickets if ticket["client_id"] == client["id"]]
        

        if len(client_driving_tickets) > 1:
            for failed_ticket in client_driving_tickets[:-1]:
                allowed_cars = list(filter(lambda car: car["category"] == failed_ticket["category"] and car["gearbox"] == failed_ticket["gearbox"] and car["car_owner"] == failed_ticket["car_owner"], cars))
                car = random.choice(allowed_cars)

                exams.append({
                    "exam_result": "failed",
                    "video_file_path": f"{failed_ticket['id']}_video.mp4",
                    "driving_ticket_id": failed_ticket["id"],
                    "inspector_id": random.choice(inspectors)["id"],
                    "car_id": car["id"]
                })

        if client["passed_driving"]:
            allowed_cars = list(filter(lambda car: car["category"] == client_driving_tickets[-1]["category"] and car["gearbox"] == client_driving_tickets[-1]["gearbox"] and car["car_owner"] == client_driving_tickets[-1]["car_owner"], cars))
            car = random.choice(allowed_cars)

            exams.append({
                "exam_result": "passed",
                "video_file_path": f"{client_driving_tickets[-1]['id']}_video.mp4",
                "driving_ticket_id": client_driving_tickets[-1]["id"],
                "inspector_id": random.choice(inspectors)["id"],
                "car_id": car["id"]
            })

    return exams

def generate_licenses(clients, inspectors):
    licenses = []

    for inspector in inspectors:
        licenses.append({
            "id": len(licenses) + 1,
            "end_date": fake.future_date(end_date="+10y"),
            "client_id": None,
            "inspector_id": inspector["id"]
        })

    for client in clients:
        if client["passed_driving"]:
            licenses.append({
                "id": len(licenses) + 1,
                "end_date": fake.future_date(end_date="+10y"),
                "client_id": client["id"],
                "inspector_id": None
            })

    return licenses

def generate_license_categories(clients, inspectors, licenses, driving_tickets):
    license_categories = []

    for client in clients:
        if client["passed_driving"]:
            passed_driving_ticket = [driving_ticket for driving_ticket in driving_tickets if driving_ticket["client_id"] == client["id"] and driving_ticket["status"] == "used"][-1]
            client_license = [license for license in licenses if license["client_id"] == client["id"]][0]

            license_categories.append({
                "category": passed_driving_ticket["category"],
                "gearbox": passed_driving_ticket["gearbox"],
                "license_id": client_license["id"]
            })

    for inspector in inspectors:
        inspector_license = [license for license in licenses if license["inspector_id"] == inspector["id"]][0]

        for category in categories:
            license_categories.append({
                "category": category,
                "gearbox": "manual",
                "license_id": inspector_license["id"]
            })

        for category in categories:
            license_categories.append({
                "category": category,
                "gearbox": "automatic",
                "license_id": inspector_license["id"]
            })


    return license_categories
    

def generate_fines(num, licenses):
    fines = []

    for _ in range(num):
        fines.append({
            "status": random.choice(fine_statuses),
            "reason": fake.text(max_nb_chars=50),
            "sum": random.randint(50, 500),
            "license_id": random.choice(licenses)["id"]
        })
    return fines

def generate_license_statuses(num, licenses):
    statuses = []

    for _ in range(num):
        statuses.append({
            "status": random.choice(license_statuses),
            "end_date": fake.future_date(end_date="+1y"),
            "reason": fake.text(max_nb_chars=50),
            "license_id": random.choice(licenses)["id"]
        })
    return statuses

def save_to_csv(filepath, data, fieldnames):
    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        for row in data:
            writer.writerow([row[field] for field in fieldnames])

clients = generate_clients(1000)
service_centers = generate_service_centers(2)
inspectors = generate_inspectors(10, service_centers)
documents = generate_documents(clients, inspectors)
cars = generate_cars(50, service_centers)
theory_tickets = generate_theory_tickets(clients, service_centers)
theory_exams = generate_theory_exam(clients, theory_tickets)
questions = generate_questions(100)
answers = generate_answers(questions)
theory_exam_results = generate_theory_exam_results(clients, theory_exams, theory_tickets, questions, answers)
driving_tickets = generate_driving_tickets(clients, service_centers, cars)
driving_exams = generate_driving_exam(clients, driving_tickets, cars, inspectors)
licenses = generate_licenses(clients, inspectors)
client_liceneses = [license for license in licenses if license["client_id"] is not None]
inspector_licenses = [license for license in licenses if license["inspector_id"] is not None]
license_categories = generate_license_categories(clients, inspectors, licenses, driving_tickets)
client_license_categories = [category for category in license_categories if category["license_id"] in [license["id"] for license in client_liceneses]]
inspector_license_categories = [category for category in license_categories if category["license_id"] in [license["id"] for license in inspector_licenses]]
fines = generate_fines(5, licenses)
license_statuses = generate_license_statuses(1, licenses)

save_to_csv("C:/Users/User/Desktop/data/client.csv", clients, ["first_name", "last_name", "middle_name", "date_of_birth", "address", "phone_number", "email"])
save_to_csv("C:/Users/User/Desktop/data/service_center.csv", service_centers, ["address", "number"])
save_to_csv("C:/Users/User/Desktop/data/inspector.csv", inspectors, ["first_name", "last_name", "middle_name", "service_center_id"])
save_to_csv("C:/Users/User/Desktop/data/document.csv", documents, ["type", "end_date", "info_file_path", "client_id", "inspector_id"])
#save_to_csv("C:/Users/User/Desktop/data/client_driving_license.csv", client_liceneses, ["end_date", "client_id"])
save_to_csv("C:/Users/User/Desktop/data/inspector_driving_license.csv", inspector_licenses, ["end_date", "inspector_id"])
#save_to_csv("C:/Users/User/Desktop/data/client_driving_license_category.csv", client_license_categories, ["category", "gearbox", "license_id"])
save_to_csv("C:/Users/User/Desktop/data/inspector_driving_license_category.csv", inspector_license_categories, ["category", "gearbox", "license_id"])
save_to_csv("C:/Users/User/Desktop/data/car.csv", cars, ["car_owner", "gearbox", "license_plate", "category", "service_center_id"])
save_to_csv("C:/Users/User/Desktop/data/theory_ticket.csv", theory_tickets, ["datetime", "status", "service_center_id", "client_id"])
save_to_csv("C:/Users/User/Desktop/data/driving_ticket.csv", driving_tickets, ["datetime", "status", "gearbox", "car_owner", "service_center_id", "client_id", "category"])
save_to_csv("C:/Users/User/Desktop/data/theory_exam.csv", theory_exams, ["theory_ticket_id"])
save_to_csv("C:/Users/User/Desktop/data/question.csv", questions, ["text", "photo_file_path"])
save_to_csv("C:/Users/User/Desktop/data/answer.csv", answers, ["text", "photo_file_path", "is_correct", "question_id"])
save_to_csv("C:/Users/User/Desktop/data/theory_exam_result.csv", theory_exam_results, ["theory_exam_id", "question_id", "answer_id"])
save_to_csv("C:/Users/User/Desktop/data/driving_exam.csv", driving_exams, ["exam_result", "video_file_path", "driving_ticket_id", "inspector_id", "car_id"])
save_to_csv("C:/Users/User/Desktop/data/fine.csv", fines, ["status", "reason", "sum", "license_id"])
save_to_csv("C:/Users/User/Desktop/data/driving_license_status.csv", license_statuses, ["status", "end_date", "reason", "license_id"])