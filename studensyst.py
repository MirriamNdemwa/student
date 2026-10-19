import csv
from abc import ABC, abstractmethod


class Learner(ABC):

    def __init__(self, admission_no, first_name, last_name, course,
                 mathematics, english, science):
        self.__admission_no = admission_no
        self.__first_name = first_name
        self.__last_name = last_name
        self.__course = course
        self.__mathematics = self.check_mark(mathematics)
        self.__english = self.check_mark(english)
        self.__science = self.check_mark(science)

    @staticmethod
    def check_mark(mark):
        if isinstance(mark, bool) or not isinstance(mark, (int, float)):
            raise ValueError("A mark must be numeric.")
        if not 0 <= mark <= 100:
            raise ValueError("A mark must be between 0 and 100.")
        return float(mark)

    def get_admission_no(self):
        return self.__admission_no

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_course(self):
        return self.__course

    def get_results(self):
        return {
            "Mathematics": self.__mathematics,
            "English": self.__english,
            "Science": self.__science
        }

    def update_results(self, mathematics, english, science):
        new_math = self.check_mark(mathematics)
        new_english = self.check_mark(english)
        new_science = self.check_mark(science)

        self.__mathematics = new_math
        self.__english = new_english
        self.__science = new_science

    def update_profile(self, admission_no, first_name, last_name, course):
        if not all([admission_no, first_name, last_name, course]):
            raise ValueError("Learner details cannot be empty.")

        self.__admission_no = admission_no
        self.__first_name = first_name
        self.__last_name = last_name
        self.__course = course

    def calculate_average(self):
        results = self.get_results()
        return sum(results.values()) / len(results)

    def determine_grade(self):
        average = self.calculate_average()

        if average < 40:
            return "F"
        elif average < 50:
            return "D"
        elif average < 60:
            return "C"
        elif average < 70:
            return "B"
        return "A"

    @staticmethod
    def average_of(*marks):
        if len(marks) == 1 and isinstance(marks[0], (list, tuple)):
            marks = tuple(marks[0])

        if not marks:
            raise ValueError("At least one mark is required.")

        checked_marks = [Learner.check_mark(mark) for mark in marks]
        return sum(checked_marks) / len(checked_marks)

    @abstractmethod
    def learner_category(self):
        pass

    def performance_summary(self):
        return (
            f"{self.learner_category()} | "
            f"{self.get_first_name()} {self.get_last_name()} | "
            f"Average: {self.calculate_average():.2f} | "
            f"Grade: {self.determine_grade()}"
        )

    def create_report(self):
        results = self.get_results()

        return (
            "\n========== ACADEMIC RECORD ==========\n"
            f"Admission Number: {self.get_admission_no()}\n"
            f"Learner: {self.get_first_name()} {self.get_last_name()}\n"
            f"Course: {self.get_course()}\n"
            f"Category: {self.learner_category()}\n"
            f"Mathematics: {results['Mathematics']:.2f}\n"
            f"English: {results['English']:.2f}\n"
            f"Science: {results['Science']:.2f}\n"
            f"Mean Score: {self.calculate_average():.2f}\n"
            f"Grade: {self.determine_grade()}\n"
        )


class UniversityLearner(Learner):

    def __init__(self, admission_no, first_name, last_name, course,
                 mathematics, english, science, study_year):
        super().__init__(
            admission_no, first_name, last_name, course,
            mathematics, english, science
        )
        self.study_year = study_year

    def learner_category(self):
        return "University Learner"

    def create_report(self):
        return (
            super().create_report()
            + f"Study Year: {self.study_year}\n"
        )


class SponsoredLearner(UniversityLearner):

    def __init__(self, admission_no, first_name, last_name, course,
                 mathematics, english, science, study_year, funding):
        super().__init__(
            admission_no, first_name, last_name, course,
            mathematics, english, science, study_year
        )

        if isinstance(funding, bool) or not isinstance(funding, (int, float)):
            raise ValueError("Funding must be a number.")
        if funding < 0:
            raise ValueError("Funding cannot be negative.")

        self.__funding = funding

    def get_funding(self):
        return self.__funding

    def qualifies_for_sponsorship(self):
        return self.calculate_average() >= 85

    def learner_category(self):
        return "Sponsored Learner"

    def create_report(self):
        status = "Yes" if self.qualifies_for_sponsorship() else "No"

        return (
            super().create_report()
            + f"Funding Amount: KSh {self.get_funding():,.2f}\n"
            + f"Meets Performance Requirement: {status}\n"
        )

    def performance_summary(self):
        status = (
            "Meets requirement"
            if self.qualifies_for_sponsorship()
            else "Below requirement"
        )
        return f"{super().performance_summary()} | {status}"


class AcademicAnalyzer:

    def __init__(self, learners):
        self.learners = list(learners)

    def best_performer(self):
        if not self.learners:
            return None
        return max(self.learners, key=lambda learner: learner.calculate_average())

    def needs_support(self):
        if not self.learners:
            return None
        return min(self.learners, key=lambda learner: learner.calculate_average())

    def mean_class_score(self):
        if not self.learners:
            return 0.0
        return sum(
            learner.calculate_average() for learner in self.learners
        ) / len(self.learners)


class AcademicReports:

    def __init__(self, analyzer):
        self.analyzer = analyzer

    def print_learner_record(self, learner):
        print(learner.create_report())

    def print_overview(self):
        learners = self.analyzer.learners

        print("\n========== CLASS OVERVIEW ==========")

        if not learners:
            print("No learner records were loaded.")
            return

        best = self.analyzer.best_performer()
        lowest = self.analyzer.needs_support()

        print(
            f"Top Performer: {best.get_first_name()} "
            f"{best.get_last_name()} - {best.calculate_average():.2f}"
        )
        print(
            f"Lowest Average: {lowest.get_first_name()} "
            f"{lowest.get_last_name()} - {lowest.calculate_average():.2f}"
        )
        print(
            f"Class Mean: {self.analyzer.mean_class_score():.2f}"
        )


def read_learners(filename):
    learners = []

    with open(filename, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file, skipinitialspace=True)

        if reader.fieldnames:
            reader.fieldnames = [
                heading.strip() for heading in reader.fieldnames
            ]

        required = {
            "StudentID", "FName", "LName", "Programme",
            "Math", "English", "Science"
        }

        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError("CSV column headings do not match the expected format.")

        for row_number, row in enumerate(reader, start=2):
            try:
                admission_no = row["StudentID"].strip()
                first_name = row["FName"].strip()
                last_name = row["LName"].strip()
                course = row["Programme"].strip()

                if not all([admission_no, first_name, last_name, course]):
                    raise ValueError("Learner details cannot be empty.")

                mathematics = Learner.check_mark(float(row["Math"]))
                english = Learner.check_mark(float(row["English"]))
                science = Learner.check_mark(float(row["Science"]))

                average = (mathematics + english + science) / 3
                study_year = "Not specified"

                common = (
                    admission_no, first_name, last_name, course,
                    mathematics, english, science, study_year
                )

                if average >= 85:
                    learner = SponsoredLearner(
                        *common, funding=50000
                    )
                else:
                    learner = UniversityLearner(*common)

                learners.append(learner)

            except (ValueError, TypeError, KeyError) as error:
                raise ValueError(
                    f"Problem in CSV row {row_number}: {error}"
                ) from error

    return learners


def main():
    try:
        learners = read_learners("student.csv")

        if not learners:
            print("No learner data was found.")
            return

        print("\n========== LEARNER PERFORMANCE ==========")
        for learner in learners:
            print(learner.performance_summary())

        analyzer = AcademicAnalyzer(learners)
        reports = AcademicReports(analyzer)

        print("\n========== LEARNER RECORDS ==========")
        for learner in learners:
            reports.print_learner_record(learner)

        reports.print_overview()

        print("\n========== FLEXIBLE AVERAGE TEST ==========")
        print("Separate marks:", Learner.average_of(75, 80, 70))
        print("List of marks:", Learner.average_of([75, 80, 70]))
        print("Different number of marks:", Learner.average_of(70, 75, 80, 85, 90))

    except (OSError, ValueError) as error:
        print(f"Unable to process records: {error}")


if __name__ == "__main__":
    main()
