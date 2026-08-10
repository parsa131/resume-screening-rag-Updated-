import ollama
import json
from tools import AVAILABLE_TOOLS
TOOL_SCHEMAS = [
    {
        "type" : "function",
        "function" : {
            "name" : "search_resume" ,
            "description" : "searches for resume with the max compability" ,
            "parameters" : {
                "type" : "object" ,
                "properties" : {
                    "query" : {"type" : "string" , "description" : "the sentence that the search for the docs is based on"} ,
                    "n_results" : {"type" : "integer" , "description" : "the amount of documents that is shown by the search "} 
                } ,
            "required":["query"]
            }
        }
    }

    ,

    {
        "type" : "function" ,
        "function" : {
            "name" : "get_candidate_score" , 
            "description" : "show the required skill and the missing skills and the score of the candidate based on the requirement list" ,
            "parameters" : {
                "type" : "object" , 
                "properties" : {
                    "candidate_id" : {"type" : "string" , "description" : "mention the candidate id"} ,
                    "required_skills": {"type" : "array" , "description":"the list of words that is searched in candidate document"}
                } ,
            "required":["candidate_id" , "required_skills"]
            }
        }
    }
    ,
    {
        "type" : "function" ,
        "function" : {
            "name" : "compare_candidates" , 
            "description" : "compare candidates based on their candidate score from highest to lowest" ,
            "parameters" : {
                "type" : "object" , 
                "properties" : {
                    "candidate_ids" : {"type" : "array" , "description" : "list of candidates ids"} ,
                    "required_skills": {"type" : "array" , "description":"a list for required skills"}
                } ,
            "required":["candidate_ids" , "required_skills"]
            }
        }
    }
    ,
    {
        "type" : "function" ,
        "function" : {
            "name" : "filter_by_criteria" , 
            "description" : "shows the candidate by filtering their year experience and skill" ,
            "parameters" : {
                "type" : "object" , 
                "properties" : {
                    "min_years_experience" : {"type" : "integer" , "description" : "minimum of needed  experience year for candidate"} ,
                    "required_skill": {"type" : "string" , "description":"an skill needed to search for candidate"}
                } ,
            "required":[]
            }
        }
        
    }
]

...


def run_agent(user_question: str):
    messages = [
        {"role": "user", "content": user_question}
    ]

    while True : 
        response = ollama.chat(
            model="llama3.2:3b",
            messages=messages,
            tools=TOOL_SCHEMAS
        )
        msg = response["message"]
        messages.append(msg)
        tool_calls = msg.get("tool_calls")

        if not tool_calls :
            return msg.get("content", "")
        for call in tool_calls:
            func_name = call["function"]["name"]
            func_args = call["function"]["arguments"]

            func = AVAILABLE_TOOLS[func_name]
            result = func(**func_args)

            messages.append(
                {
                    "role" : "tool" ,
                    "content" : json.dumps(result , ensure_ascii= False)
                }
            )


context = ""

if __name__ == "__main__":
    answer = run_agent(context)
    print(answer)