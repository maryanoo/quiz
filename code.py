import re
import random
import os
import datetime

def extract_questions(latex_file):
    """Wyodrębnia pytania zamknięte z pliku LaTeX."""
    with open(latex_file, 'r', encoding='utf-8') as f:
        latex_content = f.read()

    # Znajdź bloki questions
    questions_blocks = re.findall(r'\\begin{questions}(.*?)\\end{questions}', latex_content, re.DOTALL)

    all_questions = []
    for block in questions_blocks:
        # Znajdź wszystkie pytania w bloku
        question_matches = re.findall(r'\\question(.*?)\\begin{choices}(.*?)\\end{choices}', block, re.DOTALL)
        for q_match in question_matches:
            question_text = q_match[0].strip()
            choice_block = q_match[1].strip()
            
            choices = []
            correct_choice_indices = []
            
            choice_matches = re.findall(r'\\(correctchoice|choice)\s*(.*?)(?=\s*\\(correctchoice|choice)|$)', choice_block, re.DOTALL)
            for i, choice_match in enumerate(choice_matches):
                choice_type = choice_match[0].strip()
                choice_text = choice_match[1].strip()
                choices.append(choice_text)
                if choice_type == "correctchoice":
                    correct_choice_indices.append(i)
                
            
            all_questions.append({
                'question': question_text,
                'choices': choices,
                'correct_choices': correct_choice_indices
            })
            
    return all_questions

def shuffle_choices(question_data):
    """Losowo miesza kolejność odpowiedzi w pytaniu."""
    
    choices = question_data['choices']
    correct_choices = question_data["correct_choices"]
    
    # Stwórz listę par (indeks, treść) odpowiedzi
    indexed_choices = list(enumerate(choices))
    
    # Losowo przemieszaj pary
    random.shuffle(indexed_choices)
    
    # Zdobądź nowe indeksy poprawnych odpowiedzi po przemieszaniu
    new_correct_choices = []
    
    new_choices = []
    for new_index, (old_index, choice_text) in enumerate(indexed_choices):
        new_choices.append(choice_text)
        if old_index in correct_choices:
            new_correct_choices.append(new_index)
            
    
    
    question_data['choices'] = new_choices
    question_data["correct_choices"] = new_correct_choices
    
    return question_data

def generate_random_quiz(questions, num_questions=15):
    """Generuje losowy quiz z pytań zamkniętych."""
    if len(questions) < num_questions:
        raise ValueError("Liczba dostępnych pytań jest mniejsza niż wymagana liczba pytań w quizie.")

    random_questions = random.sample(questions, num_questions)
    
    # Przemieszaj kolejność odpowiedzi dla każdego pytania
    shuffled_questions = [shuffle_choices(q) for q in random_questions]

    return shuffled_questions

def create_latex_quiz(quiz_questions, output_file):
  """Tworzy dokument LaTeX z losowymi pytaniami."""
  
  latex_content = r"""\documentclass[addpoints,11pt,a4paper]{exam}
\usepackage[utf8]{inputenc}
\usepackage[polish]{babel}

\title{Losowy Quiz z Metod i technik badań społecznych}
\date{\today}
\author{Wygenerowany losowo}

\begin{document}

\maketitle
\textbf{Imię i nazwisko:} \hrulefill \\\
\textbf {Instrukcja}W pytaniach dopuszcza się możliwość wyboru więcej niż jednej odpowiedzi. Za każde pytanie można zdobyć maksymalnie 3 punkty. Aby uzyskać pełną punktację, należy zaznaczyć wszystkie prawidłowe odpowiedzi. Częściowo prawidłowe odpowiedzi są wliczane do punktacji proporcjonalnie. Zaznaczenie błędnej odpowiedzi powoduje nie naliczenie punktów za dane pytanie.

\begin{questions}
"""
  
  for question_data in quiz_questions:
        latex_content += f"\question {question_data['question']}\n"
        latex_content += "\\begin{choices}\n"
        for i, choice in enumerate(question_data['choices']):
            if i in question_data["correct_choices"]:
              latex_content += f"\t\\correctchoice {choice}\n"
            else:
              latex_content += f"\t\\choice {choice}\n"
        latex_content += "\\end{choices}\n\n"
  
  latex_content += r"""
\end{questions}
\end{document}
"""
  with open(output_file, "w", encoding="utf-8") as f:
      f.write(latex_content)


if __name__ == "__main__":
    latex_file = "egzmiamin_zima_zaoczni.tex" # Zmień na nazwę Twojego pliku
    try:
        all_questions = extract_questions(latex_file)
        quiz_questions = generate_random_quiz(all_questions)
        
        # Get current minute for filename
        current_minute = datetime.datetime.now().strftime("%M")
        output_latex_file = f"quiz_{current_minute}.tex"
        
        create_latex_quiz(quiz_questions, output_latex_file)
        print(f"Wygenerowano losowy quiz w pliku {output_latex_file}")
    except ValueError as e:
        print(f"Błąd: {e}")
