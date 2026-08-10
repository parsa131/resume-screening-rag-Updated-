import ollama
import chromadb


client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="my_docs")
# -----------------------------------------------------------------------------------------------------------------------------
def search_resume(query : str , n_results :int = 3 ) : 
    n_results = int(n_results)
    results = collection.query(
        query_texts= query , 
        n_results=n_results
    )
    output = []
    for i, (doc_id, doc, distance) in enumerate(zip(results['ids'][0], results['documents'][0], results['distances'][0])):
        output.append({
            "rank" : i+1 , 
            "candidate_id" : doc_id,
            "distance" : round(distance , 4),
            "preview" : doc[:150]

        })
    return output

# -----------------------------------------------------------------------------------------------------------------------------
def get_candidate_score(candidate_id : str , required_skills : list[str]) : 

    doc =collection.get(ids= [candidate_id])
    document = doc["documents"][0].lower()
    temp = 0
    have_required = []
    for skill in required_skills : 
        skill = skill.lower()
        if skill in document : 
            temp +=1 
            have_required.append(skill)
    temp1 = [skills.lower() for skills in required_skills]
    for i in have_required :
        temp1.remove(i)
    return {"candidate id" : candidate_id , "required skill":required_skills ,"candidate matching skill":have_required , 
          "candidate missing skills" : temp1 ,"candidate score" : round((temp / len(required_skills)) * 100, 2)  }

# -----------------------------------------------------------------------------------------------------------------------------
def compare_candidates(candidate_ids: list[str], required_skills: list[str]) :
    results = []
    for i in candidate_ids :
        results.append(get_candidate_score(i , required_skills= required_skills))
    results = results.sort(key=lambda item : item["candidate score"] , reverse=True)
# -----------------------------------------------------------------------------------------------------------------------------
import re

def filter_by_criteria(min_years_experience: int = 0, required_skill: str = ""):
    min_years_experience = int(min_years_experience)
    all_docs = collection.get()
    matches = []
    for doc_id, doc in zip(all_docs["ids"], all_docs["documents"]):
        text_lower = doc.lower()
        if required_skill and required_skill.lower() not in text_lower:
            continue
        years_match = re.findall(r"(\d+)\+?\s*years?", text_lower)
        years_found = max((int(y) for y in years_match), default=0)
        if years_found >= min_years_experience:
            matches.append({"candidate_id": doc_id, "years_experience_found": years_found})

    return {"matches": matches}

# -----------------------------------------------------------------------------------------------------------------------------
# ... now defining tools ...
# -----------------------------------------------------------------------------------------------------------------------------
AVAILABLE_TOOLS = {
    "search_resume": search_resume,
    "get_candidate_score": get_candidate_score,
    "compare_candidates": compare_candidates,
    "filter_by_criteria": filter_by_criteria,
}

