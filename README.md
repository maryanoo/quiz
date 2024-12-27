Simple script for generating randomized quizzes from LaTeX exams.

This Python script parses a LaTeX document to identify multiple-choice questions within a defined environment (using regular expressions). It then:
 - Randomly selects a specified number of questions.
 - Shuffles the order of answer choices for each question.
 - Generates a new LaTeX document with the selected and shuffled questions.
 - Compiles the new document into a PDF automatically, leveraging the `pdflatex` command.

This project is useful for educators who need to quickly create multiple versions of a quiz from a larger question pool.
