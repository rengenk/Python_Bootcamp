import multiprocessing
import os
import random
import time
import math
from typing import List
from prettytable import PrettyTable

GOLDEN_RATIO = (1 + math.sqrt(5)) / 2

class Question:
    def __init__(self, text: str):
        self.text = text
        self.words = text.split()
        self.correct_answers = 0
        self.total_attempts = 0

class Student:
    def __init__(self, name: str, gender: str):
        self.name = name
        self.gender = gender
        self.status = "Очередь"
        self.exam_start_time = None
        self.exam_end_time = None
        self.examiner = None

class Examiner:
    def __init__(self, name: str, gender: str):
        self.name = name
        self.gender = gender
        self.current_student = None
        self.total_students = 0
        self.failed_students = 0
        self.work_time = 0.0
        self.is_on_lunch = False
        self.is_finished = False

class Exam:
    def __init__(self):
        self.examiners: List[Examiner] = []
        self.students: List[Student] = []
        self.questions: List[Question] = []
        self.student_queue = None
        self.student_status = None
        self.completed_students = None
        self.examiner_stats = None
        self.question_stats = None
        self.print_lock = None
        self.exam_start_time = None

    @staticmethod
    def parse_people(data: str):
        values = data.split()
        pairs = zip(values[::2], values[1::2])
        return list(pairs)

    @staticmethod
    def parse_questions(data: str):
        return list(
            filter(
                bool,
                map(str.strip, data.splitlines())
            )
        )

    def load_data(self, manager):
        self.student_queue = manager.Queue()
        self.student_status = manager.dict()
        self.completed_students = manager.list()
        self.examiner_stats = manager.dict()
        self.question_stats = manager.dict()
        self.print_lock = manager.Lock()

        with open("examiners.txt", "r", encoding="utf-8") as f:
            examiner_data = self.parse_people(f.read())

        with open("students.txt", "r", encoding="utf-8") as f:
            student_data = self.parse_people(f.read())

        with open("questions.txt", "r", encoding="utf-8") as f:
            question_data = self.parse_questions(f.read())

        self.examiners = [
            Examiner(name, gender)
            for name, gender in examiner_data
        ]

        self.students = [
            Student(name, gender)
            for name, gender in student_data
        ]

        self.questions = list(map(Question, question_data))
        self.students.sort(key=lambda student: student.name)
        self.examiners.sort(key=lambda examiner: examiner.name)

        for student in self.students:
            self.student_queue.put(student.name)
            self.student_status[student.name] = "Очередь"

        for examiner in self.examiners:
            self.examiner_stats[examiner.name] = {
                "current_student": "-",
                "total_students": 0,
                "failed_students": 0,
                "work_time": 0.0,
                "is_on_lunch": False,
                "is_finished": False,
            }

        for index, question in enumerate(self.questions):
            self.question_stats[index] = {
                "text": question.text,
                "correct_answers": 0,
                "total_attempts": 0,
            }

    @staticmethod
    def calculate_golden_ratio_probabilities(word_count: int) -> List[float]:
        probabilities = []
        remaining_prob = 1.0

        for i in range(word_count):
            if i == word_count - 1:
                probabilities.append(remaining_prob)
            else:
                probability = remaining_prob / GOLDEN_RATIO
                probabilities.append(probability)
                remaining_prob -= probability

        return probabilities

    @classmethod
    def select_word_by_gender(cls, question: Question, gender: str) -> str:
        probabilities = cls.calculate_golden_ratio_probabilities(
            len(question.words)
        )

        if gender == "М":
            return random.choices(
                question.words,
                weights=probabilities
            )[0]

        return random.choices(
            question.words,
            weights=probabilities[::-1]
        )[0]

    @staticmethod
    def examiner_selects_answers(question: Question) -> List[str]:
        selected_answers = set()

        while True:
            selected_answers.add(random.choice(question.words))

            if (
                random.random() > 1 / 3
                or len(selected_answers) == len(question.words)
            ):
                break

        return list(selected_answers)

    def conduct_exam_for_student(self, student: Student) -> bool:
        name_length = len(self.current_examiner_name)
        exam_duration = random.uniform(
            max(0.1, name_length - 1),
            name_length + 1
        )

        correct_answers = 0
        total_questions = min(3, len(self.questions))

        for _ in range(total_questions):
            question_index = random.randrange(len(self.questions))
            question = self.questions[question_index]

            stats = dict(self.question_stats[question_index])
            stats["total_attempts"] += 1

            student_answer = self.select_word_by_gender(
                question,
                student.gender
            )
            correct_answers_list = self.examiner_selects_answers(question)

            if student_answer in correct_answers_list:
                correct_answers += 1
                stats["correct_answers"] += 1

            self.question_stats[question_index] = stats

        time.sleep(exam_duration)

        mood = random.random()

        if mood < 1 / 8:
            return False
        if mood < 1 / 8 + 1 / 4:
            return True

        return correct_answers > (total_questions - correct_answers)

    def examiner_process(self, examiner_name: str):
        examiner_data = dict(self.examiner_stats[examiner_name])
        lunch_taken = False

        while True:
            current_time = time.time() - self.exam_start_time

            if not lunch_taken and current_time >= 30:
                examiner_data["is_on_lunch"] = True
                self.examiner_stats[examiner_name] = examiner_data

                lunch_duration = random.uniform(12, 18)
                time.sleep(lunch_duration)

                examiner_data["is_on_lunch"] = False
                self.examiner_stats[examiner_name] = examiner_data
                lunch_taken = True

            try:
                student_name = self.student_queue.get_nowait()
            except Exception:
                examiner_data["current_student"] = "-"
                examiner_data["is_finished"] = True
                self.examiner_stats[examiner_name] = examiner_data
                break

            student = next(
                student for student in self.students_data
                if student["name"] == student_name
            )

            examiner_data["current_student"] = student_name
            examiner_data["total_students"] += 1
            self.examiner_stats[examiner_name] = examiner_data

            self.current_examiner_name = examiner_name
            self.questions = [Question(text) for text in self.questions_data]

            start_time = time.time()
            self.student_status[student_name] = "Очередь"

            result = self.conduct_exam_for_student(
                Student(student["name"], student["gender"])
            )

            end_time = time.time()

            self.student_status[student_name] = (
                "Сдал" if result else "Провалил"
            )

            examiner_data["work_time"] += end_time - start_time

            if not result:
                examiner_data["failed_students"] += 1

            examiner_data["current_student"] = "-"
            self.examiner_stats[examiner_name] = examiner_data

            self.completed_students.append({
                "name": student_name,
                "status": "Сдал" if result else "Провалил",
                "duration": end_time - start_time,
            })

    def make_process_safe_data(self):
        self.students_data = [
            {
                "name": student.name,
                "gender": student.gender,
            }
            for student in self.students
        ]

        self.questions_data = [
            question.text for question in self.questions
        ]

    def display_current_status(self):
        while True:
            os.system("cls" if os.name == "nt" else "clear")

            with self.print_lock:
                students = sorted(
                    self.student_status.items(),
                    key=lambda item: item[0]
                )
                
                table = PrettyTable()
                table.field_names = ["Студент", "Статус"]

                for name, status in students:
                    table.add_row([name, status])

                print(table)
                print()

                table = PrettyTable()
                table.field_names = [
                    "Экзаменатор",
                    "Текущий студент",
                    "Всего студентов",
                    "Завалил",
                    "Время работы"
                ]

                for examiner in self.examiners:
                    stats = dict(self.examiner_stats[examiner.name])

                    current_student = (
                        "Обед"
                        if stats["is_on_lunch"]
                        else stats["current_student"]
                    )

                    table.add_row([
                        examiner.name,
                        current_student,
                        stats["total_students"],
                        stats["failed_students"],
                        f"{stats['work_time']:.2f}"
                    ])

                print(table)
                print()

                remaining = sum(
                    status == "Очередь"
                    for status in self.student_status.values()
                )
                total = len(self.students)
                elapsed = time.time() - self.exam_start_time

                print(f"Осталось в очереди: {remaining} из {total}")
                print(
                    f"Время с момента начала экзамена: "
                    f"{elapsed:.2f}"
                )

            all_finished = all(
                dict(self.examiner_stats[e.name])["is_finished"]
                for e in self.examiners
            )

            if all_finished and remaining == 0:
                break

            time.sleep(0.5)

    def display_final_results(self):
        os.system("cls" if os.name == "nt" else "clear")

        students = sorted(
            self.student_status.items(),
            key=lambda item: item[0]
        )
        
        table = PrettyTable()
        table.field_names = ["Студент", "Статус"]

        for name, status in students:
            table.add_row([name, status])

        print(table)
        print()

        table = PrettyTable()
        table.field_names = [
            "Экзаменатор",
            "Всего студентов",
            "Завалил",
            "Время работы"
        ]

        for examiner in self.examiners:
            stats = dict(self.examiner_stats[examiner.name])

            table.add_row([
                examiner.name,
                stats["total_students"],
                stats["failed_students"],
                f"{stats['work_time']:.2f}"
            ])

        print(table)
        print()

        total_time = time.time() - self.exam_start_time

        print(
            "Время с момента начала экзамена и до момента "
            f"его завершения: {total_time:.2f}"
        )

        completed = list(self.completed_students)

        passed = [
            item for item in completed
            if item["status"] == "Сдал"
        ]

        failed = [
            item for item in completed
            if item["status"] == "Провалил"
        ]

        if passed:
            fastest = min(item["duration"] for item in passed)
            best_students = [
                item["name"]
                for item in passed
                if item["duration"] == fastest
            ]
            print(
                f"Имена лучших студентов: {', '.join(best_students)}"
            )

        examiner_stats = []

        for examiner in self.examiners:
            stats = dict(self.examiner_stats[examiner.name])

            if stats["total_students"] > 0:
                fail_rate = (
                    stats["failed_students"]
                    / stats["total_students"]
                )
                examiner_stats.append(
                    (examiner.name, fail_rate)
                )

        if examiner_stats:
            min_fail_rate = min(
                rate for _, rate in examiner_stats
            )
            best_examiners = [
                name
                for name, rate in examiner_stats
                if rate == min_fail_rate
            ]
            print(
                "Имена лучших экзаменаторов: "
                f"{', '.join(best_examiners)}"
            )

        if failed:
            earliest_fail = min(
                item["duration"] for item in failed
            )
            expelled_students = [
                item["name"]
                for item in failed
                if item["duration"] == earliest_fail
            ]
            print(
                "Имена студентов, которых после экзамена "
                f"отчислят: {', '.join(expelled_students)}"
            )

        question_stats = [
            dict(self.question_stats[index])
            for index in range(len(self.questions))
        ]

        used_questions = [
            stats for stats in question_stats
            if stats["total_attempts"] > 0
        ]

        if used_questions:
            max_success_rate = max(
                stats["correct_answers"]
                / stats["total_attempts"]
                for stats in used_questions
            )

            best_questions = [
                stats["text"]
                for stats in used_questions
                if (
                    stats["correct_answers"]
                    / stats["total_attempts"]
                ) == max_success_rate
            ]

            print(
                f"Лучшие вопросы: {', '.join(best_questions)}"
            )

        total_students = len(self.students)
        passed_count = len(passed)
        success_rate = (
            passed_count / total_students
            if total_students
            else 0
        )

        if success_rate > 0.85:
            print("Вывод: экзамен удался")
        else:
            print("Вывод: экзамен не удался")

    def run_simulation(self):
        manager = multiprocessing.Manager()

        try:
            self.load_data(manager)
            self.make_process_safe_data()
            self.exam_start_time = time.time()

            status_process = multiprocessing.Process(
                target=self.display_current_status
            )
            status_process.daemon = True
            status_process.start()

            processes = []

            for examiner in self.examiners:
                process = multiprocessing.Process(
                    target=self.examiner_process,
                    args=(examiner.name,)
                )
                processes.append(process)
                process.start()

            for process in processes:
                process.join()

            status_process.join()

            self.display_final_results()
        finally:
            manager.shutdown()

if __name__ == "__main__":
    multiprocessing.freeze_support()

    simulation = Exam()
    simulation.run_simulation()
