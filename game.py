import random
import time
import ollama

suspects_base = [
    {"nom": "Alice", "personnalité": "nerveuse et bavarde", "alibi": "était au cinéma"},
    {"nom": "Bob", "personnalité": "calme et mystérieux", "alibi": "était chez lui seul"},
    {"nom": "Charlie", "personnalité": "arrogant et sûr de lui", "alibi": "était en voyage d'affaires"}
]


def interroger_suspect(suspect, question):
    
    prompt = f"""
    Tu es {suspect['nom']}, un suspect dans une enquête policière. Tu es {suspect['personnalité']}.
    Ton alibi est : {suspect['alibi']}.
    Réponds à la question suivante comme si tu étais ce personnage, en restant dans ton rôle. Tu peux dissimuler des informations si nécessaire pour éviter d'être accusé. Tu peux aussi donner des indices subtils.
    Tes réponses doivent être courtes, maximum 4 phrases.
    Règle importante :
    - Si la question est vide, contient du charabia, des fautes de grammaire graves, 
      ou n'est pas une phrase claire en français correct,
      réponds uniquement et strictement par : "Je n'ai pas compris la question."
    - Ne tente JAMAIS de deviner ou d'interpréter le sens de la question.
    - Si tu n’es pas sûr de comprendre, réponds quand même : "Je n'ai pas compris la question."

    
    Question : {question}
    """
    
    try:
        response = ollama.generate(model="gemma3:latest", prompt=prompt)
        return response.get("response", "<pas de réponse>")
    except Exception as e:
        return f"<Erreur Ollama : {e}>"


def jeu_enquete(score):
    questions_posées = 0
    suspects = suspects_base.copy()
    coupable = random.choice(suspects)

    print("\nBienvenue dans le jeu d'enquête !")
    print("Trois suspects : Alice, Bob, Charlie.")
    print("Pose des questions pour découvrir le coupable.\n")

    for suspect in suspects:
        print(f"\nInterrogatoire de {suspect['nom']}")
        while True:
            question = input("Quelle question veux-tu poser ? (ou tape 'stop' pour passer au suivant) ")
            if question.lower() == "stop":
                break
            reponse = interroger_suspect(suspect, question)
            print(f"{suspect['nom']} répond : {reponse}")
            questions_posées += 1
            time.sleep(1)

    choix = input("\nQui est le coupable selon toi ? (Alice, Bob, Charlie) : ").strip()
    choix_lower = choix.lower()
    noms_valides = [s['nom'].lower() for s in suspects]

    while choix_lower not in noms_valides:
        print("Le coupable ne fait pas partie de la liste !")
        choix = input("Veuillez entrer un nom valide (Alice, Bob, Charlie) : ").strip()
        choix_lower = choix.lower()

    if choix_lower == coupable["nom"].lower():
        score += 10
        if questions_posées <= 5:
            score += 5
        print(f"Bravo ! Tu as trouvé le coupable ! 🎉")
    else:
        print(f"Dommage... Le coupable était {coupable['nom']}.")
        
    print(f"Ton score : {score} points")
    return score
    

if __name__ == "__main__":
    score_cumulatif = 0
    while True:
        score_cumulatif = jeu_enquete(score_cumulatif)
        rejouer = input("\nVeux-tu rejouer ? (oui/non) : ").strip().lower()
        if rejouer != "oui":
            print("Merci d'avoir joué ! Score final :", score_cumulatif)
            break